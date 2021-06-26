
from copy import deepcopy


def find_matches_in_list(number_list):
    matches = []
    for i, num1 in enumerate(number_list):
        if num1 == 0:
            continue
        for j, num2 in enumerate(number_list[i + 1:]):
            if num2 == 0:
                continue
            if is_match(num1, num2):
                matches.append((i, i+j+1))
            else:
                break

    return matches


def find_matches_in_rows(game):
    all_matches = [(i, find_matches_in_list(row)) for i, row in enumerate(game)]
    return reformat_matches(all_matches)


def find_matches_in_columns(game):
    all_matches = []
    for column_nr in range(len(game[0])):
        column = get_columns(game, column_nr)
        all_matches.append((column_nr, find_matches_in_list(column)))

    return reformat_matches(all_matches)


def find_empty_row(game):
    empty_rows = [i for i, row in enumerate(game) if sum(row) == 0]
    return [empty_rows] if len(empty_rows) > 0 else []


def find_stack_numbers(game):
    numbers = [n for row in game for n in row if n != 0]
    return [numbers] if len(numbers) > 0 else []


def reformat_matches(all_matches):
    filtered_matches = remove_none_hits(all_matches)
    return [(match[0], pair) for match in filtered_matches for pair in match[1]]


def remove_none_hits(all_matches):
    return [match for match in all_matches if len(match[1]) > 0]


def get_columns(game, row_index):
    return [row[row_index] for row in game if len(row) > row_index]


def is_match(num1, num2):
    return num1 == num2 or num1 + num2 == 10


def apply_match_on_row(game, match):
    game[match[0]][match[1][0]] = 0
    game[match[0]][match[1][1]] = 0
    return game


def apply_match_on_column(game, match):
    game[match[1][0]][match[0]] = 0
    game[match[1][1]][match[0]] = 0
    return game


def apply_remove_of_empty_lines(game, match):
    return [game[i] for i in range(len(game)) if i not in match]


def apply_match(game, rule, match):
    return rule(deepcopy(game), match)


def apply_sequence(game, sequence):
    for elm in sequence:
        game = apply_match(game, elm[1], elm[0])
    return game


def stack_game(game, numbers):

    if len(game[-1]) <= 9:
        append_numbers = numbers[:9-len(game[-1])]
        numbers = numbers[9-len(game[-1]):]
        game[-1].extend(append_numbers)

    for chunk in [numbers[i:i + 9] for i in range(0, len(numbers), 9)]:
        game.append(chunk)

    return game


def get_list_of_rules():
    return [(find_matches_in_rows, apply_match_on_row),
            (find_matches_in_columns, apply_match_on_column),
            (find_empty_row, apply_remove_of_empty_lines)] # ,
            # (find_stack_numbers, stack_game)]


def create_sequence(game):
    sequence = []
    for matcher, rule in get_list_of_rules():
        matches = matcher(game)

        for match in matches:
            sequence.append((match, rule))

    return sequence


def initial_solver(game):
    return [[sequence] for sequence in create_sequence(game)]


def play_a_round(game, sequences):
    for sequence in sequences.copy():
        new_game = apply_sequence(game, sequence)

        for step in create_sequence(new_game):
            new_sequence = sequence.copy()
            new_sequence.append(step)
            sequences.append(new_sequence)

    return sequences


def game_is_won(game, sequences):
    for sequence in sequences:
        game = apply_sequence(game, sequence)
        if len(game) == 0:
            return True


def remove_duplicates(game, sequences):
    filtered_sequences = []
    game_hash_list = []

    for sequence in sequences:
        game_to_check = apply_sequence(game, sequence)
        if hash(str(game_to_check)) not in game_hash_list:
            game_hash_list.append(hash(str(game_to_check)))
            filtered_sequences.append(sequence)

    return filtered_sequences


def print_game_statics(game, sequences):
    number_of_lines = {}

    for sequence in sequences:
        game_to_check = apply_sequence(game, sequence)
        if len(game_to_check) not in number_of_lines:
            number_of_lines[len(game_to_check)] = 1
        else:
            number_of_lines[len(game_to_check)] += 1

    for key, value in number_of_lines.items():
        print("lines {0} in {1} games".format(key, value))


MAX_NUMBER = 10
def only_take_best_candidates(game, sequences):
    return [sequence for sequence in sequences if len(apply_sequence(game, sequence)) < MAX_NUMBER]


def find_most_promising_sequence(game, sequences):
    best_sequence = sequences[0]
    best_sequence_number = len(find_stack_numbers(sequences[0]))
    for sequence in sequences[1:]:
        game_candidate = apply_sequence(game, sequence)
        if len(find_stack_numbers(game_candidate)) < best_sequence_number:
            best_sequence = sequence

    return best_sequence

def print_game(game):
    for row in game:
        print(repr(row))


def safe_game(game, file_name):
    with open(file_name, 'w') as save_file:
        for row in game:
            save_file.write(",".join([str(n) for n in row]) + '\n')


def load_game(file_name):
    game = []
    with open(file_name, 'r') as load_file:
        for line in load_file:
            game.append(line.split(','))

    return game


if __name__ == "__main__":

    game = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 1, 1, 2, 1, 3, 1, 4, 1],
            [5, 1, 6, 1, 7, 1, 8]]

