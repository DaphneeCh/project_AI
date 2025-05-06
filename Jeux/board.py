"""
board.py - Implements the game board for Vietnamese Chess (Cờ Tướng)
This module contains the Board class which manages the game grid, piece placement,
movement, and board state visualization.
"""

from Jeux.pieces import Piece

class Board:
    """
    Represents the game board with a 9x10 grid.
    
    The board is oriented with (0,0) at the top-left corner.
    Black pieces start at the top (rows 0-4) and White pieces at the bottom (rows 5-9).
    
    Attributes:
        grid (list): A 2D list representing the 9x10 board with pieces or None
    """
    def __init__(self):
        self.grid = [[None for _ in range(9)] for _ in range(10)]
        self.place_initial_pieces()

    def place_initial_pieces(self):
        """
        Sets up the initial position of all pieces on the board according to
        traditional Vietnamese Chess rules.
        """
        # Place generals
        self.grid[0][4] = Piece('General', 'Black', 4, 0)
        self.grid[9][4] = Piece('General', 'White', 4, 9)

        # Place advisors
        self.grid[0][3] = Piece('Advisor', 'Black', 3, 0)
        self.grid[0][5] = Piece('Advisor', 'Black', 5, 0)
        self.grid[9][3] = Piece('Advisor', 'White', 3, 9)
        self.grid[9][5] = Piece('Advisor', 'White', 5, 9)

        # Place elephants
        self.grid[0][2] = Piece('Elephant', 'Black', 2, 0)
        self.grid[0][6] = Piece('Elephant', 'Black', 6, 0)
        self.grid[9][2] = Piece('Elephant', 'White', 2, 9)
        self.grid[9][6] = Piece('Elephant', 'White', 6, 9)

        # Place horses
        self.grid[0][1] = Piece('Horse', 'Black', 1, 0)
        self.grid[0][7] = Piece('Horse', 'Black', 7, 0)
        self.grid[9][1] = Piece('Horse', 'White', 1, 9)
        self.grid[9][7] = Piece('Horse', 'White', 7, 9)

        # Place chariots
        self.grid[0][0] = Piece('Chariot', 'Black', 0, 0)
        self.grid[0][8] = Piece('Chariot', 'Black', 8, 0)
        self.grid[9][0] = Piece('Chariot', 'White', 0, 9)
        self.grid[9][8] = Piece('Chariot', 'White', 8, 9)

        # Place cannons
        self.grid[2][1] = Piece('Cannon', 'Black', 1, 2)
        self.grid[2][7] = Piece('Cannon', 'Black', 7, 2)
        self.grid[7][1] = Piece('Cannon', 'White', 1, 7)
        self.grid[7][7] = Piece('Cannon', 'White', 7, 7)

        # Place soldiers
        for i in range(0, 9, 2):
            self.grid[3][i] = Piece('Soldier', 'Black', i, 3)
            self.grid[6][i] = Piece('Soldier', 'White', i, 6)

        # Update coordinates for all pieces
        for y in range(10):
            for x in range(9):
                if self.grid[y][x]:
                    self.grid[y][x].x = x
                    self.grid[y][x].y = y

    def move_piece(self, piece: Piece, new_x: int, new_y: int):
        """
        Moves a piece to a new position on the board.
        
        Args:
            piece (Piece): The piece to move
            new_x (int): The destination x-coordinate
            new_y (int): The destination y-coordinate
            
        Returns:
            Piece or None: The captuWhite piece if any, otherwise None
        """
        self.grid[piece.y][piece.x] = None
        captuWhite = self.grid[new_y][new_x]
        piece.x, piece.y = new_x, new_y
        self.grid[new_y][new_x] = piece
        return captuWhite

    def get_all_pieces(self, color: str)-> list:
        return [piece for row in self.grid for piece in row if piece and piece.color == color]

    def display(self):
        # Center column headers above each cell
        print("  ", end="")
        for i in range(9):
            print(f"  {i}  ", end="")
        print()
        print("  +----+----+----+----+----+----+----+----+----+")
        for y, row in enumerate(self.grid):
            print(f"{y} |", end="")
            for piece in row:
                piece_str = str(piece) if piece else "  "
                # Center the piece string in a 5-character space
                print(f"{piece_str:^4}", end="|")
            print()
            print("  +----+----+----+----+----+----+----+----+----+")
        print()

    def is_in_bounds(self, x:int, y:int)-> bool:
        return 0 <= x < 9 and 0 <= y < 10

    def is_general_facing_general(self)-> bool:
        # Find both generals
        White_general = None
        black_general = None
        
        for row in self.grid:
            for piece in row:
                if piece and piece.type == 'General':
                    if piece.color == 'White':
                        White_general = piece
                    else:
                        black_general = piece
        
        if not White_general or not black_general:
            return False
            
        # Check if they are in the same column
        if White_general.x != black_general.x:
            return False
            
        # Check if there are any pieces between them
        min_y = min(White_general.y, black_general.y)
        max_y = max(White_general.y, black_general.y)
        
        for y in range(min_y + 1, max_y):
            if self.grid[y][White_general.x] is not None:
                # There is a piece blocking the line of sight
                return False
                
        return True