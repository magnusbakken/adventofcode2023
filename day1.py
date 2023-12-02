import re


def is_digit(c):
    return ord(c) >= ord('0') and ord(c) <= ord('9')


def digits1(line):
    digs = list(map(int, filter(is_digit, line)))
    return digs[0], digs[-1]


MAPPING = {'one': 1, 'two': 2, 'three': 3, 'four': 4,
           'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
           '1': 1, '2': 2, '3': 3, '4': 4,
           '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}


def index_safe(s, search, from_right):
    try:
        return s.rindex(search) if from_right else s.index(search)
    except:
        return -1


def digits2(line):
    first_idx = float('inf')
    first_digit = None
    last_idx = float('-inf')
    last_digit = None
    for digit_word in MAPPING.keys():
        first_digit_idx = index_safe(line, digit_word, False)
        last_digit_idx = index_safe(line, digit_word, True)
        if first_digit_idx >= 0 and first_digit_idx < first_idx:
            first_idx = first_digit_idx
            first_digit = MAPPING[digit_word]
        if last_digit_idx >= 0 and last_digit_idx > last_idx:
            last_idx = last_digit_idx
            last_digit = MAPPING[digit_word]

    return first_digit, last_digit


def all_nums(lines, digits_f):
    return sum(map(lambda x: 10*x[0] + x[1], map(digits_f, lines)))


def read_input(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def part1(filename):
    return all_nums(read_input(filename), digits1)


def part2(filename):
    return all_nums(read_input(filename), digits2)


if __name__ == '__main__':
    print(part1('day1.txt'))
    print(part2('day1.txt'))
