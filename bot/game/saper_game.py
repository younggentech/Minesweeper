import dataclasses
import random
import typing


@dataclasses.dataclass
class Event:
    """
    Important information about game is stored here
    """
    msg: str
    game_over: bool = False
    status_code: int = 0
    opened_coordinates: typing.List = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class GameConfig:
    """
    Important information about game is stored here
    """
    rows: int
    cols: int
    explosives_count: int
    lives: int


class Game:
    def __init__(self, rows: int, cols: int, explosives_count: int, lives: int):
        if explosives_count <= lives:
            raise ValueError("Explosives should be less then lives")
        explosive_coordinates = self.generate_random_explosives(rows, cols, explosives_count)
        self.score = 0
        self.cells_opened = 0
        self.bombs_detonated = 0
        self.config = GameConfig(rows=rows, cols=cols, explosives_count=explosives_count, lives=lives)
        self.grid = self.generate_grid(rows, cols, explosive_coordinates)
        self.public_grid = self.generate_public_grid(rows, cols, self.grid)

    def reveal_coordinate(self, x: int, y: int):
        """
        Event status codes:
        1 - win
        2 - no bomb in cell
        3 - cell already opeded
        4 - bomb in cell
        5 - lose
        """
        if x < 0 or y < 0 or x > self.config.rows or y > self.config.cols:
            raise ValueError("Coordinates must be within grid")
        value = self.grid[x][y]
        if value != -1 and self.public_grid[x][y] != str(value):
            self.score = self.score + value + 1 + \
                         (value * ((self.config.explosives_count // (self.config.lives + 1)) - 1))
            self.public_grid[x][y] = str(value)
            self.cells_opened += 1
            if self.cells_opened >= self.config.rows * self.config.cols - self.config.explosives_count:
                return Event(msg="Congratulations! You won!", game_over=True, status_code=1, opened_coordinates=[x, y])
            return Event(msg="Great! No bomb here!", status_code=2, opened_coordinates=[x, y])
        elif self.public_grid[x][y] == str(value) or self.public_grid[x][y] == "b":
            return Event(msg="This cell was already opened", status_code=3, opened_coordinates=[x, y])
        else:
            self.config.lives -= 1
            self.bombs_detonated += 1
            self.public_grid[x][y] = "b"
            if self.config.lives <= 0 or self.bombs_detonated >= self.config.explosives_count:
                return Event(msg="Game Over...", game_over=True, status_code=5, opened_coordinates=[x, y])
            return Event(msg=f"Booom! You have {self.config.lives} lives left...", status_code=4, opened_coordinates=[x, y])

    def generate_public_grid(self, rows: int, cols: int,
                             grid: typing.List[typing.List[int]]) -> typing.List[typing.List[int]]:
        public_grid = [["*"] * cols for _ in range(rows)]
        x, y = random.randrange(0, rows), random.randrange(0, cols)
        c = 0
        for nx, ny in ((x - 1, y), (x + 1, y), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x, y - 1), (x, y + 1)):
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != -1:
                public_grid[nx][ny] = str(grid[nx][ny])
                c += 1
        self.cells_opened += c
        return public_grid

    @classmethod
    def generate_grid(cls, rows: int, cols: int,
                      explosive_coordinates: typing.List[typing.Tuple[int]]) -> typing.List[typing.List[int]]:
        grid = [[0] * cols for _ in range(rows)]
        for x, y in explosive_coordinates:
            grid[x][y] = -1
            for nx, ny in (
                    (x - 1, y), (x + 1, y), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x, y - 1),
                    (x, y + 1)
            ):
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != -1:
                    grid[nx][ny] += 1
        return grid

    @classmethod
    def generate_random_explosives(cls, rows: int, cols: int, explosives_count: int) -> typing.List[typing.Tuple[int]]:
        explosive_coordinates = []
        used_x_y = set()
        c = 0
        while c < explosives_count and c < rows * cols:
            x, y = random.randrange(0, rows), random.randrange(0, cols)
            if f"{x}.{y}" not in used_x_y:
                used_x_y.add(f"{x}.{y}")
                explosive_coordinates.append((x, y))
                c += 1
        return explosive_coordinates

    def __repr__(self):
        return f"score: {self.score} - cells_opened: {self.cells_opened}"


def create_game(mode: int = 1):
    """
    mode:
    0 - easy
    1 - normal
    2 - hard
    3 - impossible
    """
    match mode:
        case 0:
            return Game(rows=8, cols=8, explosives_count=6, lives=3)
        case 1:
            return Game(rows=10, cols=8, explosives_count=12, lives=2)
        case 2:
            return Game(rows=10, cols=8, explosives_count=12, lives=1)
        case 3:
            return Game(rows=11, cols=8, explosives_count=30, lives=1)
