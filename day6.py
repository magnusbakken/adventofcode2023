import math

PUZZLE_INPUT_TIME = [61, 70, 90, 66]
PUZZLE_INPUT_DISTANCE = [643, 1184, 1362, 1041]

PUZZLE_INPUT_TIME_2 = [61709066]
PUZZLE_INPUT_DISTANCE_2 = [643118413621041]


def race(idx, hold_time, input_times):
    race_time = input_times[idx]
    return (race_time - hold_time) * hold_time


def beats_record(idx, hold_time, input_times, input_distances):
    record_distance = input_distances[idx]
    return race(idx, hold_time, input_times) > record_distance


def all_hold_times(idx, input_times, input_distances):
    record_hold_times = []
    for hold_time in range(1, input_times[idx]):
        if beats_record(idx, hold_time, input_times, input_distances):
            record_hold_times.append(hold_time)
    return record_hold_times


def all_races(input_times, input_distances):
    record_times = []
    for idx in range(len(input_times)):
        record_times.append(
            len(all_hold_times(idx, input_times, input_distances)))
    return math.prod(record_times)


def part1():
    return all_races(PUZZLE_INPUT_TIME, PUZZLE_INPUT_DISTANCE)


def part2():
    return all_races(PUZZLE_INPUT_TIME_2, PUZZLE_INPUT_DISTANCE_2)


if __name__ == '__main__':
    print(part1())
    print(part2())
