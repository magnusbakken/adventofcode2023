import itertools as it


class Row:
    def __init__(self, springs, spring_runs, non_empty_runs, run_counts):
        self.springs = springs
        self.spring_runs = spring_runs
        self.non_empty_runs = non_empty_runs
        self.run_counts = run_counts


def group_by_run(line, mapper=None):
    current = None
    start_idx = None
    count = 0
    for idx, c in enumerate(line):
        c = mapper(c) if mapper else c
        if c == current:
            count += 1
        else:
            if current is not None:
                yield (current, count)
            current = c
            start_idx = idx
            count = 1
    yield (start_idx, current, count)


def parse(lines, unfold=False):
    results = []
    non_empty_mapper = {'.': '.', '?': '#', '#': '#'}
    for line in lines:
        springs, specs = line.split(' ')
        if unfold:
            springs = '?'.join(springs for _ in range(5))
            specs = ','.join(specs for _ in range(5))
        run_counts = tuple(map(int, specs.split(',')))
        runs = list(group_by_run(springs))
        non_empty_runs = list(group_by_run(springs, mapper=non_empty_mapper))
        results.append(Row(springs, runs, non_empty_runs, run_counts))
    return results


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def is_match(runs, run_counts):
    grouped = list(group_by_run(runs))
    spring_counts = tuple([value for _, key, value in grouped if key == '#'])
    return spring_counts == run_counts


def apply_combination(row, combination):
    l = [c for c in row.springs]
    for c in combination:
        l[c] = '#'
    return l


def remove_impossible(row):
    springs = [c for c in row.springs]
    first_group_length = row.run_counts[0]
    first_known_run = next(run for run in row.non_empty_runs if run[0] == '#')


def find_plausible_combinations(row):
    springs = remove_impossible(row)
    unknown_indices = [idx for idx,
                       value in enumerate(springs) if value == '?']
    known_count = sum(1 for value in row.springs if value == '#')
    target_count = sum(row.run_counts)
    unknown_count = target_count - known_count
    combos = list(it.combinations(unknown_indices, unknown_count))
    return combos


def find_solutions(row, unfold=False):
    combos = find_plausible_combinations(row)
    if unfold:
        print(f'combination count: {len(combos)}')
    for combination in combos:
        new_row = apply_combination(row, combination)
        if is_match(new_row, row.run_counts):
            yield combination


def count_all_solutions(rows, unfold=False):
    total = 0
    for idx, row in enumerate(rows):
        if unfold:
            print(f'Starting row {idx} (total={total})')
        for solution in find_solutions(row, unfold=unfold):
            total += 1
    return total


def part1(filename):
    rows = parse(read_input(filename))
    return count_all_solutions(rows)


def part2(filename):
    rows = parse(read_input(filename), unfold=True)
    return count_all_solutions(rows, unfold=True)


if __name__ == '__main__':
    print(part1('day12.txt'))
    print(part2('day12_example.txt'))
