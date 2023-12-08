import math
import re

MAPPING_RE = re.compile(r'(\w+) = \((\w+)\, (\w+)\)')


def parse(lines):
    moves = lines[0]
    mappings = {}
    for line in lines[2:]:
        match = MAPPING_RE.match(line)
        mappings[match.group(1)] = (match.group(2), match.group(3))
    return moves, mappings


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def traverse(instructions, mappings):
    current = mappings['AAA']
    history = []
    destination = None
    while destination != 'ZZZ':
        for instruction in instructions:
            destination = current[0] if instruction == 'L' else current[1]
            history.append((instruction, destination))
            current = mappings[destination]
            if destination == 'ZZZ':
                break
    return len(history)


def traverse_multi(instructions, mappings):
    current_keys = list(filter(lambda key: key.endswith('A'), mappings.keys()))
    count = 0
    at_end_by_idx = [None for _ in current_keys]
    while not all(current.endswith('Z') for current in current_keys):
        for instruction in instructions:
            new_current_keys = []
            for idx, current_key in enumerate(current_keys):
                current = mappings[current_key]
                destination = current[0] if instruction == 'L' else current[1]
                new_current_keys.append(destination)
                if destination.endswith('Z'):
                    if at_end_by_idx[idx] is None:
                        at_end_by_idx[idx] = count + 1
                if all(x is not None for x in at_end_by_idx):
                    return math.lcm(*at_end_by_idx)
            count += 1
            current_keys = new_current_keys

    return count


def part1(filename):
    return traverse(*parse(read_input(filename)))


def part2(filename):
    return traverse_multi(*parse(read_input(filename)))


if __name__ == '__main__':
    print(part1('day8.txt'))
    print(part2('day8.txt'))
