"""
board.py - Implements the game board for Vietnamese Chess (Cờ Tướng)
This module contains the Board class which manages the game grid, piece placement,
movement, and board state visualization.
"""

class Board:
    """
    Represents the game board with a 9x10 grid.
    
    The board is oriented with (0,0) at the top-left corner.
    Black pieces start at the top (rows 0-4) and White pieces at the bottom (rows 5-9).
    
    Attributes:
        grid (list): A 2D list representing the 9x10 board with pieces or None
    """
    def __init__(self):
        # Initialize a 1D list representing the 9x10 board (90 positions)
        self.grid = ['  '] * 90
        
        # Helper methods to convert between 1D and 2D coordinates
        self.to_1d = lambda x, y: y * 9 + x
        self.to_2d = lambda i: (i % 9, i // 9)
        self.place_initial_pieces()

    def place_initial_pieces(self):
        """
        Sets up the initial position of all pieces on the board according to
        traditional Vietnamese Chess rules.
        """
        # Place generals
        self.grid[self.to_1d(4, 0)] = 'BG'
        self.grid[self.to_1d(4, 9)] = 'WG'

        # Place advisors
        self.grid[self.to_1d(3, 0)] = 'BA'
        self.grid[self.to_1d(5, 0)] = 'BA'
        self.grid[self.to_1d(3, 9)] = 'WA'
        self.grid[self.to_1d(5, 9)] = 'WA'
        
        # Place elephants
        self.grid[self.to_1d(2, 0)] = 'BE'
        self.grid[self.to_1d(6, 0)] = 'BE'
        self.grid[self.to_1d(2, 9)] = 'WE'
        self.grid[self.to_1d(6, 9)] = 'WE'

        # Place horses
        self.grid[self.to_1d(1, 0)] = 'BH'
        self.grid[self.to_1d(7, 0)] = 'BH'
        self.grid[self.to_1d(1, 9)] = 'WH'
        self.grid[self.to_1d(7, 9)] = 'WH'
        
        # Place chariots
        self.grid[self.to_1d(0, 0)] = 'BR'
        self.grid[self.to_1d(8, 0)] = 'BR'
        self.grid[self.to_1d(0, 9)] = 'WR'
        self.grid[self.to_1d(8, 9)] = 'WR'

        # Place cannons
        self.grid[self.to_1d(1, 2)] = 'BC'
        self.grid[self.to_1d(7, 2)] = 'BC'
        self.grid[self.to_1d(1, 7)] = 'WC'
        self.grid[self.to_1d(7, 7)] = 'WC'

        # Place soldiers
        for i in range(0, 9, 2):
            self.grid[self.to_1d(i, 3)] = 'BS'
            self.grid[self.to_1d(i, 6)] = 'WS'

    def move_piece(self, curr_x: int, curr_y: int, new_x: int, new_y: int):
        """
        Moves a piece to a new position on the board.
        
        Args:
            curr_x (int): The current x-coordinate of the piece
            curr_y (int): The current y-coordinate of the piece
            new_x (int): The destination x-coordinate
            new_y (int): The destination y-coordinate
            
        Returns:
            capture (str or None): The captured piece, if any

        """
        capture = None
        curr_idx = self.to_1d(curr_x, curr_y)
        new_idx = self.to_1d(new_x, new_y)
        
        if self.grid[curr_idx] == '  ':  # Fixed comparison
            raise ValueError("No piece at the current position")
        if not self.is_in_bounds(new_x, new_y):
            raise ValueError("New position out of bounds")
            
        current_piece = self.grid[curr_idx]
        self.grid[curr_idx] = '  '
        capture = self.grid[new_idx]
        self.grid[new_idx] = current_piece
        
        return capture

    # def get_all_pieces(self, color: str)-> list:
    #     return [piece for row in self.grid for piece in row if piece and piece.color == color]

    def display(self):
        """
        Displays the current state of the board in a formatted grid.
        """
        # Center column headers above each cell
        print("  ", end="")
        for i in range(9):
            print(f"  {i}  ", end="")
        print()
        print("  +----+----+----+----+----+----+----+----+----+")
        
        for y in range(10):
            print(f"{y} |", end="")
            for x in range(9):
                piece = self.grid[self.to_1d(x, y)]
                piece_str = str(piece) if piece else "  "
                # Center the piece string in a 4-character space
                print(f"{piece_str:^4}", end="|")
            print()
            print("  +----+----+----+----+----+----+----+----+----+")
        print()

    def is_in_bounds(self, x:int, y:int)-> bool:
        return 0 <= x < 9 and 0 <= y < 10

    def is_general_facing_general(self)-> bool:
        # Find both generals
        white_general = None
        black_general = None
        
        for i in range(90):
            piece = self.grid[i]
            if piece == 'WG':
                white_general = self.to_2d(i)
            elif piece == 'BG':
                black_general = self.to_2d(i)
        
        if not white_general or not black_general:
            return False
            
        # Check if they are in the same column
        if white_general[0] != black_general[0]:
            return False
        
        x = white_general[0]
        # Check if there are any pieces between them
        min_y = min(white_general[1], black_general[1])  # Fixed tuple access
        max_y = max(white_general[1], black_general[1])  # Fixed tuple access
        
        for y in range(min_y + 1, max_y):
            if self.grid[self.to_1d(x, y)] != '  ':  # Fixed comparison
                # There is a piece blocking the line of sight
                return False
                
        return True
    
    def _hash_board(self) -> str:
        """
        Create a simple hash of the current board state for the transposition table.
        
        Args:
            board: Current board state
            
        Returns:
            str: A hash string representing the board state
        """
        return "|".join(self.grid)
    
    def to_string(self) -> str:
        """
        Convert the board to a string representation.
        
        Returns:
            str: A string representation of the board
        """
        return self._hash_board()