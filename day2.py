import math


def parse_round(s):
    colors = []
    for color_desc in s.split(', '):
        number, color = color_desc.split(' ')
        colors.append((int(number), color.strip()))
    return colors


def parse_game(line):
    game_num_text, game_desc = line.split(': ')
    _, game_num_desc = game_num_text.split(' ')
    game_num = int(game_num_desc)
    round_descs = game_desc.split('; ')
    rounds = list(map(parse_round, round_descs))
    return (game_num, rounds)


def parse(lines):
    return list(map(parse_game, lines))


def read_input(filename):
    with open(filename, 'r') as f:
        return f.readlines()


LIMITS = {'red': 12, 'green': 13, 'blue': 14}


def check_colors(game):
    for round in game:
        for amount, color in round:
            if amount > LIMITS[color]:
                return False
    return True


def find_valid_games(games):
    valid_game_nums = []
    for game_num, game in games:
        if check_colors(game):
            valid_game_nums.append(game_num)
    return sum(valid_game_nums)


def find_game_minimums(game):
    max_by_color = {'red': 0, 'green': 0, 'blue': 0}
    for round in game:
        for amount, color in round:
            if amount > max_by_color[color]:
                max_by_color[color] = amount
    return max_by_color


def find_total_power(games):
    total = 0
    for _, game in games:
        max_by_color = find_game_minimums(game)
        color_prod = math.prod(max_by_color.values())
        total += color_prod
    return total


def part1(filename):
    return find_valid_games(parse(read_input(filename)))


def part2(filename):
    return find_total_power(parse(read_input(filename)))


if __name__ == '__main__':
    print(part1('day2.txt'))
    print(part2('day2.txt'))
