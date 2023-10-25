import typing

import pytest
from bot.game import saper_game


@pytest.mark.parametrize('mode', [
    (0, [8, 8, 6, 3]),
    (1, [10, 8, 12, 2]),
    (2, [10, 8, 12, 1]),
    (3, [11, 8, 30, 1])
])
def test_game_creation(mode: typing.Tuple[int, typing.List[int]]):
    g = saper_game.create_game(mode[0])
    e_r, e_c, e_ex, e_lives = mode[1]
    assert len(g.grid) == len(g.public_grid) == e_r
    assert len(g.grid[0]) == len(g.public_grid[0]) == e_c
    assert g.config.explosives_count == e_ex
    assert g.config.lives == e_lives
