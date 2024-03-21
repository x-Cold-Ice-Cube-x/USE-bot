# ---------- Импорты дополнительных библиотек --------- #
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from configs.text import Text
# ---------------------------------------- #


class Markup:
    # ---------- Поля класса Markup: кнопки ---------- #
    __startPracticeButton = InlineKeyboardButton(text=Text.startPracticeButton[0], callback_data=Text.startPracticeButton[1])
    __stopPracticeButton = InlineKeyboardButton(text=Text.stopPracticeButton[0], callback_data=Text.stopPracticeButton[1])
    __leaderboardButton = InlineKeyboardButton(text=Text.leaderboardButton[0], callback_data=Text.leaderboardButton[1])
    __profileButton = InlineKeyboardButton(text=Text.profileButton[0], callback_data=Text.profileButton[1])
    __toMainMenuButton = InlineKeyboardButton(text=Text.toMainMenuButton[0], callback_data=Text.toMainMenuButton[1])
    # ------------------------------------------------ #

    # ---------- Поля класса Markup: разметки ---------- #
    __startMarkup = [[__profileButton, __leaderboardButton], [__startPracticeButton]]
    __toMainMenuKeyboard = [[__toMainMenuButton]]
    # -------------------------------------------------- #

    # ---------- Поля класса Markup: клавиатуры ---------- #
    startMarkup = InlineKeyboardMarkup(inline_keyboard=__startMarkup)
    toMainMenuMarkup = InlineKeyboardMarkup(inline_keyboard=__toMainMenuKeyboard)
    # ----------------------------------------------------- #

    @classmethod
    def getPracticeMarkup(cls, sample: str) -> InlineKeyboardMarkup:
        """
        Метод, возвращающий клавиатуру практики
        :param sample: пример
        :return: aiogram.types.InlineKeyboardMarkup
        """

        solutions = [sample.replace("..", char, 1) for char in Text.charsPracticeButtons]
        practiceKeyboard = [[InlineKeyboardButton(text=f"{solution} 💡", callback_data=f"{solution}") for solution in solutions[0:3]],
                            [InlineKeyboardButton(text=f"{solution} 💡", callback_data=f"{solution}") for solution in solutions[3::]],
                            [cls.__stopPracticeButton]]
        return InlineKeyboardMarkup(inline_keyboard=practiceKeyboard)

