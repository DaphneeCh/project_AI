"""
pieces.py - Defines the pieces used in Vietnamese Chess (Cờ Tướng)
This module contains the Piece class and piece value constants used throughout the game.
"""

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
    """
    Represents a chess piece on the board.
    
    Attributes:
        type (str): The type of piece (General, Advisor, Elephant, etc.)
        color (str): The color of the piece ('White' or 'Black')
        x (int): The x-coordinate (column) of the piece on the board
        y (int): The y-coordinate (row) of the piece on the board
    """
    def __init__(self, type: str, color: str, x: int, y: int):
        self.type = type
        self.color = color  # 'White' or 'Black'
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.color[0]}_{self.type[0:2]}"