"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 420, 550
BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_LEFT = (WIDTH - BOARD_SIZE) // 2
BOARD_TOP = 95
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (245, 247, 250)
COLOR_CARD = (255, 255, 255)
COLOR_LINE = (203, 213, 225)
COLOR_X = (225, 29, 72)     # Crimson / Rose
COLOR_O = (37, 99, 235)     # Royal Blue
COLOR_TEXT = (15, 23, 42)
COLOR_MUTED = (100, 116, 139)
COLOR_SUCCESS = (16, 185, 129)
COLOR_DRAW = (217, 119, 6)

_font_cache = {}


def _get_font(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        try:
            _font_cache[key] = pygame.font.SysFont("consolas", size, bold=bold)
        except Exception:
            _font_cache[key] = pygame.font.Font(None, size)
    return _font_cache[key]


def board_pos_to_cell(pos):
    x, y = pos
    x -= BOARD_LEFT
    y -= BOARD_TOP
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None
    col = int(x // CELL_SIZE)
    row = int(y // CELL_SIZE)
    if 0 <= row < 3 and 0 <= col < 3:
        return row, col
    return None


def draw_board(surface, board):
    surface.fill(COLOR_BG)

    # Board background card
    board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_SIZE, BOARD_SIZE)
    pygame.draw.rect(surface, COLOR_CARD, board_rect, border_radius=12)
    pygame.draw.rect(surface, COLOR_LINE, board_rect, width=2, border_radius=12)

    # Grid lines
    for i in range(1, 3):
        # Vertical lines
        x = BOARD_LEFT + i * CELL_SIZE
        pygame.draw.line(surface, COLOR_LINE, (x, BOARD_TOP + 8), (x, BOARD_TOP + BOARD_SIZE - 8), 3)
        # Horizontal lines
        y = BOARD_TOP + i * CELL_SIZE
        pygame.draw.line(surface, COLOR_LINE, (BOARD_LEFT + 8, y), (BOARD_LEFT + BOARD_SIZE - 8, y), 3)

    # Symbols
    for r in range(3):
        for c in range(3):
            symbol = board[r][c]
            if symbol is None:
                continue
            cx = BOARD_LEFT + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2
            if symbol == 'X':
                offset = CELL_SIZE // 3.2
                pygame.draw.line(surface, COLOR_X, (cx - offset, cy - offset), (cx + offset, cy + offset), 7)
                pygame.draw.line(surface, COLOR_X, (cx + offset, cy - offset), (cx - offset, cy + offset), 7)
            else:
                pygame.draw.circle(surface, COLOR_O, (cx, cy), int(CELL_SIZE // 3.2), 7)


def draw_scoreboard(surface, font, scores):
    # Top scoreboard container
    card_rect = pygame.Rect(BOARD_LEFT, 12, BOARD_SIZE, 38)
    pygame.draw.rect(surface, COLOR_CARD, card_rect, border_radius=8)
    pygame.draw.rect(surface, COLOR_LINE, card_rect, width=1, border_radius=8)

    score_font = _get_font(15, bold=True)
    text_x = f"X (You): {scores.get('X', 0)}"
    text_draw = f"Draws: {scores.get('Draw', 0)}"
    text_o = f"O (AI): {scores.get('O', 0)}"

    surf_x = score_font.render(text_x, True, COLOR_X)
    surf_draw = score_font.render(text_draw, True, COLOR_MUTED)
    surf_o = score_font.render(text_o, True, COLOR_O)

    surface.blit(surf_x, (BOARD_LEFT + 12, 22))
    surface.blit(surf_draw, (surface.get_width() // 2 - surf_draw.get_width() // 2, 22))
    surface.blit(surf_o, (BOARD_LEFT + BOARD_SIZE - surf_o.get_width() - 12, 22))


def draw_status(surface, font, text, color=COLOR_TEXT):
    f = font or _get_font(20, bold=True)
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(surface.get_width() // 2, 68))
    surface.blit(surf, rect)


def draw_banner(surface, font, text, winner=None):
    if winner == 'X':
        color = COLOR_X
    elif winner == 'O':
        color = COLOR_O
    else:
        color = COLOR_DRAW
    f = font or _get_font(20, bold=True)
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(surface.get_width() // 2, 68))
    surface.blit(surf, rect)


def draw_controls(surface, small_font, first_player):
    hint_round = "[R] New Round   |   [M] Reset Match"
    hint_first = f"[F] First: {first_player} (press F to change)"

    f = small_font or _get_font(13)
    surf_round = f.render(hint_round, True, COLOR_MUTED)
    surf_first = f.render(hint_first, True, COLOR_TEXT)

    r_rect = surf_round.get_rect(center=(surface.get_width() // 2, BOARD_TOP + BOARD_SIZE + 24))
    f_rect = surf_first.get_rect(center=(surface.get_width() // 2, BOARD_TOP + BOARD_SIZE + 48))

    surface.blit(surf_round, r_rect)
    surface.blit(surf_first, f_rect)
