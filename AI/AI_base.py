"""
AI_base.py - Base class for AI implementations in Vietnamese Chess
This module defines the base AI class with common functionality that
specific AI implementations can extend.
"""

from Jeux.moves import get_valid_moves
from Jeux.pieces import PIECE_VALUES
from Jeux.board import Board

class BaseAI:
    """
    Base class for AI implementations.
    
    This class provides common functionality for all AI levels and
    defines the interface that specific AI implementations should follow.
    """
    
    def __init__(self, color: str):
        """
        Initialize the AI with a specific color.
        
        Args:
            color (str): The color of pieces the AI controls ('White' or 'Black')
        """
        self.color = color[0].upper()  # Ensure color is uppercase
        self.name = "Base AI"
    
    def get_move(self, board: Board) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Determine the next move for the AI based on the current game state.
        This method should be overridden by specific AI implementations.
        
        Args:
            game: The current game state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the move
        """
        raise NotImplementedError("Specific AI implementations must override get_move")
    
    def get_all_valid_moves(self, color:str, board: Board)-> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Get all valid moves for the current player.
        
        Args:
            game: The current game state
            
        Returns:
            list: A list of tuples ((from_x, from_y), (to_x, to_y)) for all valid moves
        """
        all_moves = []
    
        for i in range(90):
            piece = board.grid[i]
            if piece != '  ' and piece[0] == color:
                # Get all valid moves for this piece
                piece_x, piece_y = board.to_2d(i)
                valid_moves = get_valid_moves(piece_x,piece_y, board)
                for move in valid_moves:
                    all_moves.append(((piece_x, piece_y), move))
        
        return all_moves
    
    def evaluate_board(self, board: Board)-> int:
        """
        Evaluate the current board position from the AI's perspective.
        Higher values are better for the AI.
        
        Args:
            board: The game board to evaluate
            
        Returns:
            int: A score representing how favorable the position is
        """
        # Simple evaluation: sum the values of all pieces on the board
        score = 0
        for i in range(90):
            piece = board.grid[i]
            if piece != '  ':
                # Add score for own pieces, subtract for opponent's
                multiplier = 1 if piece[0] == self.color else -1
                score += multiplier * PIECE_VALUES[piece[1]]
        
        return score