import dataclasses
import typing
import dill

import aiogram


@dataclasses.dataclass
class User:
    tg_user: aiogram.types.user
    max_score: int = 0
    games_played: int = 0
    winned_games: int = 0
    game_history: typing.List = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.prefered_language: str = self.tg_user.language_code.lower()


class Storage:
    def __init__(self, path):
        self.path = path
        self.storage = {}

    def __enter__(self):
        return self.load()

    def __exit__(self, *args):
        self.close()

    def load(self):
        try:
            with open(self.path, "rb") as f:
                self.storage = dill.load(f)
        except FileNotFoundError:
            self.storage = {}
        return self.storage

    def close(self):
        with open(self.path, "wb") as f:
            dill.dump(self.storage, f)