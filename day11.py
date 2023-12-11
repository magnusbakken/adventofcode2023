class Point:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.n}, {self.x}, {self.y})'


class Graph:
    def __init__(self, points, expanded_rows, expanded_columns, expansion_factor):
        self.points = points
        self.expanded_rows = set(expanded_rows)
        self.expanded_columns = set(expanded_columns)
        self.expansion_factor = expansion_factor

    def distance(self, point1, point2):
        real1, real2 = self.get_real_point(point1), self.get_real_point(point2)
        return manhattan_distance(real1, real2)

    def get_real_point(self, point):
        x_factor = sum(1 for x in self.expanded_columns if x < point.x)
        y_factor = sum(1 for y in self.expanded_rows if y < point.y)
        new_x = point.x + x_factor * (self.expansion_factor - 1)
        new_y = point.y + y_factor * (self.expansion_factor - 1)
        return Point(point.n, new_x, new_y)


def manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def get_expansions(lines):
    expanded_rows = []
    for idx in range(len(lines)):
        if '#' not in lines[idx]:
            expanded_rows.append(idx)

    expanded_columns = []
    for idx in range(len(lines[0])):
        column = [line[idx] for line in lines]
        if '#' not in column:
            expanded_columns.append(idx)

    return expanded_rows, expanded_columns


def parse(lines, expansion_factor):
    points = []
    for y, line in enumerate(lines):
        for x in range(len(line)):
            if line[x] == '#':
                points.append(Point(len(points) + 1, x, y))
    expanded_rows, expanded_columns = get_expansions(lines)
    return Graph(points, expanded_rows, expanded_columns, expansion_factor)


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def all_pairs(graph):
    for point1 in graph.points:
        for point2 in graph.points:
            if point1.n < point2.n:
                yield (point1, point2)


def all_distances(graph):
    return sum(graph.distance(point1, point2) for point1, point2 in all_pairs(graph))


def part1(filename):
    graph = parse(read_input(filename), expansion_factor=2)
    return all_distances(graph)


def part2(filename):
    graph = parse(read_input(filename), expansion_factor=1000000)
    return all_distances(graph)


if __name__ == '__main__':
    print(part1('day11.txt'))
    print(part2('day11.txt'))
