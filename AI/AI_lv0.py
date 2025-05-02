"""
AI_lv0.py - Implements the simplest AI that makes random moves
This AI randomly selects from available valid moves without any strategy.
"""

import random
from AI.AI_base import BaseAI

class AI(BaseAI):
    """
    Level 0 AI - Makes completely random moves.
    This is the simplest AI implementation with no strategic considerations.
    """
    
    def __init__(self, color):
        """
        Initialize the Random AI.
        
        Args:
            color (str): The color of pieces the AI controls ('Red' or 'Black')
        """
        super().__init__(color)
        self.name = "Random AI (Level 0)"
    
    def get_move(self, game):
        """
        Select a random valid move.
        
        Args:
            game: The current game state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the chosen move
        """
        all_moves = self.get_all_valid_moves(game)
        
        if not all_moves:
            return None  # No valid moves available
            
        return random.choice(all_moves)
