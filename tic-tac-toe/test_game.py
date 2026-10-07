import unittest
from game.rules import check_winner, is_board_full
from game.game_engine import GameEngine, HUMAN_SYMBOL, COMPUTER_SYMBOL


class TestTicTacToe(unittest.TestCase):
    def test_task1_diagonals(self):
        # Main diagonal
        b1 = [
            ['X', 'O', None],
            ['O', 'X', None],
            [None, None, 'X']
        ]
        self.assertEqual(check_winner(b1), 'X')

        # Anti diagonal
        b2 = [
            [None, 'X', 'O'],
            [None, 'O', 'X'],
            ['O', None, None]
        ]
        self.assertEqual(check_winner(b2), 'O')

    def test_task1_win_on_last_move(self):
        # Board full, but X won on row 0
        b_full_win = [
            ['X', 'X', 'X'],
            ['O', 'O', 'X'],
            ['X', 'O', 'O']
        ]
        self.assertTrue(is_board_full(b_full_win))
        self.assertEqual(check_winner(b_full_win), 'X')

        engine = GameEngine()
        engine.board = b_full_win
        engine.check_round_end()
        self.assertTrue(engine.round_over)
        self.assertEqual(engine.winner, 'X')
        self.assertEqual(engine.scores['X'], 1)
        self.assertEqual(engine.scores['Draw'], 0)

    def test_task1_no_moves_after_game_over(self):
        engine = GameEngine()
        engine.round_over = True
        engine.current_player = 'X'
        engine.handle_click((50, 120))  # should be rejected
        self.assertIsNone(engine.board[0][0])

    def test_task2_persistent_scoreboard(self):
        engine = GameEngine()
        # Simulate X winning round 1
        engine.board = [
            ['X', 'X', 'X'],
            [None, 'O', None],
            ['O', None, None]
        ]
        engine.check_round_end()
        self.assertEqual(engine.scores['X'], 1)

        # New round (R): score should persist
        engine.start_new_round()
        self.assertEqual(engine.scores['X'], 1)
        self.assertFalse(engine.round_over)
        self.assertIsNone(engine.winner)

        # Reset match (M): score should reset to 0
        engine.reset_match()
        self.assertEqual(engine.scores['X'], 0)
        self.assertEqual(engine.scores['O'], 0)
        self.assertEqual(engine.scores['Draw'], 0)

    def test_task3_move_validation(self):
        engine = GameEngine()
        engine.board[0][0] = 'O'
        engine.current_player = 'X'
        
        # Click on (0,0) which is already 'O'
        # Board top is 95, left is 30, cell size is 120
        engine.handle_click((40, 105)) # inside cell (0, 0)
        self.assertEqual(engine.board[0][0], 'O')
        self.assertEqual(engine.current_player, 'X')  # turn must not change!

    def test_task4_first_player_choice(self):
        engine = GameEngine()
        self.assertEqual(engine.starting_player, 'X')

        # Toggle first player to O
        engine.toggle_starting_player()
        self.assertEqual(engine.starting_player, 'O')

        # When starting with O, AI should have made the first move
        o_count = sum(row.count('O') for row in engine.board)
        self.assertEqual(o_count, 1)
        self.assertEqual(engine.current_player, 'X')


if __name__ == '__main__':
    unittest.main()
