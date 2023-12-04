import math


def parse(lines):
    cards = []
    for line in lines:
        _, data = line.split(':')
        winners, numbers = data.split('|')
        winners = map(lambda s: s.strip(), winners.strip().split(' '))
        numbers = map(lambda s: s.strip(), numbers.strip().split(' '))
        cards.append(
            (set(winner for winner in winners if winner != ''),
             set(number for number in numbers if number != '')))
    return cards


def read_input(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def count_winners(cards):
    for card in cards:
        matches = len(card[0].intersection(card[1]))
        yield 0 if matches == 0 else int(math.pow(2, matches - 1))


def count_copies(cards):
    copy_count = {}
    for idx, card in enumerate(cards):
        cardnum = idx + 1
        if cardnum not in copy_count:
            copy_count[cardnum] = 0
        copy_count[cardnum] += 1
        matches = len(card[0].intersection(card[1]))
        for n in range(cardnum + 1, cardnum + matches + 1):
            if n not in copy_count:
                copy_count[n] = 0
            copy_count[n] += copy_count[cardnum]
    return sum(copy_count.values())


def part1(filename):
    return sum(count_winners(parse(read_input(filename))))


def part2(filename):
    return count_copies(parse(read_input(filename)))


if __name__ == '__main__':
    print(part1('day4.txt'))
    print(part2('day4.txt'))
