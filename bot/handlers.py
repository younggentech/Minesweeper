import abc
import logging
import typing

import aiogram
import aiogram.types.inline_keyboard

from bot.game import saper_game
from bot import keyboard_generator, messages, additional_classes, button_texts


def load_context():
    global ustorage, gstorage, user_to_game, users
    gstorage = additional_classes.Storage("games.pickle")
    user_to_game = gstorage.load()
    ustorage = additional_classes.Storage("users.pickle")
    users = ustorage.load()


def close_context():
    global ustorage, users
    ustorage.close()
    gstorage.close()


class BaseHandler(abc.ABC):
    def __init__(self):
        self.user: typing.Optional[additional_classes.User] = None
        self.reply_messages: typing.Optional[messages.BaseMessages] = None
        self.keyboard_buttons: typing.Optional[button_texts.BaseKeyboardButtonsTexts] = None

    async def __call__(self, event: aiogram.types.Message | aiogram.types.CallbackQuery):
        if event.from_user.id not in users:
            users[event.from_user.id] = additional_classes.User(tg_user=event.from_user)
        self.user = users[event.from_user.id]
        self.reply_messages = messages.get_language(self.user)
        self.keyboard_buttons = button_texts.get_keyboard_buttons_texts(self.user)
        await self.handle(event)

    @abc.abstractmethod
    async def handle(self, event: aiogram.types.Message | aiogram.types.CallbackQuery):
        raise NotImplemented


class StartMessageHandler(BaseHandler):
    async def handle(self, message: aiogram.types.Message):
        keyboard = keyboard_generator.RenderInitialMenu()
        await message.answer(self.reply_messages.start(), reply_markup=keyboard(self.keyboard_buttons))


class StartMessageInlineHandler(BaseHandler):
    async def handle(self, event: aiogram.types.CallbackQuery):
        keyboard = keyboard_generator.RenderInitialMenu()
        await event.message.edit_text(self.reply_messages.start())
        await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))


class MainMenuHandler(BaseHandler):
    async def handle(self, event: aiogram.types.CallbackQuery):
        match event.data.split(".")[1]:
            case "play":
                keyboard = keyboard_generator.RenderPlayMenu()
                await event.message.edit_text(self.reply_messages.choose_difficulty())
                await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))
            case "profile":
                keyboard = keyboard_generator.RenderProfileMenu()
                await event.message.edit_text(self.reply_messages.profile_menu())
                await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))
            case "statistics":
                keyboard = keyboard_generator.RenderStatisticsMenu()
                await event.message.edit_text(self.reply_messages.statistics_menu(self.user))
                await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))
            case "leaderboard":
                keyboard = keyboard_generator.RenderLeaderBoardMenu()
                await event.message.edit_text(self.reply_messages.leaderboard_menu(list(users.values()), self.user))
                await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))


class ProfileMenuHandler(BaseHandler):
    async def handle(self, event: aiogram.types.CallbackQuery):
        match event.data.split(".")[1]:
            case "language":
                keyboard = keyboard_generator.RenderLanguageMenu()
                await event.message.edit_text(self.reply_messages.language_menu())
                await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))


class LanguageMenuHandler(BaseHandler):
    async def handle(self, event: aiogram.types.CallbackQuery):
        lang = event.data.split(".")[1]
        self.user.prefered_language = lang
        users[event.from_user.id] = self.user
        self.reply_messages = messages.get_language(self.user)
        self.keyboard_buttons = button_texts.get_keyboard_buttons_texts(self.user)
        keyboard = keyboard_generator.RenderProfileMenu()
        await event.message.edit_text(self.reply_messages.language_changed())
        await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))


class StatisticsMenuHandler(BaseHandler):
    async def handle(self, event: aiogram.types.CallbackQuery):
        match event.data.split(".")[1]:
            case "hist":
                keyboard = keyboard_generator.RenderGameHistoryMenu()
                # we go from last(-1) to first(-len(v)-1) elements in inverse order
                if len(self.user.game_history) > 0:
                    await event.message.edit_text(self.reply_messages.game_history(
                        g=self.user.game_history[-1],
                        field=keyboard_generator.render_final_field(self.user.game_history[-1])))
                    await event.message.edit_reply_markup(keyboard(self.keyboard_buttons))
                else:
                    await event.message.edit_text(self.reply_messages.no_games_yet())


class GameHistMenuHandler(BaseHandler):
    async def handle(self, event: aiogram.types.CallbackQuery):
        # we go from last(-1) to first(-len(v)-1) elements in inverse order
        idx = int(event.data.split(".")[1])
        # check that element with idx exists
        if idx > -1 or idx < -len(self.user.game_history) - 1 or -idx > len(self.user.game_history):
            return
        await event.message.edit_text(self.reply_messages.game_history(
            g=self.user.game_history[idx],
            field=keyboard_generator.render_final_field(self.user.game_history[idx])))
        keyboard = keyboard_generator.RenderGameHistoryMenu()
        await event.message.edit_reply_markup(keyboard(self.keyboard_buttons, prev=idx-1, nxt=idx+1))


class PlayHandler(BaseHandler):
    async def handle(self, event: aiogram.types.Message | aiogram.types.CallbackQuery):
        if isinstance(event, aiogram.types.Message):
            g = saper_game.create_game()
        elif isinstance(event, aiogram.types.CallbackQuery):
            g = saper_game.create_game(int(event.data.split(".")[1]))
        else:
            raise TypeError("Event should be either Message, or CallbackQuery")
        user_to_game[event.from_user.id] = g
        logging.log(msg=f"player: {event.from_user.id}; game: {g}", level=logging.INFO)
        keyboard = keyboard_generator.RenderInlineGameKeyboard()(self.keyboard_buttons, g)
        if isinstance(event, aiogram.types.Message):
            await event.answer(self.reply_messages.play(g), reply_markup=keyboard)
        elif isinstance(event, aiogram.types.CallbackQuery):
            await event.message.edit_text(self.reply_messages.play(g))
            await event.message.edit_reply_markup(keyboard)


class GameCallBackHandler(BaseHandler):
    async def handle(self, callback_query: aiogram.types.CallbackQuery):
        g = user_to_game[callback_query.from_user.id]
        if g is None:
            return
        try:
            x, y = map(int, callback_query.data.split(".")[1:])
        except TypeError:
            await callback_query.answer("Unable to process")
            return
        event = g.reveal_coordinate(x, y)
        if event.game_over:
            final_field = keyboard_generator.render_final_field(user_to_game[self.user.tg_user.id])
            await callback_query.message.edit_text(
                self.reply_messages.play_result(user_to_game[self.user.tg_user.id], event, final_field)
            )
            self.user.max_score = max(self.user.max_score, g.score)
            self.user.games_played += 1
            self.user.game_history.append(g)
            if event.status_code == 1:
                self.user.winned_games += 1
            user_to_game[callback_query.from_user.id] = None
            keyboard = keyboard_generator.RenderInitialMenu()
            await callback_query.message.edit_reply_markup(keyboard(self.keyboard_buttons))
            return
        user_to_game[callback_query.from_user.id] = g
        logging.log(msg=f"player: {callback_query.from_user.id}; game: {g}; event: {event}", level=logging.INFO)
        keyboard = keyboard_generator.RenderInlineGameKeyboard()(self.keyboard_buttons, g)
        await callback_query.message.edit_text(self.reply_messages.play(g, event))
        await callback_query.message.edit_reply_markup(keyboard)


def setup_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(StartMessageHandler(), commands=['start'])
    dp.register_callback_query_handler(StartMessageInlineHandler(), lambda x: x.data.lower() == "main_menu")

    dp.register_callback_query_handler(MainMenuHandler(), lambda x: x.data.lower().startswith("main"))

    dp.register_callback_query_handler(ProfileMenuHandler(), lambda x: x.data.lower().startswith("profile"))

    dp.register_callback_query_handler(LanguageMenuHandler(), lambda x: x.data.lower().startswith("language"))

    dp.register_callback_query_handler(StatisticsMenuHandler(), lambda x: x.data.lower().startswith("statistics"))

    dp.register_callback_query_handler(GameHistMenuHandler(), lambda x: x.data.lower().startswith("hist"))

    dp.register_message_handler(PlayHandler(), commands=['play'])
    dp.register_callback_query_handler(PlayHandler(), lambda x: x.data.lower().startswith("play"))

    dp.register_callback_query_handler(GameCallBackHandler(), lambda x: x.data.startswith("g"))
