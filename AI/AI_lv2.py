"""
AI_lv2.py - Implements an intermediate-level AI using minimax algorithm
This AI looks ahead a few moves to make more strategic decisions.
"""

from AI.AI_base import BaseAI
import random
import copy
from Jeux.pieces import PIECE_VALUES
from Jeux.board import Board

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
    
    def get_move(self, board:Board) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Use minimax to find the best move looking ahead a few moves.
        
        Args:
            board: The current board state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the chosen move
        """
        # Get all valid moves for the current player's pieces
        all_moves = self.get_all_valid_moves(self.color,board)
        
        if len(all_moves) == 0:
            return None  # No valid moves available
        
        best_score = float('-inf')
        best_moves = []  # Store all moves with the best score
        
        # Create a deep copy of the board to simulate moves
        board_copy = copy.deepcopy(board)
        for move in all_moves:
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos

            start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
            target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
            
            # Move the piece in the copied grid
            try:
                capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                if capture[1] == 'G' and capture[0] != self.color:
                    # If the move captures the general, it's a winning move
                    return move
            except Exception as e:
                continue  # Skip invalid moves

            # Evaluate this move using minimax
            score = self.minimax(board_copy, self.search_depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)  # Add equally good moves
                
            # Undo the move
            board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
            board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell
        
        
        # Choose randomly from the best moves
        if len(best_moves) > 0:
            return random.choice(best_moves)
        else:
            # Fallback: if minimax didn't yield good results, choose randomly
            return random.choice(all_moves) if all_moves else None
    
    def minimax(self, board: Board, depth: int, is_maximizing: bool) -> float:
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
        
        if depth == 0:
            return self.evaluate_board(board)
        
        # Get the current player's color
        current_color = self.color if is_maximizing else 'B' if self.color == 'W' else 'W'
        
        # Get all valid moves for the current player
        all_moves = self.get_all_valid_moves(current_color, board)
        
        # If no moves are available, this is a terminal state
        if len(all_moves) == 0:
            return 0  # Draw
        
        board_copy = copy.deepcopy(board)
        if is_maximizing:
            max_eval = float('-inf')
            for move in all_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                # Move the piece in the copied grid
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                except Exception as e:
                    continue
                # Evaluate this move using minimax                
                eval = self.minimax(board_copy, depth - 1, False)
                max_eval = max(max_eval, eval)
                # Undo the move
                board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell

            # If the AI is maximizing, return the best score
            return max_eval
        else:
            min_eval = float('inf')
            for move in all_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
                # Move the piece in the copied grid
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)

                except Exception as e:
                    continue
            
                eval = self.minimax(board_copy, depth - 1, True)
                min_eval = min(min_eval, eval)
            
                # Undo the move
                board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell

            # If the AI is minimizing, return the worst score
            return min_eval