# ---------- Импорты из проекта ---------- #
from tables.table import Table
from configs.text import Text
# ---------------------------------------- #


class AuthorizationTable(Table):
    # ---------- Поля и свойства класса AuthorizationTable --------- #
    TELEGRAM_TOKEN = "Telegram_token"
    PAYMENT_TOKEN = "Payment_token"
    # --------------------------------------------------------- #

    # ---------- Конструктор класса AuthorizationTable ---------- #
    def __init__(self):
        """
        Конструктор класса AuthorizationTable: выполнение конструктора класса-родителя
        """

        # Определение необходимых полей, для корректной работы методов экспорта и импорта ↓
        super().__init__("Authorization", self.TELEGRAM_TOKEN)

        # Логирование ↓
        self._logger.info(Text.authorizationConnectedLog)
    # ----------------------------------------------------------- #

    # ---------- Переопределенные методы Table ---------- #
    def fillingTheTable(self, telegramToken: str, paymentToken: str) -> None:
        """
        Переопределенный метод Table, заполняющий таблицу Authorization
        :param telegramToken: Авторизационный токен бота Telegram
        :param paymentToken: Авторизационный токен оплаты бота
        :return: NoneType
        """

        # Удаление всех исходных данных из таблицы ↓
        self._cursor.execute(f"DELETE * FROM {self._tableName}")

        # Добавление актуальных авторизационных данных в таблицу ↓
        self._cursor.execute(f"INSERT INTO {self._tableName} VALUES (?, ?)", (telegramToken, paymentToken))
        self._connection.commit()  # сохранение изменений

        # Логирование ↓
        self._logger.warning(Text.fillingTheTableAuthorizationLog.format(self._tableName, self.TELEGRAM_TOKEN,
                                                                         telegramToken, self.PAYMENT_TOKEN, paymentToken))
    # --------------------------------------------------- #

    # ---------- Методы импорта данных из таблицы Authorization ---------- #
    def getTelegramToken(self) -> str:
        """
        Метод, возвращающий Telegram токен бота
        :return: telegramToken
        """

        # Возвращение телеграмм-токена из таблицы ↓
        return str(self.getDataFromColumn(columnName=self.TELEGRAM_TOKEN)[0])

    def getPaymentToken(self) -> str:
        """
        Метод, возвращающий токен оплаты бота
        :return: paymentToken
        """

        # Возвращение токена оплаты из таблицы ↓
        return str(self.getDataFromColumn(columnName=self.PAYMENT_TOKEN)[0])
    # --------------------------------------------------------------------- #
