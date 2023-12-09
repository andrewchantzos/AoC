from aocd.models import Puzzle
from src.utils import *
import numpy as np
from itertools import count

puzzle = Puzzle(year=2023, day=9)

inp = puzzle.example_data.splitlines()

inp = puzzle.input_data.splitlines()


def to_array(history, flip=False):
    arr = np.array([int(x) for x in history.split(" ")])
    return np.flip(arr) if flip else arr


def extrapolate(arr):
    for step in count(start=1):
        if np.all(np.diff(arr, step) == 0):
            return int(np.sum([np.diff(arr, i)[-1] for i in range(step)]))
    raise Exception("Should not end up here")


puzzle.answer_a = sum([extrapolate(to_array(history)) for history in inp])

puzzle.answer_b = sum([extrapolate(to_array(history, flip=True)) for history in inp])
