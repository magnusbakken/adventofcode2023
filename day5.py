class Range:
    def __init__(self, destination, source, amount):
        self.destination = destination
        self.source = source
        self.amount = amount
        self._diff = self.destination - self.source

    def __repr__(self):
        return f'Range({self.destination}, {self.source}, {self.amount})'

    def get_mapping(self, n):
        if n >= self.source and n < self.source + self.amount:
            return n + self._diff
        else:
            return None


class Category:
    def __init__(self, source_type, destination_type, ranges):
        self.source_type = source_type
        self.destination_type = destination_type
        self.ranges = ranges

    def __repr__(self):
        return f'Category({self.source_type}, {self.destination_type}, {self.ranges})'

    def map_number(self, n):
        for range in self.ranges:
            range_mapping = range.get_mapping(n)
            if range_mapping is not None:
                return range_mapping
        return n

    def reverse_map_number(self, n):
        for range in self.ranges:
            range_mapping = range.get_reverse_mapping(n)
            if range_mapping is not None:
                return range_mapping
        return n

    def lowest_range(self, n):
        applicable_ranges = (
            r for r in self.ranges if r.get_mapping(n) is not None)
        range_ = list(sorted(applicable_ranges,
                      key=lambda range: range.destination))
        return Range(n, n, 1) if len(range_) == 0 else range_[0]


def parse_range(lines, idx):
    line = lines[idx]
    destination, source, amount = map(int, line.split(' '))
    return (idx + 1, Range(destination, source, amount))


def parse_category(lines, idx):
    while not lines[idx].endswith(' map:'):
        idx += 1

    source, destination = lines[idx].removesuffix(' map:').split('-to-')
    idx += 1
    ranges = []
    while idx < len(lines) and not len(lines[idx]) == 0:
        idx, range_ = parse_range(lines, idx)
        ranges.append(range_)
    return (idx, Category(source, destination, ranges))


def parse_seeds(lines):
    line = lines[0].removeprefix('seeds: ')
    return list(map(int, line.split(' ')))


def parse(lines):
    seeds = parse_seeds(lines)
    idx = 2
    categories = []
    while idx < len(lines):
        idx, category = parse_category(lines, idx)
        categories.append(category)
    return seeds, categories


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def move_through_categories(seeds, categories):
    lowest = float('inf')
    for seed in seeds:
        n = seed
        current_category = 'seed'
        while current_category != 'location':
            category = next(
                c for c in categories if c.source_type == current_category)
            current_category = category.destination_type
            n = category.map_number(n)
        if n < lowest:
            lowest = n
    return lowest


def is_in_seed_ranges(n, seed_ranges):
    for seed_range in seed_ranges:
        start, amount = seed_range
        if n >= start and n < start + amount:
            return True
    return False


def find_lowest_locations(categories):
    current_category = 'location'
    best_n = 0
    while current_category != 'seed':
        category = next(
            c for c in categories if c.destination_type == current_category)
        current_category = category.source_type
        best_range = category.lowest_range(best_n)
        best_n = best_range.destination

    return best_n


def part1(filename):
    seeds, categories = parse(read_input(filename))
    return move_through_categories(seeds, categories)


def part2(filename):
    seed_ranges, categories = parse(read_input(filename))
    seed_ranges = list(zip(seed_ranges[::2], seed_ranges[1::2]))
    best_n = find_lowest_locations(categories)
    closest_range, closest_diff = None, float('inf')
    for start, amount in seed_ranges:
        if start > best_n and start - best_n < closest_diff:
            closest_diff = start - best_n
            closest_range = (start, amount)
    print(best_n)
    print(closest_range)


if __name__ == '__main__':
    print(part1('day5.txt'))
    print(part2('day5.txt'))
