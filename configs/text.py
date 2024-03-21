class Text:
    # ---------- Пути к файлам ---------- #
    logsFilepath = "databases/logs.log"
    databaseFilepath = "databases/bot_database.sqlite"

    samplesFilepath = "databases/tasks.json"
    # ----------------------------------- #

    # ---------- Протокольные сообщения ---------- #
    fillingTheTableAuthorizationLog = ("Таблица {} успешно обновлена. Старые данные удалены. Новые данные:"
                                       "{}: {}, {}: {}")

    fillingTheTableUsersLog = ("Таблица {} успешно обновлена. Заполнены данные о новом пользователе: "
                               "{}: {}")

    loggerConnectedLog = "Логгер успешно подключён."
    pollingStartedLog = "Поллинг бота успешно запущен."
    authorizationConnectedLog = "Класс Authorization успешно импортирован. Таблица Authorization подключена."
    usersConnectedLog = "Класс Users успешно импортирован. Таблица Users подключена."

    parsingTasksUrlsSuccessfulLog = "Ссылки на тесты успешно скопированы."
    parsingErrorLog = "Примеры из теста {} не были скопированы."
    parsingSuccessfulLog = "Примеры из теста {} были успешно скопированы."
    samplesSuccessfulSavedLog = "Примеры успешно сохранены по пути {}"

    # -------------------------------------------- #

    # ---------- ID групп, каналов и чатов ---------- #
    # ----------------------------------------------- #

    # ---------- Содержание кнопок ---------- #
    charsPracticeButtons = ("А", "О", "И", "Е", "Ы")
    startPracticeButton = ("Начать практику 🖊", "start_practice")
    stopPracticeButton = ("Закончить практику ⚙️", "stop_practice")
    toMainMenuButton = ("В главное меню ⚙️", "to_main_menu")
    profileButton = ("Мой профиль 💡", "profile")
    leaderboardButton = ("Рейтинг ⚙️", "leaderboard")
    # --------------------------------------- #

    # ---------- Команды бота ---------- #
    # ---------------------------------- #

    # ---------- Сообщения бота ---------- #
    startCommandMessage = "<b>{}</b>, выбери что-то из предложенных ниже кнопок ↓ ☺️"
    leaderboardMessage = ("Рейтинг ⚔️\n"
                            "{}\n"
                          "Ваше место в рейтинге: <b>[{}]</b>")
    profileMessage = ("👥 Имя: <b>{}</b>\n"
                      "📈 Лучший результат: <b>[{}]</b>\n"
                      "⚔️ Место в рейтинге: <b>[{}]</b>\n\n"
                      "👁 Ошибки: {}")
    practiceMessage = ("<b>{}</b>, выберите правильное написание слова 💡\n"
                       "Новый пример: <b>{}</b>\n"
                       "Ваш счётчик на этот момент: <b>{}</b>")
    practiceMistakeMessage = ("<b>{}</b>, Вы совершили ошибку: \n"
                              "Правило: <b>{}</b> ⚙️\n"
                              "<i>[где ЧГ - чередующаяся гласная, ПГ - проверяемая, а НГ - непроверяемая (словарное слово)]</i> ☺️\n\n" + practiceMessage)
    unknownMessage = "<b>{}</b>, я не знаю что ответить на: \n<i>{}</i> 😔"
    unregisteredMessage = "<b>{}</b>, чтобы пользоваться услугами бота, пропиши /start ⚙️"
    # ------------------------------------ #
