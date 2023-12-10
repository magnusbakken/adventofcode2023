from collections import deque


class Node:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.neighbors = set()

    def __repr__(self):
        return f'Node({self.x}, {self.y}, {self.symbol})'

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __hash__(self):
        return hash((self.x, self.y))

    def _cmp(self, other):
        if self.x == other.x:
            return self.y - other.y
        elif self.x > other.x:
            return 1
        else:
            return -1

    def connect(self, node):
        self.neighbors.add(node)

    def has_neighbor(self, node):
        return node in self.neighbors


def dot(x, y):
    return Node(x, y, '.')


def horizontal(x, y):
    return Node(x, y, '-')


def vertical(x, y):
    return Node(x, y, '|')


class Graph:
    def __init__(self, node_map, width, height, start):
        self.node_map = node_map
        self.width = width
        self.height = height
        self.start = start

    def __str__(self):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(self.node_map[(x, y)].symbol)
            lines.append(line)
        return '\n'.join(''.join(line) for line in lines)

    def non_loop_neighbors(self, x, y):
        for neighbor_x, neighbor_y in get_neighbor_coords(x, y, self.width, self.height):
            neighbor = self.node_map[(neighbor_x, neighbor_y)]
            if neighbor.symbol in ('.', 'I'):
                yield neighbor


def get_neighbor_coords(x, y, width, height):
    if y > 0:
        yield (x, y-1)
    if x > 0:
        yield (x-1, y)
    if x < width - 1:
        yield (x+1, y)
    if y < height - 1:
        yield (x, y+1)


def get_raw_neighbors(node):
    x, y = node.x, node.y
    symbol = node.symbol
    if symbol == '|':
        return [(x, y-1), (x, y+1)]
    elif symbol == '-':
        return [(x-1, y), (x+1, y)]
    elif symbol == 'L':
        return [(x, y-1), (x+1, y)]
    elif symbol == 'J':
        return [(x, y-1), (x-1, y)]
    elif symbol == '7':
        return [(x-1, y), (x, y+1)]
    elif symbol == 'F':
        return [(x+1, y), (x, y+1)]
    else:
        return []


def is_in_bounds(x, y, width, height):
    return x >= 0 and x < width and y >= 0 and y < height


def get_neighbors(node, width, height):
    return [(x, y) for x, y in get_raw_neighbors(node) if is_in_bounds(x, y, width, height)]


def parse(lines):
    node_map = {}
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            node_map[(x, y)] = Node(x, y, symbol)

    height = len(lines)
    width = len(lines[0])
    for y in range(height):
        for x in range(width):
            neighbors = get_neighbors(node_map[(x, y)], width, height)
            for neighbor in neighbors:
                node_map[(x, y)].connect(node_map[neighbor])

    nodes = node_map.values()
    start = next(node for node in nodes if node.symbol == 'S')
    start_neighbors = [node for node in nodes if node.has_neighbor(start)]
    for neighbor in start_neighbors:
        start.connect(neighbor)

    return Graph(node_map, width, height, start)


def read_input(filename):
    with open(filename, 'r') as f:
        return list(map(lambda s: s.strip(), f.readlines()))


def bfs(graph):
    queue = deque([graph.start])
    distances = {graph.start: 0}
    while len(queue) > 0:
        current = queue.popleft()
        for neighbor in current.neighbors:
            if neighbor not in distances:
                queue.append(neighbor)
                distances[neighbor] = distances[current] + 1
    return distances


def bfs_dot(graph):
    start = graph.node_map[(0, 0)]
    queue = deque([start])
    distances = {start: 0}
    while len(queue) > 0:
        current = queue.popleft()
        for neighbor in graph.non_loop_neighbors(current.x, current.y):
            if neighbor not in distances:
                queue.append(neighbor)
                distances[neighbor] = distances[current] + 1
    return distances


def max_distance(graph):
    distances = bfs(graph)
    return max(distances.items(), key=lambda x: x[1])[1]


def get_modified_graph(graph):
    modified_node_map = {}
    distances = bfs(graph)
    for node in graph.node_map.values():
        if node in distances:
            modified_node_map[(node.x, node.y)] = node
        else:
            modified_node_map[(node.x, node.y)] = Node(node.x, node.y, 'I')
    return Graph(modified_node_map, graph.width, graph.height, graph.start)


def get_double_graph(graph):
    doubled_node_map = {}
    for y in range(graph.height):
        for x in range(graph.width):
            old_node = graph.node_map[(x, y)]
            symbol = old_node.symbol
            doubled_node_map[(x*2, y*2)] = Node(x, y, symbol)
            doubled_node_map[(x*2 + 1, y*2 + 1)] = dot(x, y)
            r = (x*2 + 1, y*2)
            d = (x*2, y*2 + 1)
            if symbol == '|':
                doubled_node_map[r] = dot(*r)
                doubled_node_map[d] = vertical(*d)
            elif symbol == '-':
                doubled_node_map[r] = horizontal(*r)
                doubled_node_map[d] = dot(*d)
            elif symbol == 'L':
                doubled_node_map[r] = horizontal(*r)
                doubled_node_map[d] = dot(*d)
            elif symbol == 'J':
                doubled_node_map[r] = dot(*r)
                doubled_node_map[d] = dot(*d)
            elif symbol == '7':
                doubled_node_map[r] = dot(*r)
                doubled_node_map[d] = vertical(*d)
            elif symbol == 'F':
                doubled_node_map[r] = horizontal(*r)
                doubled_node_map[d] = vertical(*d)
            elif symbol == 'S':
                if graph.node_map[(x + 1, y)].symbol in ('-', 'J', '7'):
                    doubled_node_map[r] = horizontal(*r)
                else:
                    doubled_node_map[r] = dot(*r)
                if graph.node_map[(x, y + 1)].symbol in ('|', 'J', 'L'):
                    doubled_node_map[d] = vertical(*d)
                else:
                    doubled_node_map[d] = dot(*d)
            else:
                doubled_node_map[r] = dot(*r)
                doubled_node_map[d] = dot(*d)

    new_start_x, new_start_y = graph.start.x * 2, graph.start.y * 2
    new_width, new_height = graph.width * 2, graph.height * 2
    new_start = doubled_node_map[(new_start_x, new_start_y)]
    new_graph = Graph(doubled_node_map, new_width, new_height, new_start)
    return parse(str(new_graph).split('\n'))


def fill_outside(graph):
    # assume that 0,0 is outside the loop
    explored = bfs_dot(graph)
    modified_node_map = {}
    for node in graph.node_map.values():
        if node in explored:
            modified_node_map[(node.x, node.y)] = dot(node.x, node.y)
        else:
            modified_node_map[(node.x, node.y)] = node
    return Graph(modified_node_map, graph.width, graph.height, graph.start)


def count_enclosed(graph):
    return sum(1 for node in graph.node_map.values() if node.symbol == 'I')


def enclosed_count(graph):
    modified_graph = get_modified_graph(graph)
    double_graph = get_double_graph(modified_graph)
    filled_graph = fill_outside(double_graph)
    return count_enclosed(filled_graph)


def part1(filename):
    graph = parse(read_input(filename))
    return max_distance(graph)


def part2(filename):
    graph = parse(read_input(filename))
    return enclosed_count(graph)


if __name__ == '__main__':
    print(part1('day10.txt'))
    print(part2('day10.txt'))
