from __future__ import annotations
from copy import deepcopy
from aocd.models import Puzzle
from collections import defaultdict
from copy import deepcopy
from collections import deque
from math import lcm

puzzle = Puzzle(year=2023, day=20)

inp = puzzle.input_data.splitlines()


class FlipFlop:
    def __init__(self, dests, val):
        self.dests = dests
        self.val = val

    def flip(self):
        self.val = not self.val


class Conjunction:
    def __init__(self, dests):
        self.dests = dests
        self.memory = {}

    def add_memory(self, memory):
        self.memory = memory

    def receive(self, src, pulse):
        self.memory[src] = pulse

    def send(self):
        return not all(self.memory.values())


broadcaster = []

flip_flops = {}
conjunctions = {}
revs_map = defaultdict(list)
for line in inp:
    label, destinations = [s.strip() for s in line[1:].split("->")]
    destinations = [dest.strip() for dest in destinations.split(",")]

    if label == "roadcaster":
        broadcaster = destinations
    if line.startswith("%"):
        # flip-flop
        flip_flops[label] = FlipFlop(destinations, False)

    if line.startswith("&"):
        # conjunction
        conjunctions[label] = Conjunction(destinations)

    for dest in destinations:
        revs_map[dest].append(label)

for label, con in conjunctions.items():
    memory = {el: False for el in revs_map[label]}
    con.add_memory(memory)


def part1(flip_flops, conjunctions):
    low_pulses = 0
    high_pulses = 0
    flip_flops = deepcopy(flip_flops)
    conjunctions = deepcopy(conjunctions)

    for _ in range(1000):
        queue = deque((el, False, "broadcaster") for el in broadcaster)
        low_pulses += 1

        while queue:
            label, pulse, src = queue.popleft()

            high_pulses += pulse
            low_pulses += not pulse

            if label in flip_flops:
                if pulse:
                    continue
                flip_flop = flip_flops[label]
                flip_flop.flip()
                for dest in flip_flop.dests:
                    queue.append((dest, flip_flop.val, label))

            if label in conjunctions:
                conjunction = conjunctions[label]
                conjunction.receive(src, pulse)
                for dest in conjunction.dests:
                    queue.append((dest, conjunction.send(), label))
    return low_pulses * high_pulses


def part2(flip_flops, conjunctions):
    low_pulses = 0
    high_pulses = 0
    button = 0
    flip_flops = deepcopy(flip_flops)
    conjunctions = deepcopy(conjunctions)
    rx_origin = revs_map["rx"][0]
    rx_buttons = {}

    while True:
        queue = deque((el, False, "broadcaster") for el in broadcaster)
        low_pulses += 1
        button += 1
        while queue:
            label, pulse, src = queue.popleft()
            if label == "rx":
                continue

            high_pulses += pulse
            low_pulses += not pulse

            if label in flip_flops:
                if pulse:
                    continue
                flip_flop = flip_flops[label]
                flip_flop.flip()
                for dest in flip_flop.dests:
                    queue.append((dest, flip_flop.val, label))

            if label in conjunctions:
                conjunction = conjunctions[label]
                conjunction.receive(src, pulse)
                for dest in conjunction.dests:
                    queue.append((dest, conjunction.send(), label))

            for label, val in conjunctions[rx_origin].memory.items():
                if val == 1 and label not in rx_buttons:
                    rx_buttons[label] = button

            # There are only 4 cycles in the input
            if len(rx_buttons) == 4:
                return lcm(*rx_buttons.values())


puzzle.answer_a = part1(flip_flops, conjunctions)
puzzle.answer_b = part2(flip_flops, conjunctions)
