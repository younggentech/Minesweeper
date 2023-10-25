import abc

from bot import additional_classes


class BaseKeyboardButtonsTexts(abc.ABC):
    @abc.abstractmethod
    def main_menu(self):
        raise NotImplemented

    @abc.abstractmethod
    def play(self):
        raise NotImplemented

    @abc.abstractmethod
    def profile(self):
        raise NotImplemented

    @abc.abstractmethod
    def language(self):
        raise NotImplemented

    @abc.abstractmethod
    def statistics(self):
        raise NotImplemented

    @abc.abstractmethod
    def game_history(self):
        raise NotImplemented

    @abc.abstractmethod
    def leaderboard(self):
        raise NotImplemented


class EnglishKeyboardButtonsTexts(BaseKeyboardButtonsTexts):
    def main_menu(self):
        return ["Play", "Profile", "Statistics", "Leaderboard"]

    def play(self):
        return ["Easy", "Medium", "Hard", "Impossible", "Main Menu"]

    def profile(self):
        return ["Language", "Main Menu"]

    def language(self):
        return ["English", "Russian"]

    def statistics(self):
        return ["Game History", "Main Menu"]

    def game_history(self):
        return ["Previous", "Next", "Main Menu"]

    def leaderboard(self):
        return ["Main Menu"]


class RussianKeyboardButtonsTexts(BaseKeyboardButtonsTexts):
    def main_menu(self):
        return ["Играть", "Профиль", "Статистика", "Рейтинг игроков"]

    def play(self):
        return ["Легко", "Средне", "Сложно", "Невозможно", "Главное Меню"]

    def profile(self):
        return ["Язык", "Главное Меню"]

    def language(self):
        return ["Английский", "Русский"]

    def statistics(self):
        return ["История Игр", "Главное Меню"]

    def game_history(self):
        return ["Назад", "Вперед", "Главное Меню"]

    def leaderboard(self):
        return ["Главное Меню"]


def get_keyboard_buttons_texts(user: additional_classes.User):
    match user.prefered_language:
        case "ru":
            return RussianKeyboardButtonsTexts()
        case _:
            return EnglishKeyboardButtonsTexts()
