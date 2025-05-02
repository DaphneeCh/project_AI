"""
AI_base.py - Base class for AI implementations in Vietnamese Chess
This module defines the base AI class with common functionality that
specific AI implementations can extend.
"""

from Jeux.moves import get_valid_moves

class BaseAI:
    """
    Base class for AI implementations.
    
    This class provides common functionality for all AI levels and
    defines the interface that specific AI implementations should follow.
    """
    
    def __init__(self, color):
        """
        Initialize the AI with a specific color.
        
        Args:
            color (str): The color of pieces the AI controls ('Red' or 'Black')
        """
        self.color = color
        self.name = "Base AI"
    
    def get_move(self, game):
        """
        Determine the next move for the AI based on the current game state.
        This method should be overridden by specific AI implementations.
        
        Args:
            game: The current game state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the move
        """
        raise NotImplementedError("Specific AI implementations must override get_move")
    
    def get_all_valid_moves(self, game):
        """
        Get all valid moves for the current player.
        
        Args:
            game: The current game state
            
        Returns:
            list: A list of tuples ((from_x, from_y), (to_x, to_y)) for all valid moves
        """
        all_moves = []
        pieces = game.board.get_all_pieces(self.color)
        
        for piece in pieces:
            valid_moves = get_valid_moves(piece, game.board)
            for move in valid_moves:
                all_moves.append(((piece.x, piece.y), move))
        
        return all_moves
    
    def evaluate_board(self, board):
        """
        Evaluate the current board position from the AI's perspective.
        Higher values are better for the AI.
        
        Args:
            board: The game board to evaluate
            
        Returns:
            int: A score representing how favorable the position is
        """
        from Jeux.pieces import PIECE_VALUES
        
        score = 0
        for y in range(10):
            for x in range(9):
                piece = board.grid[y][x]
                if piece:
                    # Add score for own pieces, subtract for opponent's
                    multiplier = 1 if piece.color == self.color else -1
                    score += multiplier * PIECE_VALUES.get(piece.type, 0)
        
        return score