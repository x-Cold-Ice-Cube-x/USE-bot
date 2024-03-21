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
    __users = None  # тип: UsersTable (обеспечить единственность объекта)
    __dispatcher = None  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __parser = None
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)

    # ---------------------------------------- #

    # ---------- Конструктор класса USEBot ---------- #
    def __init__(self):
        self.__setBasicConfig()  # создание объекта Logger (заранее, потому что дальше идет инициализация объектов)
        self.__setAttributes()  # заполнение всех полей класса
        super().__init__(token=self.__auth.getTelegramToken())  # авторизация бота в Telegram

        # Подключение хэндлера команды /start ↓
        self.__dispatcher.message.register(self.__startCommandHandler, CommandStart())

        # Подключение хэндлера кнопки startPracticeButton ↓
        self.__dispatcher.callback_query.register(self.__startPracticeHandler, F.data == Text.startPracticeButton[1],
                                                  RegistrationFilter(users=self.__users))

        # Подключение хэндлера кнопки stopPracticeButton ↓
        self.__dispatcher.callback_query.register(self.__stopPracticeHandler, States.practiceState,
                                                  F.data == Text.stopPracticeButton[1],
                                                  RegistrationFilter(users=self.__users))

        # Подключение хэндлера практики ↓
        self.__dispatcher.callback_query.register(self.__practiceHandler, States.practiceState,
                                                  RegistrationFilter(users=self.__users))

        # Подключение хэндлера кнопки profileButton ↓
        self.__dispatcher.callback_query.register(self.__profileHandler, F.data == Text.profileButton[1],
                                                  RegistrationFilter(users=self.__users))

        # Подключение хэндлера кнопки toMainMenuButton ↓
        self.__dispatcher.callback_query.register(self.__toMainMenuHandler, F.data == Text.toMainMenuButton[1],
                                                  RegistrationFilter(users=self.__users))

        # Подключение хэндлера кнопки leaderboardButton ↓
        self.__dispatcher.callback_query.register(self.__leaderboardHandler, F.data == Text.leaderboardButton[1],
                                                  RegistrationFilter(users=self.__users))

        # Подключение хэндлера неизвестных сообщений ↓
        self.__dispatcher.message.register(self.__unknownMessageHandler,
                                           RegistrationFilter(users=self.__users))

        # Подключение хэндлера незарегистрированных пользователей ↓
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
        cls.__users = UsersTable()  # заполнение поля класса __users
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

        # Если пользователя нет в базе данных ↓
        if message.chat.id not in self.__users.getDataFromColumn(columnName=self.__users.TELEGRAM_ID):
            # Заполнение таблицы данными о новом пользователе ↓
            self.__users.fillingTheTable(telegramID=message.chat.id, username=message.chat.username,
                                         firstName=message.chat.first_name)
        # Отправка сообщения startCommandMessage ↓
        await self.send_message(chat_id=message.chat.id, text=Text.startCommandMessage.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.startMarkup)

    # --------------------------------------------------- #

    # --------- Хэндлеры бота USEBot: CallbackQuery ---------- #
    async def __startPracticeHandler(self, call: CallbackQuery, state: FSMContext) -> None:
        """
        Метод-хэндлер: обработка кнопки startPracticeButton
        :param call: aiogram.types.CallbackQuery
        :param state: aiogram.fsm.context.FSMContext
        :return: NoneType
        """

        sample, solution = self.__parser.getRandomSample()  # получение случайного примера

        # Отправка сообщения practiceMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.practiceMessage.format(call.message.chat.first_name, sample, 0),
                                     message_id=call.message.message_id,
                                     parse_mode="HTML", reply_markup=Markup.getPracticeMarkup(sample))

        # Установка состояния States.practiceState, заполнение state.data ↓
        await state.set_state(States.practiceState)
        await state.update_data({"count": 0, "solution": solution})

    async def __practiceHandler(self, call: CallbackQuery, state: FSMContext) -> None:
        """
        Метод-хэндлер: обработка состояния States.practiceState
        :param call: aiogram.types.CallbackQuery
        :param state: aiogram.fsm.context.FSMContext
        :return: NoneType
        """

        stateData = await state.get_data()  # получение state.data
        sample, solution = self.__parser.getRandomSample()  # получение случайного примера

        # Если ответ некорректен ↓
        if not stateData["solution"].startswith(call.data.lower()):
            # Отправка сообщения practiceMistakeMessage ↓
            await self.edit_message_text(chat_id=call.message.chat.id,
                                         text=Text.practiceMistakeMessage.format(call.message.chat.first_name,
                                                                                 stateData["solution"],
                                                                                 call.message.chat.first_name, sample,
                                                                                 0),
                                         parse_mode="HTML", reply_markup=Markup.getPracticeMarkup(sample),
                                         message_id=call.message.message_id)

            # Импортирование из базы данных ошибок пользователя ↓
            mistakes = dict(loads(
                str(self.__users.getDataFromField(lineData=call.message.chat.id, columnName=self.__users.MISTAKES))))
            # Если ошибка в данном слове не первая ↓
            if stateData["solution"] in list(mistakes.keys()):
                mistakes[stateData["solution"]] = mistakes[stateData["solution"]] + 1  # увеличение счетчика ошибки
            else:
                mistakes[stateData["solution"]] = 1  # создание новой ошибки
            # Обновление ошибок пользователя ↓
            self.__users.updateField(lineData=call.message.chat.id, columnName=self.__users.MISTAKES,
                                     field=dumps(mistakes, ensure_ascii=False))

            # Если конкретный результат больше лучшего результата ↓
            if stateData["count"] > self.__users.getDataFromField(lineData=call.message.chat.id,
                                                                  columnName=self.__users.COUNT):
                # Обновление лучшего результата ↓
                self.__users.updateField(lineData=call.message.chat.id, columnName=self.__users.COUNT,
                                         field=stateData["count"])
            # Обновление state.data ↓
            await state.update_data({"count": 0, "solution": solution})
            return

        # Отправка сообщения practiceMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.practiceMessage.format(call.message.chat.first_name, sample,
                                                                      stateData["count"] + 1),
                                     message_id=call.message.message_id,
                                     parse_mode="HTML", reply_markup=Markup.getPracticeMarkup(sample))
        # Обновление state.data ↓
        await state.update_data({"count": stateData["count"] + 1, "solution": solution})

    async def __profileHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопки profileButton
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        mistakesMassage = ""  # создание сборника ошибок
        # Импорт ошибок из базы данных ↓
        mistakes = dict(loads(str(self.__users.getDataFromField(lineData=call.message.chat.id,
                                                                columnName=self.__users.MISTAKES)))).items()
        for word, count in mistakes:
            mistakesMassage += f"\n{word} - <b>[{count}]</b>"  # добавление ошибки из базы данных в сборник

        # Отправка сообщения profileMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.profileMessage.format(call.message.chat.first_name,
                                                                     self.__users.getDataFromField(
                                                                         lineData=call.message.chat.id,
                                                                         columnName=self.__users.COUNT),
                                                                     self.__users.getRank(
                                                                         telegram_id=call.message.chat.id),
                                                                     mistakesMassage),
                                     parse_mode="HTML", message_id=call.message.message_id,
                                     reply_markup=Markup.toMainMenuMarkup)

    async def __leaderboardHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопки leaderboardButton
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        leaderboard = self.__users.getLeaderboard()  # импорт лидерборда
        leaderboardMessage = ""  # создание сборника пользователей

        for user in leaderboard:
            leaderboardMessage += f"\n{user[0]} - <b>[{user[1]}]</b>"  # добавление пользователя в сборник
            if leaderboard.index(user) == 19:  # ограничение по пользователям - 20
                break

        # Отправка сообщения leaderboardMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.leaderboardMessage.format(leaderboardMessage, self.__users.getRank(
                                         telegram_id=call.message.chat.id)),
                                     parse_mode="HTML", message_id=call.message.message_id,
                                     reply_markup=Markup.toMainMenuMarkup)

    async def __toMainMenuHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопки toMainMenuButton
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        # Отправка сообщения startCommandMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.startCommandMessage.format(call.message.chat.first_name),
                                     message_id=call.message.message_id,
                                     parse_mode="HTML", reply_markup=Markup.startMarkup)

    async def __stopPracticeHandler(self, call: CallbackQuery, state: FSMContext) -> None:
        """
        Метод-хэндлер: обработка кнопки stopPracticeButton
        :param call: aiogram.types.CallbackQuery
        :param state: aiogram.fsm.context.FSMContext
        :return: NoneType
        """

        stateData = await state.get_data()  # получение state.data

        # Отправка сообщения startCommandMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id,
                                     text=Text.startCommandMessage.format(call.message.chat.first_name),
                                     message_id=call.message.message_id,
                                     parse_mode="HTML", reply_markup=Markup.startMarkup)

        # Если конкретный результат больше лучшего результата ↓
        if stateData["count"] > self.__users.getDataFromField(lineData=call.message.chat.id,
                                                              columnName=self.__users.COUNT):
            # Обновление лучшего результата ↓
            self.__users.updateField(lineData=call.message.chat.id, columnName=self.__users.COUNT,
                                     field=stateData["count"])
        await state.clear()  # удаление состояния

    async def __unregisteredCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка незарегистрированного пользователя
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        # Отправка сообщения unregisteredMessage ↓
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

        # Отправка сообщения unregisteredMessage ↓
        await self.send_message(chat_id=message.chat.id,
                                text=Text.unregisteredMessage.format(message.chat.first_name),
                                parse_mode="HTML")

    async def __unknownMessageHandler(self, message: Message) -> None:
        """
        Метод-хэндлера: обработка неизвестных сообщений
        :param message: aiogram.types.Message
        :return: NoneType
        """

        # Отправка сообщения unknownMessage ↓
        await self.send_message(chat_id=message.chat.id,
                                text=Text.unknownMessage.format(message.chat.first_name, message.text),
                                parse_mode="HTML")
    # --------------------------------------------------- #
