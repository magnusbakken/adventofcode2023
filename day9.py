
def parse(lines):
    return [[int(n) for n in line.split(' ')] for line in lines]


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def diffs(line):
    return [b - a for a, b in zip(line, line[1:])]


def extrapolate(line):
    levels = [line]
    while len(line) > 0 and not all(n == 0 for n in line):
        line = diffs(line)
        levels.append(line)

    levels[-1].append(0)
    for prev_level, next_level in reversed(list(zip(levels[1:], levels))):
        next_level.append(prev_level[-1] + next_level[-1])

    return levels[0][-1]


def all_diffs(lines):
    return sum(extrapolate(line) for line in lines)


def part1(filename):
    return all_diffs(parse(read_input(filename)))


def part2(filename):
    lines = parse(read_input(filename))
    lines = [list(reversed(line)) for line in lines]
    return all_diffs(lines)


if __name__ == '__main__':
    print(part1('day9.txt'))
    print(part2('day9.txt'))
