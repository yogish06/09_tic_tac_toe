"""
GameEngine: owns the board, turn state, scoreboard, and round-end logic.

- Player always plays X (clicks to move).
- Computer always plays O (uses random-move AI).
- Tracks persistent match scoreboard across rounds.
- Allows first-player selection (X or O).
"""

import pygame
from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move

HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        # Persistent match state
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        self.starting_player = HUMAN_SYMBOL

        # Round state
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.starting_player
        self.round_over = False
        self.winner = None   # 'X', 'O', or None
        self._score_recorded = False

        # If computer is configured to start first
        self._maybe_take_computer_turn()

    def start_new_round(self):
        """Starts a new round while preserving the scoreboard."""
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.starting_player
        self.round_over = False
        self.winner = None
        self._score_recorded = False
        self._maybe_take_computer_turn()

    def reset_match(self):
        """Resets both the current round and the persistent scoreboard."""
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        self.start_new_round()

    def toggle_starting_player(self):
        """Toggles who starts the round between X and O."""
        self.starting_player = COMPUTER_SYMBOL if self.starting_player == HUMAN_SYMBOL else HUMAN_SYMBOL
        # If the round is not in progress (empty board or round over), apply immediately
        if self.round_over or all(cell is None for row in self.board for cell in row):
            self.start_new_round()

    def handle_click(self, pos):
        # Reject click if the round is already over or if it's not human's turn
        if self.round_over or self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)
        if cell is None:
            return

        row, col = cell

        # Move validation: Reject click if cell is already occupied
        if self.board[row][col] is not None:
            return

        # Place player's symbol
        self.board[row][col] = self.current_player
        self.check_round_end()

        # If game continues, hand turn over to computer
        if not self.round_over:
            self.current_player = COMPUTER_SYMBOL
            self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)
        if move is None:
            return

        row, col = move
        self.board[row][col] = self.current_player
        self.check_round_end()

        if not self.round_over:
            self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        if key == pygame.K_r:
            # R: New round (keeps scoreboard)
            self.start_new_round()
        elif key == pygame.K_m:
            # M: Reset match (clears scoreboard)
            self.reset_match()
        elif key in (pygame.K_f, pygame.K_t):
            # F / T: Toggle first player
            self.toggle_starting_player()
        elif key == pygame.K_x:
            self.starting_player = HUMAN_SYMBOL
            if self.round_over or all(cell is None for row in self.board for cell in row):
                self.start_new_round()
        elif key == pygame.K_o:
            self.starting_player = COMPUTER_SYMBOL
            if self.round_over or all(cell is None for row in self.board for cell in row):
                self.start_new_round()

    def check_round_end(self):
        # 1. Check for a winner first (so a winning last move is scored as win, not draw)
        winner = check_winner(self.board)
        if winner:
            self.round_over = True
            self.winner = winner
            if not self._score_recorded:
                self.scores[winner] += 1
                self._score_recorded = True
            return

        # 2. Check for a full board (draw)
        if is_board_full(self.board):
            self.round_over = True
            self.winner = None
            if not self._score_recorded:
                self.scores['Draw'] += 1
                self._score_recorded = True
            return

    def draw(self, surface, font, small_font=None):
        from game import renderer
        renderer.draw_board(surface, self.board)
        renderer.draw_scoreboard(surface, small_font or font, self.scores)

        if not self.round_over:
            turn_label = "Your turn (X)" if self.current_player == HUMAN_SYMBOL else "Computer's turn (O)..."
            renderer.draw_status(surface, font, turn_label)
        else:
            if self.winner:
                text = f"{self.winner} Wins!" if self.winner != HUMAN_SYMBOL else "You Win (X)!"
            else:
                text = "It's a Draw!"
            renderer.draw_banner(surface, font, text, winner=self.winner)

        renderer.draw_controls(surface, small_font or font, self.starting_player)
