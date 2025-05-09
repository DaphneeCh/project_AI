"""
AI_lv1.py - Implements a beginner-level AI that prioritizes capturing opponent pieces
This AI uses a simple greedy approach to select moves that capture the highest-value pieces.
"""

from AI.AI_base import BaseAI
import random
from Jeux.board import Board
from Jeux.pieces import PIECE_VALUES

class AI(BaseAI):
    """
    Level 1 AI - Uses a simple greedy strategy.
    This AI prioritizes capturing opponent pieces, especially high-value ones.
    """
    
    def __init__(self, color: str):
        """
        Initialize the Beginner AI.
        
        Args:
            color (str): The color of pieces the AI controls ('Red' or 'Black')
        """
        super().__init__(color)
        self.name = "Beginner AI (Level 1)"
    
    def get_move(self, board: Board)-> tuple[tuple[int, int], tuple[int, int]]:
        """
        Select a move prioritizing captures of high-value pieces.
        
        Args:
            game: The current game state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the chosen move
        """
        all_moves = self.get_all_valid_moves(self.color,board)
        
        if len(all_moves) == 0:
            return None  # No valid moves available
        
        # Calculate the value of each move
        valued_moves = []
        for move in all_moves:
            # move is a tuple of ((from_x, from_y), (to_x, to_y))
            from_pos, to_pos = move
            # from_pos and to_pos are tuples (x, y)
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            # Check if we're capturing a piece
            target_piece = board.grid[board.to_1d(to_x, to_y)]
            
            if target_piece != '  ':
                if target_piece[0] != self.color:
                    # Higher score for capturing higher-value pieces
                    capture_value = PIECE_VALUES[target_piece[1]]  # Get the value of the captured piece
                    valued_moves.append((move, capture_value))
            else:
                # No capture
                valued_moves.append((move, 0))
        
        # Sort moves by value (highest first)
        valued_moves.sort(key=lambda x: x[1], reverse=True)
        
        # If there are captures available, select the highest-value one
        if valued_moves[0][1] > 0:
            return valued_moves[0][0]
        
        # Otherwise, make a random move
        return random.choice(all_moves)