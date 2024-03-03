# --------- Импорты встроенных библиотек --------- #
from logging import getLogger, INFO, basicConfig
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot
from aiogram.types import Message
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.authorization_table import AuthorizationTable
from configs.text import Text
# ---------------------------------------- #


class USEBot(Bot):
    # ---------- Поля класса USEBot ---------- #
    __auth = None  # тип: AuthorizationTable (обеспечить единственность объекта)
    __dispatcher = None  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)
    # ---------------------------------------- #

    # ---------- Конструктор класса USEBot ---------- #
    def __init__(self):
        self.__setBasicConfig()  # создание объекта Logger (заранее, потому что дальше идет инициализация объектов)
        self.__setAttributes()  # заполнение всех полей класса
        super().__init__(token=self.__auth.getTelegramToken())  # авторизация бота в Telegram
    # ----------------------------------------------- #

    # ---------- Методы класса USEBot --------- #
    @classmethod
    def __setBasicConfig(cls) -> None:
        """
        Метод, устанавливающий базовую конфигурацию логирования
        :return: NoneType
        """

        # Установление конфигурации логирования ↓
        basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] - %(filename)s - %(message)s",
                    filename=Text.logsFilepath, filemode="a")

        # Логирование ↓
        cls.__logger.info(Text.loggerConnectedLog)

    @classmethod
    def __setAttributes(cls) -> None:
        """
        Метод, заполняющий поля класса USEBot (создание необходимых объектов)
        :return: NoneType
        """

        cls.__auth = AuthorizationTable()  # заполнение поля класса __authorization
        cls.__dispatcher = Dispatcher()  # заполнение поля класса __dispatcher
    # ----------------------------------------- #

    # ---------- Метод-запуск бота USEBot --------- #
    async def startPolling(self) -> None:
        """
        Метод-запуск USEBot в Telegram
        :return: NoneType
        """

        # Логирование ↓
        self.__logger.info(Text.pollingStartedLog)
        await self.__dispatcher.start_polling(self)  # запуск бесконечного ожидания
    # --------------------------------------------- #

    # --------- Хэндлеры бота USEBot: Commands ---------- #
    async def __startCommandHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка команды /start
        :param message: aiogram.types.Message
        :return: NoneType
        """

        pass

    # --------------------------------------------------- #

    # --------- Хэндлеры бота USEBot: CallbackQuery ---------- #
    # -------------------------------------------------------- #

    # ---------- Хэндлеры бота USEBot: PreCheckoutQuery ---------- #
    # ------------------------------------------------------------ #

    # ---------- Хэндлеры бота USEBot: SuccessfulPayment ---------- #
    # ------------------------------------------------------------- #

    # ---------- Хэндлеры бота USEBot: Message ---------- #
    # --------------------------------------------------- #
