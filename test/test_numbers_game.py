
from copy import deepcopy
import unittest

from NumbersGame import NumbersGame


class TestFindPairsInRows(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_find_single_pair(self):
        row = [1, 1, 2, 3]
        self.assertEqual([(0, 1)], NumbersGame.find_matches_in_list(row))

        row = [1, 2, 2, 3]
        self.assertEqual([(1, 2)], NumbersGame.find_matches_in_list(row))

        row = [1, 2, 3, 3]
        self.assertEqual([(2, 3)], NumbersGame.find_matches_in_list(row))

    def test_find_single_pair_with_gap(self):
        row = [1, 0, 1]
        self.assertEqual([(0, 2)], NumbersGame.find_matches_in_list(row))

        row = [1, 2, 0, 0, 2, 3]
        self.assertEqual([(1, 4)], NumbersGame.find_matches_in_list(row))

        row = [1, 2, 3, 0, 3]
        self.assertEqual([(2, 4)], NumbersGame.find_matches_in_list(row))

    def test_find_double_pair(self):
        row = [1, 1, 2, 2]
        self.assertEqual([(0, 1), (2, 3)], NumbersGame.find_matches_in_list(row))

        row = [1, 0, 1, 2, 0, 2]
        self.assertEqual([(0, 2), (3, 5)], NumbersGame.find_matches_in_list(row))

    def test_pairs_that_are_no_matches(self):
        row = [1, 2, 1]
        self.assertEqual([], NumbersGame.find_matches_in_list(row))

        row = [1, 0, 0, 2, 1, 2]
        self.assertEqual([], NumbersGame.find_matches_in_list(row))

    @unittest.expectedFailure
    def test_find_not_to_many_matches(self):
        row = [1, 1, 1]
        self.assertEqual([(0, 1), (1, 2)], NumbersGame.find_matches_in_list(row))


class TestFindPairsRows(unittest.TestCase):

    def test_find_pair_in_row(self):
        row = [[1, 1]]
        self.assertEqual([(0, (0, 1))], NumbersGame.find_matches_in_rows(row))

    def test_find_a_pair_in_each_row(self):
        row = [[1, 1], [2, 2]]
        self.assertEqual([(0, (0, 1)), (1, (0, 1))], NumbersGame.find_matches_in_rows(row))


class TestFindPairsColumns(unittest.TestCase):

    def test_get_columns(self):
        game = [[1], [1]]
        self.assertEqual([1, 1], NumbersGame.get_columns(game, 0))

        game = [[1, 2], [1, 3]]
        self.assertEqual([2, 3], NumbersGame.get_columns(game, 1))

    def test_find_pair_in_column(self):
        column = [[1], [1]]
        self.assertEqual([(0, (0, 1))], NumbersGame.find_matches_in_columns(column))

    def test_find_a_pair_in_each_column(self):
        column = [[1, 2], [1, 2]]
        self.assertEqual([(0, (0, 1)), (1, (0, 1))], NumbersGame.find_matches_in_columns(column))

    @unittest.expectedFailure
    def test_find_a_multi_pairs_in_a_column(self):
        column = [[1], [1], [1]]
        self.assertEqual([(0, (0, 1)), (0, (1, 2))], NumbersGame.find_matches_in_columns(column))

    def test_find_not_a_pair_in_each_column(self):
        column = [[1, 0, 3], [1, 2, 3]]
        self.assertEqual([(0, (0, 1)), (2, (0, 1))], NumbersGame.find_matches_in_columns(column))


class TestRemoveLines(unittest.TestCase):

    def test_find_empty_row(self):
        game = [[2, 2, 2], [0, 0, 0], [1, 1]]
        self.assertEqual([[1]], NumbersGame.find_empty_row(game))

    def test_remove_line(self):
        game = [[0, 0, 0]]
        self.assertEqual([], NumbersGame.apply_remove_of_empty_lines(game, [0]))

    def test_remove_row(self):
        game = [[2, 2, 2], [0, 0, 0], [1, 1]]
        self.assertEqual([[2, 2, 2], [1, 1]], NumbersGame.apply_remove_of_empty_lines(game, [1]))

    def test_find_and_apply(self):
        game = [[2, 2, 2], [0, 0, 0], [1, 1]]
        matches = NumbersGame.find_empty_row(game)
        print(NumbersGame.apply_remove_of_empty_lines(game, matches))


class TestApplyAMatch(unittest.TestCase):

    def test_cross_a_row_match(self):
        game = [[1, 1]]
        match = (0, (0, 1))
        self.assertEqual([[0, 0]], NumbersGame.apply_match_on_row(game, match))

    def test_cross_a_column_match(self):
        game = [[1], [1]]
        match = (0, (0, 1))
        self.assertEqual([[0], [0]], NumbersGame.apply_match_on_column(game, match))

    def test_apply_a_rule(self):

        game = [[1, 1], [2, 3]]
        match = (0, (0, 1))
        rule = NumbersGame.apply_match_on_row

        self.assertEqual([[0, 0], [2, 3]], NumbersGame.apply_match(game, rule, match))


class TestGameStacking(unittest.TestCase):

    def test_find_stack_numbers(self):
        game = [[1, 1], [2, 2]]
        self.assertEqual([1, 1, 2, 2], NumbersGame.find_stack_numbers(game))

    @unittest.skip("not implemented")
    def test_find_none_stack_numbers(self):
        pass

    def test_stack_full_row(self):
        game = [[1]*9]
        self.assertEqual(2, len(NumbersGame.stack_game(game, [1]*9)))
        self.assertEqual(game[0], game[1])

    def test_stack_single_number(self):
        game = [[1]]

        self.assertEqual([[1, 1]], NumbersGame.stack_game(game, [1]))

    def test_stack_with_skips(self):
        game = [[1, 0, 3, 0, 5, 0, 7, 0, 9]]
        result = [[1, 0, 3, 0, 5, 0, 7, 0, 9],
                  [1, 3, 5, 7, 9]]

        self.assertEqual(result, NumbersGame.stack_game(game, [1, 3, 5, 7, 9]))

    def test_stack_none_full_row(self):
        game = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 0, 2, 0, 2, 0, 2, 0, 2],
                [0, 3, 0, 3, 0, 3]]

        result = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 3, 0, 3, 0, 3, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 2, 2, 2],
                  [2, 2, 3, 3, 3]]

        self.assertEqual(result, NumbersGame.stack_game(game, [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3]))


class TestHeuristics(unittest.TestCase):

    def test_remove_duplicates(self):
        game = [[1, 1], [1, 1]]
        sequence = [[((0, (0, 1)), NumbersGame.apply_match_on_row), ((1, (0, 1)), NumbersGame.apply_match_on_row)],
                    [((1, (0, 1)), NumbersGame.apply_match_on_row), ((0, (0, 1)), NumbersGame.apply_match_on_row)]]

        self.assertEqual(1, len(NumbersGame.remove_duplicates(game, sequence)))


class TestPlayingGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game = [[1, 1, 3, 4], [1, 3, 7, 1]]

    def test_get_all_match_pairs(self):
        game = deepcopy(self.game)
        options = []
        options.extend(NumbersGame.find_matches_in_rows(game))
        options.extend(NumbersGame.find_matches_in_columns(game))

        self.assertEqual(4, len(options))

    def test_solution_sequence_one_match(self):
        game = deepcopy(self.game)
        sequence = [((0, (0, 1)), NumbersGame.apply_match_on_row)]

        self.assertEqual([[0, 0, 3, 4], [1, 3, 7, 1]], NumbersGame.apply_sequence(game, sequence))

    def test_solution_sequence_two_matches(self):
        game = deepcopy(self.game)
        sequence = [((0, (0, 1)), NumbersGame.apply_match_on_row),
                    ((2, (0, 1)), NumbersGame.apply_match_on_column)]

        self.assertEqual([[0, 0, 0, 4], [1, 3, 0, 1]], NumbersGame.apply_sequence(game, sequence))

    def test_start_playing_a_game_for_one_round(self):
        game = deepcopy(self.game)

        sequences = NumbersGame.initial_solver(game)
        self.assertEqual(4, len(sequences))

        for sequence in sequences:
            print(sequence)
            NumbersGame.print_game(NumbersGame.apply_sequence(game, sequence))

    def test_playing_a_game_for_two_rounds(self):
        game = deepcopy(self.game)

        sequences = NumbersGame.initial_solver(game)

        self.assertEqual(13, len(NumbersGame.play_a_round(game, sequences)))

        for sequence in sequences:
            print(sequence)
            NumbersGame.print_game(NumbersGame.apply_sequence(game, sequence))


class TestPlayingForReal(unittest.TestCase):

    def setUp(self) -> None:
        self.game = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                     [1, 1, 1, 2, 1, 3, 1, 4, 1],
                     [5, 1, 6, 1, 7, 1, 8]]

    def test_play_a_game_for_five_rounds(self):

        game = deepcopy(self.game)

        sequences = NumbersGame.initial_solver(game)

        for _ in range(10):
            print(len(sequences))
            sequences = NumbersGame.play_a_round(game, sequences)
            sequences = NumbersGame.remove_duplicates(game, sequences)
            sequences = NumbersGame.only_take_best_candidates(game, sequences)

            if NumbersGame.game_is_won(game, sequences):
                print("Game is won!")
                break

        NumbersGame.safe_game(
            NumbersGame.apply_sequence(game,
                                       NumbersGame.find_most_promising_sequence(game, sequences)),
            'save01.csv')



        print(len(sequences))

        NumbersGame.print_game_statics(game, sequences)

        # for sequence in sequences:
        #     print(sequence)
        #     NumbersGame.print_game(NumbersGame.apply_sequence(game, sequence))


if __name__ == "__main__":

    unittest.main()
