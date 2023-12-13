def parse(lines):
    blocks = []
    current = []
    for line in lines:
        if len(line) == 0:
            blocks.append(current)
            current = []
        else:
            current.append([c for c in line])
    blocks.append(current)
    return blocks


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def find_vertical_reflection(block):
    width = len(block[0])
    for idx in range(width - 1):
        left, right = None, None
        search = 0
        while left == right and idx - search >= 0 and idx + 1 + search < width:
            left = tuple(line[idx-search] for line in block)
            right = tuple(line[idx+1+search] for line in block)
            if left != right:
                break
            search += 1
        else:
            return idx + 1
    return None


def find_horizontal_reflection(block):
    height = len(block)
    for idx in range(height - 1):
        top, bottom = None, None
        search = 0
        while top == bottom and idx - search >= 0 and idx + 1 + search < height:
            top = tuple(block[idx-search])
            bottom = tuple(block[idx+1+search])
            if top != bottom:
                break
            search += 1
        else:
            return idx + 1
    return None


def count_all_reflection_indices(blocks):
    total = 0
    for block in blocks:
        vertical_idx = find_vertical_reflection(block)
        if vertical_idx is None:
            horizontal_idx = find_horizontal_reflection(block)
            if horizontal_idx is None:
                raise Exception('No reflection found for block {block}')
            else:
                total += 100 * horizontal_idx
        else:
            total += vertical_idx
    return total


def smudge(block, x, y):
    old = block[y][x]
    block[y][x] = '.' if block[y][x] == '#' else '#'
    print(f'smudged ({x}, {y}) from {old} to {block[y][x]}')


def get_ranges(block):
    width, height = len(block[0]), len(block)
    baseline = find_vertical_reflection(block)
    if baseline is not None:
        x_range = range(width)
        midpoint = width // 2
        if baseline > midpoint:
            return (x_range, range(baseline - midpoint, width))
        else:
            return (x_range, range(baseline + midpoint))

    baseline = find_horizontal_reflection(block)
    y_range = range(height)
    midpoint = height // 2
    if baseline > midpoint:
        return (range(baseline - midpoint, height), y_range)
    else:
        return (range(baseline + midpoint), y_range)


def count_all_smudged_reflection_indices(blocks):
    total = 0
    for idx, block in enumerate(blocks):
        x_range, y_range = get_ranges(block)
        print(f'ranges: {list(x_range)}, {list(y_range)}')
        for y in y_range:
            found = False
            for x in x_range:
                smudge(block, x, y)
                for line in block:
                    print(''.join(line))
                print()
                horizontal_idx = find_horizontal_reflection(block)
                if horizontal_idx is None:
                    vertical_idx = find_vertical_reflection(block)
                    if vertical_idx is None:
                        smudge(block, x, y)
                    else:
                        print(f'block {idx}: vertical {vertical_idx}')
                        total += vertical_idx
                        found = True
                        break
                else:
                    print(f'block {idx}: horizontal {horizontal_idx}')
                    total += 100 * horizontal_idx
                    found = True
                    break
            if found:
                break
    return total


def part1(filename):
    rows = parse(read_input(filename))
    return count_all_reflection_indices(rows)


def part2(filename):
    rows = parse(read_input(filename))
    return count_all_smudged_reflection_indices(rows)


if __name__ == '__main__':
    print(part1('day13.txt'))
    print(part2('day13_example.txt'))
