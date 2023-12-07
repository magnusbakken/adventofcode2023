from enum import Enum
from operator import __lt__, __gt__, __ge__, __le__


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Rank(OrderedEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


CARD_VALUE_MAPPING = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

JOKER_CARD_VALUE_MAPPING = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1,
}

NON_JOKER_CARDS = [card for card in CARD_VALUE_MAPPING.keys() if card != 'J']


class Hand:
    def __init__(self, cards, bid, use_jokers):
        self.cards = cards
        self.bid = bid
        self.use_jokers = use_jokers
        self._rank = None
        self._card_values = []

    def __repr__(self):
        return f'Hand("{"".join(self.cards)}", {self.bid})'

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        return self._op(other, __lt__, False)

    def __gt__(self, other):
        return self._op(other, __gt__, False)

    def __le__(self, other):
        return self._op(other, __le__, True)

    def __ge__(self, other):
        return self._op(other, __ge__, True)

    def card_value(self, idx):
        if len(self._card_values) <= idx:
            value_mapping = JOKER_CARD_VALUE_MAPPING if self.use_jokers else CARD_VALUE_MAPPING
            self._card_values.append(value_mapping[self.cards[idx]])
        return self._card_values[idx]

    def _op(self, other, op, true_if_equal):
        my_rank = self.rank
        other_rank = other.rank
        if my_rank != other_rank:
            return op(my_rank, other_rank)

        for card_idx in range(len(self.cards)):
            my_card = self.card_value(card_idx)
            other_card = other.card_value(card_idx)
            if my_card != other_card:
                return op(my_card, other_card)

        return true_if_equal

    @property
    def rank(self):
        if self._rank is None:
            if self.use_jokers:
                self._rank = Hand.calculate_rank_with_jokers(self.cards)
            else:
                self._rank = Hand.calculate_rank(self.cards)
        return self._rank

    @staticmethod
    def calculate_rank_with_jokers(cards):
        joker_count = len([card for card in cards if card == 'J'])
        if joker_count in (4, 5):
            return Rank.FIVE_OF_A_KIND

        non_joker_cards = [card for card in cards if card != 'J']
        if joker_count == 3:
            if non_joker_cards[0] == non_joker_cards[1]:
                return Rank.FIVE_OF_A_KIND
            else:
                return Rank.FOUR_OF_A_KIND
        elif joker_count == 2:
            distinct_non_jokers = len(set(non_joker_cards))
            if distinct_non_jokers == 1:
                return Rank.FIVE_OF_A_KIND
            elif distinct_non_jokers == 2:
                return Rank.FOUR_OF_A_KIND
            else:
                return Rank.THREE_OF_A_KIND
        elif joker_count == 1:
            best_substituted_rank = None
            joker_idx = cards.index('J')
            for card in NON_JOKER_CARDS:
                subbed_hand = [*cards[:joker_idx], card, *cards[joker_idx+1:]]
                rank = Hand.calculate_rank(subbed_hand)
                if best_substituted_rank is None or rank > best_substituted_rank:
                    best_substituted_rank = rank
            return best_substituted_rank
        else:
            return Hand.calculate_rank(cards)

    @staticmethod
    def calculate_rank(cards):
        d = {}
        for card in cards:
            if card not in d:
                d[card] = 0
            d[card] += 1
        if len(d) == 1:
            return Rank.FIVE_OF_A_KIND
        elif len(d) == 2:
            if d[cards[0]] in (1, 4):
                return Rank.FOUR_OF_A_KIND
            else:
                return Rank.FULL_HOUSE
        elif len(d) == 3:
            if d[cards[0]] == 1:
                if d[cards[1]] in (1, 3):
                    return Rank.THREE_OF_A_KIND
                else:
                    return Rank.TWO_PAIR
            elif d[cards[0]] == 2:
                return Rank.TWO_PAIR
            else:
                return Rank.THREE_OF_A_KIND
        elif len(d) == 4:
            return Rank.ONE_PAIR
        else:
            return Rank.HIGH_CARD


def parse(lines, use_jokers):
    hands = []
    for line in lines:
        hand, bid = line.split(' ')
        cards = [c for c in hand]
        hands.append(Hand(cards, int(bid), use_jokers))
    return hands


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def rank_hands(hands):
    hands.sort()
    total = 0
    for idx, hand in enumerate(hands):
        total += hand.bid * (idx + 1)
    return total


def part1(filename):
    return rank_hands(parse(read_input(filename), use_jokers=False))


def part2(filename):
    return rank_hands(parse(read_input(filename), use_jokers=True))


if __name__ == '__main__':
    print(part1('day7.txt'))
    print(part2('day7.txt'))
