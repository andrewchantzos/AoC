from aocd.models import Puzzle
import re
from collections import defaultdict

puzzle = Puzzle(year=2023, day=2)

inp = puzzle.input_data.splitlines()

# Get input
def get_combo(txt):
    def _filter_regex(colour, txt):
        res = re.findall(r"([0-9]+) " + colour, txt)
        if res:
            return int(res[0])
        return 0

    green = _filter_regex("green", txt)
    red = _filter_regex("red", txt)
    blue = _filter_regex("blue", txt)
    return (green, red, blue)


d = defaultdict(list)
for x in inp:
    game_num = int(re.findall(r"Game (\d*):", x)[0])

    for split in x.split(":")[1].split(";"):
        d[game_num].append(get_combo(split))

# part one

# 12 red cubes, 13 green cubes, and 14 blue cubes
to_match = (13, 12, 14)

def cmp_tuples(tup1, tup2):
    return all(x >= y for x, y in zip(tup1, tup2))

total = 0
for num, games in d.items():
    if all(cmp_tuples(to_match, game) for game in games):
        total += num

puzzle.answer_a = total

# part two

total = 0
for games in d.values():
    reds, greens, blues = zip(*games)
    total += max(reds) * max(blues) * max(greens)

puzzle.answer_b = total
