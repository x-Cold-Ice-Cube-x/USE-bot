# ---------- Импорты дополнительных библиотек --------- #
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.users_table import UsersTable
# ---------------------------------------- #


class RegistrationFilter(BaseFilter):
    # ---------- Конструктор класса RegistrationFilter ---------- #
    def __init__(self, users: UsersTable):
        """
        Конструктор класса RegistrationFilter: предобработка события, полученного ботом
        :param users: UsersTable (обеспечить единственность объекта)
        """

        # Добавление необходимых полей экземпляру для корректной работы фильтра ↓
        self.__users = users  # обеспечить единственность объекта
    # ----------------------------------------------------------- #

    # ---------- Переопределенный метод BaseFilter ---------- #
    async def __call__(self, response: CallbackQuery | Message) -> bool:
        """
        Переопределенный метод класса BaseFilter: предобработка события, полученного ботом
        :param response: aiogram.types.CallbackQuery | aiogram.types.Message
        :return: bool (True - есть в базе, False - нет в базе)
        """

        # Получение объекта aiogram.types.Message ↓
        if isinstance(response, CallbackQuery):
            message = response.message
        else:
            message = response

        # Проверка существования пользователя в базе данных ↓
        return message.chat.id in self.__users.getDataFromColumn(columnName=self.__users.TELEGRAM_ID)
    # ------------------------------------------------------- #
