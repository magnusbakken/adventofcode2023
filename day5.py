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


def find_range_inflection_points(seed_range, categories):
    prev_n = None
    prev_result = None
    step = 1000
    for n in range(seed_range[0], seed_range[0] + seed_range[1], step):
        n_result = move_through_categories([n], categories)
        if prev_n is not None and n_result - prev_result != step:
            prev_n_ = None
            prev_result_ = None
            for n_ in range(prev_n, n + 1):
                n_result_ = move_through_categories([n_], categories)
                if prev_n_ is not None and n_result_ - prev_result_ != 1:
                    yield (n_-1, n_)
                prev_n_ = n_
                prev_result_ = n_result_
        prev_n = n
        prev_result = n_result


def get_best_seed_from_inflection_points(seed_ranges, categories):
    all_results = []
    for seed_range in seed_ranges:
        for low_point, high_point in find_range_inflection_points(seed_range, categories):
            low_result = move_through_categories([low_point], categories)
            high_result = move_through_categories([high_point], categories)
            all_results.append(low_result)
            all_results.append(high_result)

    return min(all_results)


def part1(filename):
    seeds, categories = parse(read_input(filename))
    return move_through_categories(seeds, categories)


def part2(filename):
    seed_ranges, categories = parse(read_input(filename))
    seed_ranges = list(zip(seed_ranges[::2], seed_ranges[1::2]))
    return get_best_seed_from_inflection_points(seed_ranges, categories)


if __name__ == '__main__':
    print(part1('day5.txt'))
    print(part2('day5.txt'))
