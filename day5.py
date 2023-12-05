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


def find_range_inflection_points(seed_range, categories):
    prev_n = None
    prev_result = None
    for n in range(seed_range[0], seed_range[1] + 1, 100):
        n_result = move_through_categories([n], categories)
        if prev_n is not None and n_result < prev_result:
            print('found inflection point, narrowing')
            prev_n_ = None
            prev_result_ = None
            for n_ in range(prev_n, n + 1, 1):
                n_result_ = move_through_categories([n_], categories)
                if prev_n_ is not None and n_result_ > prev_result_:
                    yield (n_-1, n_)
        prev_n = n
        prev_result = n_result


def find_inflection_points(seed_ranges, categories):
    best_range_result = float('inf')
    for seed_range in seed_ranges:
        print(f'seed range: {seed_range}')
        min_, max_ = seed_range[0], seed_range[0] + seed_range[1] - 1
        step = 128
        while step > 1:
            if abs(min_ - max_) <= step:
                print(f'breaking at {min_}, {max_}, {step}')
                break

            # print(f'min={min_} and max={max_}')
            min_result = move_through_categories([min_], categories)
            max_result = move_through_categories([max_], categories)
            # print(f'min result={min_result} and max result={max_result}')

            if min_result > max_result:
                # start from max
                best_result = max_result
                print('from max', max_, min_, step, len(
                    list(reversed(range(min_, max_ + 1, step)))))
                r = reversed(range(min_, max_ + 1, step))
            else:
                # start from min
                best_result = min_result
                print('from min', min_, max_, len(
                    list(range(min_, max_ + 1, step))))
                r = range(min_, max_ + 1, step)

            prev_result = best_result
            prev = None
            for next_ in r:
                next_result = move_through_categories([next_], categories)
                if next_result > prev_result:
                    print(f'found inflection point at ({prev}, {next_})')
                    if prev > next_:
                        min_ = next_
                        max_ = prev
                    else:
                        min_ = prev
                        max_ = next_
                    step = step // 2
                    break
                prev = next_
                prev_result = next_result
        min_result = move_through_categories([min_], categories)
        max_result = move_through_categories([max_], categories)
        print(f'result: min={min_}->{min_result}, max={max_}->{max_result}')
        print()
        if min_result < best_range_result:
            best_range_result = min_result
            print(f'new best: {min_}->{min_result}')
        if max_result < best_range_result:
            best_range_result = max_result
            print(f'new best: {max_}->{max_result}')
        print()
    return best_range_result


def part1(filename):
    seeds, categories = parse(read_input(filename))
    return move_through_categories(seeds, categories)


def part2(filename):
    seed_ranges, categories = parse(read_input(filename))
    seed_ranges = list(zip(seed_ranges[::2], seed_ranges[1::2]))

    for seed_range in seed_ranges:
        print(seed_range)
        for inflection_point in find_range_inflection_points(seed_range, categories):
            print(inflection_point)
        print()


if __name__ == '__main__':
    print(part1('day5.txt'))
    print(part2('day5.txt'))
