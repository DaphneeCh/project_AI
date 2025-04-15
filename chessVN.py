# Core implementation of Co Tuong (Vietnamese Chess)

import random

# Define piece types and values
PIECE_VALUES = {
    'General': 1000,
    'Chariot': 90,
    'Cannon': 60,
    'Horse': 45,
    'Elephant': 30,
    'Advisor': 25,
    'Soldier': 10
}

class Piece:
    def __init__(self, type, color, x, y):
        self.type = type
        self.color = color  # 'Red' or 'Black'
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.color[0]}_{self.type[0:2]}"

# Board: 9 columns x 10 rows
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(9)] for _ in range(10)]
        self.place_initial_pieces()

    def place_initial_pieces(self):
        # Place generals
        self.grid[0][4] = Piece('General', 'Black', 4, 0)
        self.grid[9][4] = Piece('General', 'Red', 4, 9)

        # Place chariots
        self.grid[0][0] = self.grid[0][8] = Piece('Chariot', 'Black', 0, 0)
        self.grid[9][0] = self.grid[9][8] = Piece('Chariot', 'Red', 0, 9)

        # Place cannons
        self.grid[2][1] = self.grid[2][7] = Piece('Cannon', 'Black', 1, 2)
        self.grid[7][1] = self.grid[7][7] = Piece('Cannon', 'Red', 1, 7)

        # Add more pieces as needed
        # For simplicity, only a subset is placed

    def move_piece(self, piece, new_x, new_y):
        self.grid[piece.y][piece.x] = None
        captured = self.grid[new_y][new_x]
        piece.x, piece.y = new_x, new_y
        self.grid[new_y][new_x] = piece
        return captured

    def get_all_pieces(self, color):
        return [piece for row in self.grid for piece in row if piece and piece.color == color]

    def display(self):
        for row in self.grid:
            print(' '.join([str(p) if p else '--' for p in row]))
        print("\n")

# Example: get all legal moves (stub for now)
def get_valid_moves(piece, board):
    moves = []
    x, y = piece.x, piece.y
    # Only implement General moves as example
    if piece.type == 'General':
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 3 <= nx <= 5 and ((0 <= ny <= 2 and piece.color == 'Black') or (7 <= ny <= 9 and piece.color == 'Red')):
                target = board.grid[ny][nx]
                if not target or target.color != piece.color:
                    moves.append((nx, ny))
    return moves

# Simple random AI
def get_random_move(board, color):
    pieces = board.get_all_pieces(color)
    random.shuffle(pieces)
    for piece in pieces:
        valid_moves = get_valid_moves(piece, board)
        if valid_moves:
            move = random.choice(valid_moves)
            return piece, move
    return None, None

# Demo game setup
board = Board()
board.display()

# Make a random move for Red
piece, move = get_random_move(board, 'Red')
if piece and move:
    print(f"Red moves {piece} to {move}")
    board.move_piece(piece, *move)
    board.display()
