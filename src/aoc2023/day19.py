from __future__ import annotations
from aocd.models import Puzzle
import collections
import ast
from functools import reduce
from operator import mul
from copy import deepcopy
from typing import Tuple

puzzle = Puzzle(year=2023, day=19)

Rule = collections.namedtuple("Rule", ["conditions", "fallback"])


class Condition:
    def __init__(self, str_repr: str, target: str):
        self.str_repr = str_repr
        self.target = target
        self.xmas = str_repr[0]
        self.comp = str_repr[1]
        self.value = int(str_repr[2:])

    def split(self, rng: range) -> Tuple[range, range]:
        def more(rng: range, value: int):
            return range(value + 1, rng.stop), range(rng.start, value + 1)

        def less(rng: range, value: int):
            return range(rng.start, value), range(value, rng.stop)

        operator = more if self.comp == ">" else less
        return operator(rng, self.value)


def read_input():
    rules = {}
    ratings = []
    workflows, ratings_str = puzzle.input_data.split("\n\n")

    for line in workflows.splitlines():
        name = line.split("{")[0]
        str_rules = line.split("{")[1].replace("}", "").split(",")
        conditions = []

        for rule in str_rules:
            rule_split = rule.split(":")
            if len(rule_split) == 2:
                conditions.append((Condition(*rule_split)))
            rules[name] = Rule(conditions, fallback=rule_split[0])

    for line in ratings_str.splitlines():
        rating = {
            key: int(value)
            for pair in line.strip("{}").split(",")
            for key, value in (pair.split("="),)
        }
        ratings.append(rating)
    return rules, ratings


rules, ratings = read_input()


def evaluate(operation_str: str, val: int, name: str) -> bool:
    operation_ast = ast.parse(operation_str, mode="eval")
    return eval(compile(operation_ast, filename="<string>", mode="eval"), {name: val})


def matching(rating: dict, rule: Rule) -> str:
    # Change the implementation for the second part therefore `cond.str_repr`
    # is a bit unnatural, but I liked the `ast` idea, so I kept the first part
    # as is
    for cond in rule.conditions:
        for ch in "xmas":
            if ch in cond.str_repr and evaluate(cond.str_repr, rating[ch], ch):
                return cond.target
    return rule.fallback


def count_workflows(start_from: str) -> int:
    total = 0
    for rating in ratings:
        target = start_from
        while True:
            target = matching(rating, rules[target])
            if target == "A":
                total += sum(rating.values())
                break
            if target == "R":
                break
    return total


MAX_RANGE = range(1, 4001)


class XmasRanges:
    def __init__(self, rng={c: MAX_RANGE for c in "xmas"}):
        self.rng = rng

    def __getitem__(self, char):
        return self.rng[char]

    def __setitem__(self, char, val):
        self.rng[char] = val

    def apply(self, cond: Condition) -> Tuple[XmasRanges, XmasRanges]:
        match, no_match = deepcopy(self), deepcopy(self)
        original_range = self[cond.xmas]

        # Update ranges
        match[cond.xmas], no_match[cond.xmas] = cond.split(original_range)
        return match, no_match

    def __len__(self) -> int:
        return reduce(mul, map(len, self.rng.values()))


def count_workflows_range(name: str, remaining=XmasRanges()) -> int:
    if name == "A":
        return len(remaining)
    if name == "R":
        return 0

    total = 0
    rule = rules[name]
    for condition in rule.conditions:
        matching, remaining = remaining.apply(condition)
        total += count_workflows_range(condition.target, matching)
    return total + count_workflows_range(rule.fallback, remaining)


puzzle.answer_a = count_workflows("in")
puzzle.answer_b = count_workflows_range("in")
