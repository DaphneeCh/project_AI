"""
pieces.py - Defines the pieces used in Vietnamese Chess (Cờ Tướng)
This module contains the Piece class and piece value constants used throughout the game.
"""

# Define piece types and values
PIECE_VALUES = {
    'General': 10000,
    'Rook': 9,
    'Cannon': 4.5,
    'Horse': 4,
    'Elephant': 2,
    'Advisor': 2,
    'Soldier': 1,
    # define value for each piece's acronyms
    'G': 10000,
    'R': 9,
    'C': 4.5,
    'H': 4,
    'E': 2,
    'A': 2,
    'S': 1
}

# Define piece types
PIECE_TYPES = {
    'General': 'G',
    'Rook': 'R',
    'Cannon': 'C',
    'Horse': 'H',
    'Elephant': 'E',
    'Advisor': 'A',
    'Soldier': 'S',
    'White': 'W',
    'Black': 'B'
}
PIECE_TYPES_REVERSE = {v: k for k, v in PIECE_TYPES.items()}

# Dictionary of piece symbols and their explanations
PIECE_SYMBOLS = {
    "R": "Rook (Xe): Moves horizontally or vertically any number of spaces.",
    "C": "Cannon (Pháo): Moves like a Chariot but captures by jumping over one piece.",
    "H": "Horse (Mã): Move in an 'L' shape, two squares in one direction and one square perpendicular. If there is another piece standing at the intersection adjacent to the vertical or horizontal step, the Horse is blocked and cannot move.",
    "E": "Elephant (Tượng): Moves diagonally two spaces, cannot cross the river. If there is another piece standing in the middle of that diagonal line, the Elephant is blocked and cannot move.",
    "A": "Advisor (Sĩ): Moves one space diagonally, restricted to the palace.",
    "G": "General (Tướng): Moves one space in any direction, restricted to the palace. Two Generals cannot face each other directly on the same line. If they do, there must be a piece from either side blocking their view.",
    "S": "Soldier (Binh): Moves one space forward, can move sideways after crossing the river.",
}
