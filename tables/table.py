# --------- Импорты встроенных библиотек --------- #
from logging import getLogger
from abc import ABC, abstractmethod
from sqlite3 import connect
# ------------------------------------------------ #

# ---------- Импорты дополнительных библиотек --------- #
from pandas import read_sql_query
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from configs.text import Text
# ---------------------------------------- #


class Table(ABC):
    # ---------- Поля класса Table ---------- #
    _connection = connect(database=Text.databaseFilepath)  # тип: sqlite3.Connection (обеспечить единственность объекта)
    _cursor = _connection.cursor()  # тип: sqlite3.Cursor (обеспечить единственность объекта)
    _logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)

    # -------------------------------------------------- #

    # ---------- Конструктор класса Table ---------- #
    def __init__(self, tableName: str, searchColumn: str):
        """
        Конструктор класса Table: определение необходимых полей, для корректной работы методов экспорта и импорта
        :param tableName: название таблицы
        :param searchColumn: название поискового столбца
        """

        self._tableName = tableName  # создание поля _tableName у экземпляра класса-наследника
        # Создание поля __searchColumn у экземпляра класса-наследника
        # ВАЖНО: поле __searchColumn может использоваться только в методах класса родителя
        self.__searchColumn = searchColumn

    # ---------------------------------------------- #

    # ---------- Абстрактные методы Table ---------- #
    @abstractmethod
    def fillingTheTable(self, **kwargs) -> None:
        """
        Абстрактный метод Table: заполнение таблицы (логирование по необходимости)
        :return: NoneType
        """

        pass

    # --------------------------------------------- #

    # ---------- Методы импорта данных из таблицы ---------- #
    def getDataFromField(self, lineData, columnName: str) -> object:
        """
        Метод, возвращающий содержание ячейки таблицы
        :param lineData: содержание поискового столбца
        :param columnName: название столбца
        :return: object
        """

        # Запрос в базу данных ↓
        self._cursor.execute(f"SELECT {columnName} FROM {self._tableName} WHERE {self.__searchColumn} = '{lineData}'")
        return self._cursor.fetchone()[0]  # возвращение одного объекта

    def getDataFromColumn(self, columnName: str) -> list[object]:
        """
        Метод, возвращающий содержание столбца
        :param columnName: название столбца
        :return: list[object]
        """

        # Запрос в базу данных ↓
        self._cursor.execute(f"SELECT {columnName} FROM {self._tableName}")
        return [data[0] for data in self._cursor.fetchall()]  # возвращение списка объектов

    def getDataFromLine(self, lineData) -> tuple[object] | None:
        """
        Метод, возвращающий содержание строки
        :param lineData: содержание поискового столбца
        :return: list[object]
        """

        # Запрос в базу данных ↓
        self._cursor.execute(f"SELECT * FROM {self._tableName} WHERE {self.__searchColumn} = '{lineData}'")
        return self._cursor.fetchone()

    def exportToExcel(self, filepath: str) -> None:
        """
        Метод, экспортирующий таблицу в xlsx
        :param filepath: относительный путь к экспортированной таблице
        :return: NoneType
        """
        # Преобразование sqlite3.Cursor в pandas.DataFrame ↓
        sqlQuery = read_sql_query(f"SELECT * FROM {self._tableName}", self._connection)
        sqlQuery.to_excel(filepath, index=False)  # сохранение преобразованной информации в xlsx базу данных

    # ----------------------------------------------------- #

    # ---------- Методы экспорта данных в таблицу --------- #
    def updateField(self, lineData, columnName: str, field) -> None:
        """
        Метод, обновляющий значение в ячейке таблицы
        :param lineData: содержание поискового столбца
        :param columnName: название столбца
        :param field: новое содержание ячейки
        :return: NoneType
        """

        if field is None:
            # Изменение содержания ячейки, в случае, если new_data является пустотой ↓
            self._cursor.execute(f"UPDATE {self._tableName} SET {columnName} = NULL "
                                 f"WHERE {self.__searchColumn} = '{lineData}'")
        else:
            # Изменение содержания ячейки, в случае, если new_data не является пустотой ↓
            self._cursor.execute(f"UPDATE {self._tableName} SET {columnName} = '{field}' "
                                 f"WHERE {self.__searchColumn} = '{lineData}'")
        self._connection.commit()  # сохранение изменений

    def removeLine(self, lineData) -> None:
        """
        Метод, удаляющий необходимую строку из таблицы
        :param lineData: содержание поискового столбца
        :return: NoneType
        """

        # Удаление строки из таблицы ↓
        self._cursor.execute(f"DELETE FROM {self._tableName} WHERE {self.__searchColumn} = '{lineData}'")
        self._connection.commit()  # сохранение изменений

    # ------------------------------------------------------ #
