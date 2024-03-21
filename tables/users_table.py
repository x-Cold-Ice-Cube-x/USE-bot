# --------- Импорты встроенных библиотек --------- #
from json import dumps
# ------------------------------------------------ #

# ---------- Импорты из проекта ---------- #
from tables.table import Table
from configs.text import Text
# ---------------------------------------- #


class UsersTable(Table):

    # ---------- Поля класса UsersTable ---------- #
    TELEGRAM_ID = "Telegram_ID"
    TELEGRAM_USERNAME = "Telegram_username"
    FIRST_NAME = "First_name"
    COUNT = "Count"
    MISTAKES = "Mistakes"
    # -------------------------------------------- #

    def __init__(self):
        """
        Конструктор класса UsersTable: выполнение конструктора класса-родителя
        """

        # Определение необходимых полей, для корректной работы методов экспорта и импорта ↓
        super().__init__(tableName="Users", searchColumn=self.TELEGRAM_ID)

        # Логирование ↓
        self._logger.info(Text.usersConnectedLog)

    def fillingTheTable(self, telegramID: int, username: str, firstName: str) -> None:
        """
        Переопределенный метод Table, заполняющий таблицу Users
        :param username: Имя пользователя телеграмм
        :param firstName: Имя пользователя телеграмм
        :param telegramID: Идентификационный код пользователя Telegram
        :return: NoneType
        """

        # Добавление нового пользователя в базу данных ↓
        self._cursor.execute(f"INSERT INTO {self._tableName} VALUES (?, ?, ?, ?, ?)", (telegramID, username, firstName, 0, "{}"))
        self._connection.commit()  # сохранение изменений

        # Логирование ↓
        self._logger.info(Text.fillingTheTableUsersLog.format(self._tableName, self.TELEGRAM_ID, telegramID))

    def getLeaderboard(self) -> list[tuple[str, int]]:
        usernames = sorted(map(str, self.getDataFromColumn(columnName=self.TELEGRAM_USERNAME)), reverse=True)
        firstNames = self.getDataFromColumn(columnName=self.FIRST_NAME)
        counts = self.getDataFromColumn(columnName=self.COUNT)
        leaderboard = [(f"<b>{firstNames[index]}</b> (@{usernames[index]})", int(counts[index])) for index in range(len(usernames))]
        leaderboard = sorted(leaderboard, key=lambda user: user[1], reverse=True)
        return [(f"{index + 1}. {leaderboard[index][0]}", leaderboard[index][1]) for index in range(len(leaderboard))]

    def getRank(self, telegram_id: int) -> int:
        userKey = f"<b>{self.getDataFromField(lineData=telegram_id, columnName=self.FIRST_NAME)}</b> (@{self.getDataFromField(lineData=telegram_id, columnName=self.TELEGRAM_USERNAME)})"
        for user in self.getLeaderboard():
            if userKey in user[0]:
                return self.getLeaderboard().index(user) + 1








