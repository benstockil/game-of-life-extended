from dataclasses import dataclass
from typing import Callable

from pygame.locals import Color

@dataclass
class Ruleset:
    conditions: list[Callable[[int, int], int]]
    max_state: int
    start_rule: Callable[[int, int], int]
    count_indirect_neighbours: bool

@dataclass
class Config:
    behaviour: Ruleset

    env_width: int
    env_height: int

    win_width: int
    win_height: int
    cell_gap: int

    bg_colour: Color
    alive_colour: Color
    dead_colour: Color


# ------------ DEFINE RULESETS HERE ------------ #

classic = Ruleset(
    conditions=(
        lambda n,s: False if n < 2 or n > 3 else s,
        lambda n,s: True if n==3 else s
    ),
    max_state=1,
    start_rule=lambda x,y: 0,
    count_indirect_neighbours=True
)

labyrinth = Ruleset(
    conditions=(
        lambda n,s: s+1 if n > 5 and n < 9 else s,
        lambda n,s: 0 if n < 3 or n > 8 else s
    ),
    max_state=2,
    start_rule=lambda x,y: 2 if x*100+y % 2 == 0 else 0,
    count_indirect_neighbours=True
)

corruptor = Ruleset(
    conditions=(
        lambda n,s: s+1 if n > 5 and n < 9 else s,
        lambda n,s: 0 if n < 3 or n > 8 else s
    ),
    max_state=2,
    start_rule=lambda x,y: 2 if y%2 == 0 else 0,
    count_indirect_neighbours=True
)

biobrush = Ruleset(
    conditions=(
        lambda n,s: s+1 if n > 5 and n < 9 else s,
        lambda n,s: 0 if n < 3 or n > 8 else s
    ),
    max_state=3,
    start_rule=lambda x,y: 0,
    count_indirect_neighbours=False
)

# ------------ DEFINE CONFIG HERE ------------ #

config = Config(
    behaviour=corruptor,
    env_width=100,
    env_height=100,
    win_width=500,
    win_height=500,
    cell_gap=1,
    bg_colour=Color(0, 0, 0),
    alive_colour=Color(240, 0, 120),
    dead_colour=Color(30, 30, 30)
)

