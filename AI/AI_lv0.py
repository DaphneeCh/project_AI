"""
AI_lv0.py - Implements the simplest AI that makes random moves
This AI randomly selects from available valid moves without any strategy.
"""

import random
from AI.AI_base import BaseAI
from Jeux.game import Game

class AI(BaseAI):
    """
    Level 0 AI - Makes completely random moves.
    This is the simplest AI implementation with no strategic considerations.
    """
    
    def __init__(self, color: str):
        """
        Initialize the Random AI.
        
        Args:
            color (str): The color of pieces the AI controls ('Red' or 'Black')
        """
        super().__init__(color)
        self.name = "Random AI (Level 0)"
    
    def get_move(self, game: Game)-> tuple[tuple[int, int], tuple[int, int]]:
        """
        Select a random valid move.
        
        Args:
            game: The current game state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the chosen move
        """
        all_moves = self.get_all_valid_moves(game)
        
        if len(all_moves) == 0:
            # No valid moves available
            return None
            
        return random.choice(all_moves)
