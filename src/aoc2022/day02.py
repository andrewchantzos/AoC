from aocd.models import Puzzle

puzzle = Puzzle(year=2022, day=2)

inp = puzzle.input_data.splitlines()


def get_score(their, my):
    d = {"X": 1, "Y": 2, "Z": 3}
    scores_part1 = {
        "A": {"X": 3, "Y": 6, "Z": 0},
        "B": {"X": 0, "Y": 3, "Z": 6},
        "C": {"X": 6, "Y": 0, "Z": 3},
    }
    return scores_part1[their][mine] + d[my]


total = 0
for line in inp:
    their, mine = line.split(" ")
    total += get_score(their, mine)

# puzzle.answer_a = total


def get_score_part_two(their, my):
    d = {"X": 0, "Y": 3, "Z": 6}
    scores_part2 = {
        'A': {'X': 3, 'Y': 1, 'Z': 2},
        'B': {'X': 1, 'Y': 2, 'Z': 3},
        'C': {'X': 2, 'Y': 3, 'Z': 1}
    }
    return scores_part2[their][mine] + d[my]


total = 0
for line in inp:
    their, mine = line.split(" ")
    total += get_score_part_two(their, mine)

puzzle.answer_b = total
