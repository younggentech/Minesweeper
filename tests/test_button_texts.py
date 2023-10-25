from unittest.mock import MagicMock
import pytest
import bot.button_texts as but_texts


@pytest.mark.parametrize('method',
                         ['main_menu', 'play', 'profile', 'language', 'statistics', 'game_history', 'leaderboard'])
@pytest.mark.parametrize('lang', ['ru', 'en'])
def test_game_creation(lang: str, method: str):
    user_mock = MagicMock()
    user_mock.return_value(lang)
    text_generator = but_texts.get_keyboard_buttons_texts(user_mock)
    result = getattr(text_generator, method)()
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
