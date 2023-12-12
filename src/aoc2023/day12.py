from aocd.models import Puzzle
from src.utils import *
from functools import cache

puzzle = Puzzle(year=2023, day=12)


inp = puzzle.input_data.splitlines()

# inp = """???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1""".splitlines()


@cache
def solver(s, remains, within=0) -> int:
    if not s:
        if not within and len(remains) == 0:
            return 1
        if len(remains) == 1 and within == remains[0]:
            return 1
        return 0

    possible_more = sum(1 for ch in s if ch in "#?")

    if possible_more + within < sum(remains):
        return 0
    if within and not remains:
        return 0

    matching_remainder = len(remains) and within == remains[0]

    match s[0]:
        case "#":
            return solver(s[1:], remains, within + 1)
        case ".":
            if matching_remainder:
                return solver(s[1:], remains[1:], 0)
            elif not within:
                return solver(s[1:], remains, 0)
            elif within:
                return 0
        case "?":
            if matching_remainder:
                return solver(s[1:], remains[1:], 0)
            elif not within:
                # The important step. Match or not match
                return solver(s[1:], remains, 0) + solver(s[1:], remains, 1)
            elif within:
                return solver(s[1:], remains, within + 1)
    return 0


inp1 = []
inp2 = []
for line in inp:
    string = line.split(" ")[0]
    arrangements = tuple([int(x) for x in line.split(" ")[1].split(",")])
    inp1.append((string, arrangements))
    inp2.append(("?".join([string] * 5), arrangements * 5))


puzzle.answer_a = sum(solver(x, arr) for x, arr in inp1)

puzzle.answer_b = sum(solver(x, arr) for x, arr in inp2)
exit()

# Alternative brute force solution (will not work for part 2)


def get_positions(s, target_char):
    return [index for index, char in enumerate(s) if char == target_char]


def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(0, len(s) + 1))


def consecutive_ranges(lst, target_element):
    ranges = []
    for key, group in itertools.groupby(lst):
        if key == target_element:
            ranges.append(len(list(group)))
    return tuple(ranges)


count = 0
for string, arrangements in inp1:
    string = string.replace("..", ".")
    questionmarks = get_positions(string, "?")
    init_string = string.replace("?", ".")
    for combo in powerset(questionmarks):
        string = list(init_string)
        for i in combo:
            string[i] = "#"
        if consecutive_ranges(string, "#") == arrangements:
            count += 1

puzzle.answer_a = count
