import re


def parse(lines):
    grid = []
    for line in lines:
        line_values = {}
        for match in re.finditer('(\\d+|[^.\\d])', line.rstrip()):
            if match.group(0).isnumeric():
                line_values[match.span()] = int(match.group(0))
            else:
                line_values[match.span()] = match.group(0)
        grid.append(line_values)
    return grid


def read_input(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def find_adjacent_indices(rownum, span, grid, rowwidth):
    is_top = rownum == 0
    is_bottom = rownum == len(grid) - 1
    is_left = span[0] == 0
    is_right = span[1] == rowwidth
    if not is_top:
        if not is_left:
            yield (span[0] - 1, rownum - 1)
        for idx in range(span[0], span[1]):
            yield (idx, rownum - 1)
        if not is_right:
            yield (span[1], rownum - 1)

    if not is_left:
        yield (span[0] - 1, rownum)
    if not is_right:
        yield (span[1], rownum)

    if not is_bottom:
        if not is_left:
            yield (span[0] - 1, rownum + 1)
        for idx in range(span[0], span[1]):
            yield (idx, rownum + 1)
        if not is_right:
            yield (span[1], rownum + 1)


def is_adjacent_to_symbol(rownum, span, grid, rowwidth):
    for x, y in find_adjacent_indices(rownum, span, grid, rowwidth):
        if (x, x + 1) in grid[y]:
            return True
    return False


def get_gear_ratio(rownum, span, grid, rowwidth):
    adjacent_spans = set()
    for x, y in find_adjacent_indices(rownum, span, grid, rowwidth):
        for adjacent_span in grid[y]:
            if x in tuple(range(*adjacent_span)) and isinstance(grid[y][adjacent_span], int):
                adjacent_spans.add((adjacent_span, y))
    spans = list(adjacent_spans)
    if len(spans) == 2:
        (span1, y1), (span2, y2) = spans
        return grid[y1][span1] * grid[y2][span2]
    else:
        return None


def find_part_numbers(grid, rowwidth):
    for rownum, line in enumerate(grid):
        for span, value in line.items():
            if isinstance(value, int):
                if is_adjacent_to_symbol(rownum, span, grid, rowwidth):
                    yield value


def find_gear_ratios(grid, rowwidth):
    for rownum, line in enumerate(grid):
        for span, value in line.items():
            if value == '*':
                gear_ratio = get_gear_ratio(rownum, span, grid, rowwidth)
                if gear_ratio:
                    yield gear_ratio


def part1(filename):
    lines = read_input(filename)
    return sum(find_part_numbers(parse(lines), len(lines[0])))


def part2(filename):
    lines = read_input(filename)
    return sum(find_gear_ratios(parse(lines), len(lines[0])))


if __name__ == '__main__':
    print(part1('day3.txt'))
    print(part2('day3.txt'))
