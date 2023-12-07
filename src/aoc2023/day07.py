from aocd.models import Puzzle
from enum import IntEnum
from src.utils import *
from collections import Counter
from functools import cmp_to_key, partial

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


def compare_hands(hand_to_rank, hand1, hand2):
    cards1, _ = hand1
    cards2, _ = hand2
    kind1 = hand_to_rank(cards1)
    kind2 = hand_to_rank(cards2)

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


def hand_to_rank_joker(hand):
    possible_hands = [hand.replace("1", card) for card in "23456789TJQKA"]
    return max(hand_to_rank(possible_hand) for possible_hand in possible_hands)


def get_score(hands):
    return sum(bid * pos for pos, (_, bid) in enumerate(hands, start=1))



# Part 1
hands = [(part[0], int(part[1])) for part in (line.split() for line in inp)]

hands = sorted(hands, key=cmp_to_key(partial(compare_hands, hand_to_rank)))

puzzle.answer_a = get_score(hands)

# Part 2

joker_hands = [(hand.replace("J", "1"), bid) for (hand, bid) in hands]
joker_hands = sorted(joker_hands, key=cmp_to_key(partial(compare_hands, hand_to_rank_joker)))

puzzle.answer_b = get_score(joker_hands)
