from aocd.models import Puzzle
from enum import IntEnum
from src.utils import *
from collections import Counter
from functools import cmp_to_key

puzzle = Puzzle(year=2023, day=7)

inp = puzzle.example_data.splitlines()

inp = puzzle.input_data.splitlines()


class HandRank(IntEnum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


def hand_to_rank(hand):
    counter = Counter(hand)
    vals = sorted(counter.values(), reverse=True)
    if vals == [5]:
        return HandRank.FiveOfAKind
    elif vals == [4, 1]:
        return HandRank.FourOfAKind
    elif vals == [3, 2]:
        return HandRank.FullHouse
    elif vals == [3, 1, 1]:
        return HandRank.ThreeOfAKind
    elif vals == [2, 2, 1]:
        return HandRank.TwoPair
    elif vals == [2, 1, 1, 1]:
        return HandRank.OnePair
    else:
        return HandRank.HighCard


mapping = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def compare_hands(hand1, hand2):
    cards1, kind1, _ = hand1
    cards2, kind2, _ = hand2
    if kind1 < kind2:
        return -1
    if kind1 > kind2:
        return 1
    for a, b in zip(cards1, cards2):
        if mapping[a] < mapping[b]:
            return -1
        if mapping[a] > mapping[b]:
            return 1
    return 0


def get_score(hands):
    res = 0
    for pos, (_, _, bid) in enumerate(hands, start=1):
        res += bid * pos
    return res


hands = []
for line in inp:
    hand, bid = line.split(" ")
    bid = int(bid)
    hands.append((hand, hand_to_rank(hand), bid))

hands = sorted(hands, key=cmp_to_key(compare_hands))

# Part 1

puzzle.answer_a = get_score(hands)


def hand_to_rank_joker(hand):
    best = 1
    for card in "23456789TQKA":
        # We will always want to replace with the same value of cards
        alternate = hand.replace("J", card)
        kind = hand_to_rank(alternate)
        best = max(kind, best)
    return best


joker_hands = [(hand.replace("J", "1"), hand_to_rank_joker(hand), bid) for (hand, _, bid) in hands]
joker_hands = sorted(joker_hands, key=cmp_to_key(compare_hands))

# Part 2
puzzle.answer_b = get_score(joker_hands)
