# --------- Импорты встроенных библиотек --------- #
from logging import getLogger, INFO, basicConfig
from json import dumps, loads
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.authorization_table import AuthorizationTable
from tables.users_table import UsersTable
from configs.text import Text
from bot.markup.markup import Markup
from parser.parser import Parser
from bot.states.states import States
from bot.filters.registration_filter import RegistrationFilter


# ---------------------------------------- #


class USEBot(Bot):
    # ---------- Поля класса USEBot ---------- #
    __auth = None  # тип: AuthorizationTable (обеспечить единственность объекта)
    __users = None
    __dispatcher = None  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __parser = None
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)

    # ---------------------------------------- #

    # ---------- Конструктор класса USEBot ---------- #
    def __init__(self):
        self.__setBasicConfig()  # создание объекта Logger (заранее, потому что дальше идет инициализация объектов)
        self.__setAttributes()  # заполнение всех полей класса
        super().__init__(token=self.__auth.getTelegramToken())  # авторизация бота в Telegram

        self.__dispatcher.message.register(self.__startCommandHandler, CommandStart())
        self.__dispatcher.callback_query.register(self.__startPracticeHandler, F.data == Text.startPracticeButton[1],
                                                  RegistrationFilter(users=self.__users))
        self.__dispatcher.callback_query.register(self.__practiceHandler, States.practiceState,
                                                  RegistrationFilter(users=self.__users))
        self.__dispatcher.callback_query.register(self.__profileHandler, F.data == Text.profileButton[1],
                                                  RegistrationFilter(users=self.__users))
        self.__dispatcher.callback_query.register(self.__toMainMenuHandler, F.data == Text.toMainMenuButton[1],
                                                  RegistrationFilter(users=self.__users))
        self.__dispatcher.callback_query.register(self.__leaderboardHandler, F.data == Text.leaderboardButton[1],
                                                  RegistrationFilter(users=self.__users))

        self.__dispatcher.message.register(self.__unknownMessageHandler,
                                           RegistrationFilter(users=self.__users))
        self.__dispatcher.message.register(self.__unregisteredMessageHandler)
        self.__dispatcher.callback_query.register(self.__unregisteredCallbackHandler)

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

        cls.__parser = Parser(samplesFilepath=Text.samplesFilepath)
        cls.__auth = AuthorizationTable()  # заполнение поля класса __authorization
        cls.__users = UsersTable()
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
        if message.chat.id not in self.__users.getDataFromColumn(columnName=self.__users.TELEGRAM_ID):
            self.__users.fillingTheTable(telegramID=message.chat.id, username=message.chat.username,
                                         firstName=message.chat.first_name)

        await self.send_message(chat_id=message.chat.id, text=Text.startCommandMessage.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.startMarkup)

    # --------------------------------------------------- #

    # --------- Хэндлеры бота USEBot: CallbackQuery ---------- #
    async def __startPracticeHandler(self, call: CallbackQuery, state: FSMContext):
        sample, solution = self.__parser.getRandomSample()
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.practiceMessage.format(call.message.chat.first_name, sample, 0),
                                     message_id=call.message.message_id,
                                     parse_mode="HTML", reply_markup=Markup.getPracticeMarkup(sample))

        await state.set_state(States.practiceState)
        await state.update_data({"count": 0, "solution": solution})

    async def __practiceHandler(self, call: CallbackQuery, state: FSMContext):
        stateData = await state.get_data()
        if call.data == "stop_practice":
            await self.edit_message_text(chat_id=call.message.chat.id,
                                         text=Text.startCommandMessage.format(call.message.chat.first_name),
                                         message_id=call.message.message_id,
                                         parse_mode="HTML", reply_markup=Markup.startMarkup)
            if stateData["count"] > self.__users.getDataFromField(lineData=call.message.chat.id,
                                                                  columnName=self.__users.COUNT):
                self.__users.updateField(lineData=call.message.chat.id, columnName=self.__users.COUNT,
                                         field=stateData["count"])
            await state.clear()
            return

        sample, solution = self.__parser.getRandomSample()
        if not stateData["solution"].startswith(call.data.lower()):
            # окончание практики
            await self.edit_message_text(chat_id=call.message.chat.id,
                                         text=Text.practiceMistakeMessage.format(call.message.chat.first_name,
                                                                                 stateData["solution"],
                                                                                 call.message.chat.first_name, sample,
                                                                                 0),
                                         parse_mode="HTML", reply_markup=Markup.getPracticeMarkup(sample),
                                         message_id=call.message.message_id)

            mistakes = dict(loads(str(self.__users.getDataFromField(lineData=call.message.chat.id, columnName=self.__users.MISTAKES))))
            if stateData["solution"] in list(mistakes.keys()):
                mistakes[stateData["solution"]] = mistakes[stateData["solution"]] + 1
            else:
                mistakes[stateData["solution"]] = 1
            self.__users.updateField(lineData=call.message.chat.id, columnName=self.__users.MISTAKES, field=dumps(mistakes, ensure_ascii=False))

            if stateData["count"] > self.__users.getDataFromField(lineData=call.message.chat.id,
                                                                  columnName=self.__users.COUNT):
                self.__users.updateField(lineData=call.message.chat.id, columnName=self.__users.COUNT,
                                         field=stateData["count"])

            await state.update_data({"count": 0, "solution": solution})
            return

        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.practiceMessage.format(call.message.chat.first_name, sample,
                                                                      stateData["count"] + 1),
                                     message_id=call.message.message_id,
                                     parse_mode="HTML", reply_markup=Markup.getPracticeMarkup(sample))
        await state.update_data({"count": stateData["count"] + 1, "solution": solution})

    async def __profileHandler(self, call: CallbackQuery):
        mistakesMassage = ""
        for word, count in dict(loads(str(self.__users.getDataFromField(lineData=call.message.chat.id, columnName=self.__users.MISTAKES)))).items():
            mistakesMassage += f"\n{word} - <b>[{count}]</b>"
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.profileMessage.format(call.message.chat.first_name,
                                                                     self.__users.getDataFromField(
                                                                         lineData=call.message.chat.id,
                                                                         columnName=self.__users.COUNT),
                                                                     self.__users.getRank(
                                                                         telegram_id=call.message.chat.id), mistakesMassage),
                                     parse_mode="HTML", message_id=call.message.message_id,
                                     reply_markup=Markup.toMainMenuMarkup)

    async def __leaderboardHandler(self, call: CallbackQuery):
        leaderboard = self.__users.getLeaderboard()
        leaderboardMessage = ""

        for user in leaderboard:
            leaderboardMessage += f"\n{user[0]} - <b>[{user[1]}]</b>"
            if leaderboard.index(user) == 9:
                break

        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.leaderboardMessage.format(leaderboardMessage, self.__users.getRank(
                                         telegram_id=call.message.chat.id)),
                                     parse_mode="HTML", message_id=call.message.message_id,
                                     reply_markup=Markup.toMainMenuMarkup)

    async def __toMainMenuHandler(self, call: CallbackQuery):
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.startCommandMessage.format(call.message.chat.first_name),
                                     message_id=call.message.message_id,
                                     parse_mode="HTML", reply_markup=Markup.startMarkup)

    async def __unregisteredCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка незарегистрированного пользователя
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.unregisteredMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML")

    # -------------------------------------------------------- #

    # ---------- Хэндлеры бота USEBot: PreCheckoutQuery ---------- #
    # ------------------------------------------------------------ #

    # ---------- Хэндлеры бота USEBot: SuccessfulPayment ---------- #
    # ------------------------------------------------------------- #

    # ---------- Хэндлеры бота USEBot: Message ---------- #
    async def __unregisteredMessageHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка незарегистрированного пользователя
        :param message: aiogram.types.Message
        :return: NoneType
        """
        await self.send_message(chat_id=message.chat.id,
                                text=Text.unregisteredMessage.format(message.chat.first_name),
                                parse_mode="HTML")

    async def __unknownMessageHandler(self, message: Message) -> None:
        # Ответ ↓
        await self.send_message(chat_id=message.chat.id,
                                text=Text.unknownMessage.format(message.chat.first_name, message.text),
                                parse_mode="HTML")
    # --------------------------------------------------- #
