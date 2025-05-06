"""
AI_lv2.py - Implements an intermediate-level AI using minimax algorithm
This AI looks ahead a few moves to make more strategic decisions.
"""

from AI.AI_base import BaseAI
import random
import copy
from Jeux.game import Game
from Jeux.moves import get_valid_moves

class AI(BaseAI):
    """
    Level 2 AI - Uses minimax algorithm with limited depth.
    This AI looks ahead a few moves to make better strategic decisions.
    """
    
    def __init__(self, color: str):
        """
        Initialize the Intermediate AI.
        
        Args:
            color (str): The color of pieces the AI controls ('Red' or 'Black')
        """
        super().__init__(color)
        self.name = "Intermediate AI (Level 2)"
        self.search_depth = 2  # Look ahead 5 moves
    
    def get_move(self, game:Game) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Use minimax to find the best move looking ahead a few moves.
        
        Args:
            game: The current game state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the chosen move
        """
        # Get all valid moves for the current player's pieces
        all_moves = self.get_all_valid_moves(game)
        
        if len(all_moves) == 0:
            return None  # No valid moves available
        
        best_score = float('-inf')
        best_moves = []  # Store all moves with the best score
        
        for move in all_moves:
            # Create a deep copy of the game to simulate moves
            game_copy = copy.deepcopy(game)
            from_pos, to_pos = move
            
            # Double check that there's a piece at the source position before moving
            from_x, from_y = from_pos
            if game_copy.board.grid[from_y][from_x] is None:
                continue  # Skip this move if there's no piece
                
            # Make the move on the copy
            success, _ = game_copy.make_move(from_pos, to_pos)
            if not success:
                continue  # Skip if the move was invalid
            
            # Evaluate this move using minimax
            score = self.minimax(game_copy, self.search_depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)  # Add equally good moves
        
        # Choose randomly from the best moves
        if len(best_moves) > 0:
            return random.choice(best_moves)
        else:
            # Fallback: if minimax didn't yield good results, choose randomly
            return random.choice(all_moves) if all_moves else None
    
    def minimax(self, game: Game, depth: int, is_maximizing: bool) -> float:
        """
        Minimax algorithm implementation.
        
        Args:
            game: Current game state
            depth: How many more layers to search
            is_maximizing: True if it's the maximizing player's turn (AI's turn)
            
        Returns:
            float: Score for this game state
        """
        # Terminal conditions
        if game.game_over:
            return 1000 if game.winner == self.color else -1000
        
        if depth == 0:
            return self.evaluate_board(game.board)
        
        # Get the current player's color
        current_color = game.current_player
        
        # Get all valid moves for the current player
        all_moves = []
        pieces = game.board.get_all_pieces(current_color)
        
        for piece in pieces:
            valid_destinations = get_valid_moves(piece, game.board)
            for dest in valid_destinations:
                all_moves.append(((piece.x, piece.y), dest))
        
        # If no moves are available, this is a terminal state
        if len(all_moves) == 0:
            return 0  # Draw
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in all_moves:
                game_copy = copy.deepcopy(game)
                from_pos, to_pos = move
                
                # Verify the piece exists before moving
                from_x, from_y = from_pos
                if game_copy.board.grid[from_y][from_x] is None:
                    continue
                
                success, _ = game_copy.make_move(from_pos, to_pos)
                if success:  # Only evaluate valid moves
                    eval = self.minimax(game_copy, depth - 1, False)
                    max_eval = max(max_eval, eval)
            
            return max_eval
        else:
            min_eval = float('inf')
            for move in all_moves:
                game_copy = copy.deepcopy(game)
                from_pos, to_pos = move
                
                # Verify the piece exists before moving
                from_x, from_y = from_pos
                if game_copy.board.grid[from_y][from_x] is None:
                    continue
                
                success, _ = game_copy.make_move(from_pos, to_pos)
                if success:  # Only evaluate valid moves
                    eval = self.minimax(game_copy, depth - 1, True)
                    min_eval = min(min_eval, eval)
            
            return min_eval