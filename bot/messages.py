import abc
import typing

from bot.game import saper_game
from bot import additional_classes


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def choose_difficulty(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def play(self, g: saper_game.Game, event: saper_game.Event = saper_game.Event("Good Luck!")) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def play_result(self, g: saper_game.Game, event: saper_game.Event, field: str) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def profile_menu(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def language_menu(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def language_changed(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def statistics_menu(self, user: additional_classes.User) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def leaderboard_menu(self, users: typing.List[additional_classes.User], cur_user: additional_classes.User) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def game_history(self, g: saper_game.Game, field: str) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def no_games_yet(self) -> str:
        raise NotImplemented


class EnglishMessage(BaseMessages):
    def play(self, g: saper_game.Game, event: saper_game.Event = saper_game.Event("Good Luck!")) -> str:
        return f"{event.msg}\nCurrent score: {g.score}"

    def start(self) -> str:
        return "Hi! Send me /play to play."

    def play_result(self, g: saper_game.Game, event: saper_game.Event, field: str) -> str:
        return f"{event.msg}\nScore: {g.score}\nGame Field: \n{field}"

    def choose_difficulty(self) -> str:
        return f"Choose difficulty level."

    def profile_menu(self) -> str:
        return f"Here you can manage your profile."

    def language_menu(self) -> str:
        return f"Choose prefered language."

    def language_changed(self) -> str:
        return f"Language was changed successfuly."

    def statistics_menu(self, user: additional_classes.User) -> str:
        wictory_percentage = f'{round((user.winned_games / user.games_played) * 100, 2)}%' \
            if user.games_played > 0 else 'no games yet'
        return f"{user.tg_user.first_name if user.tg_user.first_name else user.tg_user.id}\n" \
               f"Games played: {user.games_played}\n" \
               f"Maximum score: {user.max_score}\n" \
               f"Victories: {user.winned_games}\n" \
               f"Wictory percentage: {wictory_percentage}"

    def leaderboard_menu(self, users: typing.List[additional_classes.User], cur_user: additional_classes.User) -> str:
        sorted_users = sorted(users, key=lambda u: u.max_score, reverse=True)
        rating = "Current Leaderboard.\n"
        cur_user_position = sorted_users.index(cur_user)
        for i in range(min(len(sorted_users), 10)):
            user = sorted_users[i]
            row = f"{i + 1}. {user.tg_user.first_name if user.tg_user.first_name else user.tg_user.id} - " \
                  f"{user.max_score} points"
            if i == cur_user_position:
                row += ' (you)'
            rating += row + '\n'
        if cur_user_position >= 10:
            rating += f"...\n{cur_user_position + 1}. " \
                      f"{cur_user.tg_user.first_name if cur_user.tg_user.first_name else cur_user.tg_user.id}" \
                      f" = {cur_user.max_score} points"
        return rating

    def game_history(self, g: saper_game.Game, field: str) -> str:
        return f"Game History.\n{'Win' if g.config.lives > 0 else 'Defeat'}\nScore: {g.score}\n{field}"

    def no_games_yet(self) -> str:
        return "No games yet. Start playing."


class RussianMessage(BaseMessages):
    def play(self, g: saper_game.Game, event: saper_game.Event = saper_game.Event("Good Luck!")) -> str:
        match event.status_code:
            case 1:
                event_text = "Поздравляю! Вы победили!"
            case 2:
                event_text = "Отлично! Здесь бомбы нет!"
            case 3:
                event_text = "Эта клетка уже открыта."
            case 4:
                event_text = f"Буууум! У вас осталось {g.config.lives} жизней!"
            case 5:
                event_text = "Вы проиграли..."
            case _:
                event_text = "Удачи!"
        return f"{event_text}\nТекущий счет: {g.score}"

    def start(self) -> str:
        return "Привет! Отправь мне /play, чтобы начать игру."

    def play_result(self, g: saper_game.Game, event: saper_game.Event, field: str) -> str:
        match event.status_code:
            case 1:
                event_text = "Поздравляю! Вы победили!"
            case 5:
                event_text = "Вы проиграли..."
            case _:
                event_text = "Игра завершена"

        return f"{event_text}\nСчет: {g.score}\nИгровое поле: \n{field}"

    def choose_difficulty(self) -> str:
        return f"Выберите уровень сложности."

    def profile_menu(self) -> str:
        return f"Здесь Вы можете управлять профилем."

    def language_menu(self) -> str:
        return f"Выберите язык."

    def language_changed(self) -> str:
        return f"Язык изменен успешно."

    def statistics_menu(self, user: additional_classes.User) -> str:
        wictory_percentage = f'{round((user.winned_games / user.games_played) * 100, 2)}%' \
            if user.games_played > 0 else 'игр нет'
        return f"{user.tg_user.first_name if user.tg_user.first_name else user.tg_user.id}\n" \
               f"Игр всего: {user.games_played}\n" \
               f"Максимальный счет: {user.max_score}\n" \
               f"Побед: {user.winned_games}\n" \
               f"Процент побед: {wictory_percentage}"

    def leaderboard_menu(self, users: typing.List[additional_classes.User], cur_user: additional_classes.User) -> str:
        sorted_users = sorted(users, key=lambda u: u.max_score, reverse=True)
        rating = "Текущий Рейтинг.\n"
        cur_user_position = sorted_users.index(cur_user)
        for i in range(min(len(sorted_users), 10)):
            user = sorted_users[i]
            row = f"{i + 1}. {user.tg_user.first_name if user.tg_user.first_name else user.tg_user.id} - " \
                  f"{user.max_score} очков\n"
            if i == cur_user_position:
                row += ' (Вы)'
            rating += row + '\n'
        if cur_user_position >= 10:
            rating += f"...\n{cur_user_position + 1}. " \
                      f"{cur_user.tg_user.first_name if cur_user.tg_user.first_name else cur_user.tg_user.id}" \
                      f" = {cur_user.max_score} очков"
        return rating

    def game_history(self, g: saper_game.Game, field: str) -> str:
        return f"История игр.\n{'Победа' if g.config.lives > 0 else 'Поражение'}\nСчет: {g.score}\n{field}"

    def no_games_yet(self) -> str:
        return "Игр пока нет. Начните новую игру."


def get_language(user: additional_classes.User):
    match user.prefered_language:
        case "ru":
            return RussianMessage()
        case _:
            return EnglishMessage()
