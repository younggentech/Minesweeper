import abc

import aiogram.types.inline_keyboard

from bot import button_texts
from bot.game import saper_game
grid_to_emoji = {
    "*": "❔",
    "b": "💣",
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
}


def render_final_field(g: saper_game.Game):
    field = ""
    for row in range(g.config.rows):
        one_row = []
        for col in range(g.config.cols):
            text_value = grid_to_emoji.get(g.public_grid[row][col], g.public_grid[row][col])
            one_row.append(text_value)
        field += "".join(one_row)
        field += "\n"
    return field


class RenderBaseKeyboard(abc.ABC):
    def __call__(self, keyboard_button_text: button_texts.BaseKeyboardButtonsTexts, *args, **kwargs):
        self.keyboard_button_text = keyboard_button_text
        return self.render(*args, **kwargs)

    @abc.abstractmethod
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        raise NotImplemented


class RenderInlineGameKeyboard(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        """
        Important: g: saper_game.Game - mandatory param
        """
        g: saper_game.Game = args[0] if len(args) > 0 else kwargs["g"]
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(row_width=g.config.rows)
        for row in range(g.config.rows):
            one_row = []
            for col in range(g.config.cols):
                text_value = grid_to_emoji.get(g.public_grid[row][col], g.public_grid[row][col])
                button = aiogram.types.inline_keyboard.InlineKeyboardButton(text=text_value,
                                                                            callback_data=f"g.{row}.{col}")
                one_row.append(button)
            keyboard.row(*one_row)
        return keyboard


class RenderInitialMenu(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(3)
        texts = self.keyboard_button_text.main_menu()
        play = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[0], callback_data=f"main.play")
        profile = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[1], callback_data=f"main.profile")
        statistics = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[2], callback_data=f"main.statistics")
        leaderboard = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[3],
                                                                         callback_data=f"main.leaderboard")
        keyboard.add(play, profile, statistics)
        keyboard.add(leaderboard)
        return keyboard


class RenderPlayMenu(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(3)
        texts = self.keyboard_button_text.play()
        for i in range(len(texts) - 1):
            button = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[i], callback_data=f"play.{i}")
            keyboard.add(button)
        main_menu = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[-1], callback_data="main_menu")
        keyboard.add(main_menu)
        return keyboard


class RenderProfileMenu(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(3)
        texts = self.keyboard_button_text.profile()
        play = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[0], callback_data=f"profile.language")
        main_menu = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[-1], callback_data="main_menu")
        keyboard.add(play)
        keyboard.add(main_menu)
        return keyboard


class RenderLanguageMenu(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(3)
        texts = self.keyboard_button_text.language()
        english = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[0], callback_data=f"language.en")
        russian = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[1], callback_data=f"language.ru")
        keyboard.add(english, russian)
        return keyboard


class RenderStatisticsMenu(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(3)
        texts = self.keyboard_button_text.statistics()
        game_hist = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[0], callback_data=f"statistics.hist")
        main_menu = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[-1], callback_data="main_menu")
        keyboard.add(game_hist)
        keyboard.add(main_menu)
        return keyboard


class RenderGameHistoryMenu(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        prev: int = args[0] if len(args) > 0 else kwargs.get("prev")
        nxt: int = args[0] if len(args) > 0 else kwargs.get("nxt")
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(3)
        texts = self.keyboard_button_text.game_history()
        # Callback data shows inverse indexing, we go from last(-1) to first(-len(v)-1) elements
        prv = aiogram.types.inline_keyboard.InlineKeyboardButton(
            text=texts[0],
            callback_data=f"hist.{prev if prev is not None else -2}"
        )
        nxt = aiogram.types.inline_keyboard.InlineKeyboardButton(
            text=texts[1],
            callback_data=f"hist.{nxt if nxt is not None else 0}"
        )
        main_menu = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[-1], callback_data="main_menu")
        keyboard.add(prv, nxt)
        keyboard.add(main_menu)
        return keyboard


class RenderLeaderBoardMenu(RenderBaseKeyboard):
    def render(self, *args, **kwargs) -> aiogram.types.inline_keyboard.InlineKeyboardMarkup:
        keyboard = aiogram.types.inline_keyboard.InlineKeyboardMarkup(3)
        texts = self.keyboard_button_text.leaderboard()
        main_menu = aiogram.types.inline_keyboard.InlineKeyboardButton(text=texts[-1], callback_data="main_menu")
        keyboard.add(main_menu)
        return keyboard
