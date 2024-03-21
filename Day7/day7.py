import re
from parse import parse_file
from functools import reduce


class Hand:
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    def __init__(self, hand, with_joker: bool = False):
        self.hand = hand
        self.with_joker = with_joker
        self.type = Hand.evualuate_type(self.hand, self.with_joker)

    def __repr__(self) -> str:
        return f'{self.hand}: {self.type}'

    def __lt__(self, other):
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False

        for (cs, co) in zip(self.hand, other.hand):
            def key_function(char):
                if self.with_joker:
                    if char == 'J':
                        return 0
                    elif char.isdigit():
                        return int(char) - 1
                    elif char == 'T':
                        return 9
                    elif char == 'Q':
                        return 10
                    elif char == 'K':
                        return 11
                    else:
                        return 12
                else:
                    if char.isdigit():
                        return int(char) - 2
                    elif char == 'T':
                        return 8
                    elif char == 'J':
                        return 9
                    elif char == 'Q':
                        return 10
                    elif char == 'K':
                        return 11
                    else:
                        return 12
            if key_function(cs) < key_function(co):
                return True
            elif key_function(cs) > key_function(co):
                return False
        return False

    def evualuate_type(hand, with_joker):
        buckets = {c: 0 for c in hand}

        def count_chars(buckets, char):
            buckets[char] += 1
            return buckets
        buckets = reduce(count_chars, hand, buckets)
        sorted_counts = sorted(buckets.values(), reverse=True)
        if with_joker and buckets.get('J') is not None:
            if buckets['J'] == sorted_counts[0]:
                if len(sorted_counts) == 1:
                    sorted_counts.append(0)
                sorted_counts[1] += buckets['J']
                sorted_counts.pop(0)
            else:
                sorted_counts[0] += buckets['J']
                sorted_counts.remove(buckets['J'])
        result = None
        if sorted_counts[0] == 5:
            result = Hand.FIVE_OF_A_KIND
        elif sorted_counts[0] == 4:
            result = Hand.FOUR_OF_A_KIND
        elif sorted_counts[0] == 3:
            if sorted_counts[1] == 2:
                result = Hand.FULL_HOUSE
            else:
                result = Hand.THREE_OF_A_KIND
        elif sorted_counts[0] == 2:
            if sorted_counts[1] == 2:
                result = Hand.TWO_PAIRS
            else:
                result = Hand.ONE_PAIR
        else:
            result = Hand.HIGH_CARD
        return result


def parse_line(line, with_joker: bool = False):
    m = re.match('([2-9AKQJT]{5}) ([0-9]+)', line)
    hand = Hand(m.group(1), with_joker)
    bid = int(m.group(2))
    return (hand, bid)


def solve(filename, with_joker: bool):
    hand_bid_pairs = parse_file(
        filename, lambda line: parse_line(line, with_joker))
    hand_bid_pairs.sort(key=lambda pair: pair[0])
    solution = 0
    for (i, (_, bid)) in enumerate(hand_bid_pairs):
        solution += bid * (i + 1)
    print(solution)


if __name__ == '__main__':
    solve('input', False)
    solve('input', True)
