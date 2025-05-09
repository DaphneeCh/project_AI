"""
AI_optimal.py - Implements an advanced AI using minimax with alpha-beta pruning
This AI uses advanced techniques to find optimal moves in the Vietnamese Chess game.
"""

from AI.AI_base import BaseAI
import random
import copy
from Jeux.pieces import PIECE_VALUES
from Jeux.board import Board
from Jeux.moves import get_valid_moves

class AI(BaseAI):
    """
    Optimal AI - Makes moves using minimax algorithm with alpha-beta pruning.
    This AI uses advanced heuristics and optimization techniques for stronger play.
    """
    
    def __init__(self, color: str):
        """
        Initialize the Optimal AI.
        
        Args:
            color (str): The color of pieces the AI controls ('White' or 'Black')
        """
        super().__init__(color)
        self.name = "Optimal AI (Advanced)"
        self.search_depth = 3 # Look ahead 3 moves
    
    def get_move(self, board: Board) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """
        Select a move using the minimax algorithm with alpha-beta pruning.
        
        Args:
            board: The current board state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the chosen move
        """
        
        # Get all valid moves for the current player's pieces
        all_moves = self.get_all_valid_moves(self.color, board)
        
        if len(all_moves) == 0:
            return None  # No valid moves available
        
        # If there's only one move, return it immediately
        if len(all_moves) == 1:
            return all_moves[0]
        
        # Initialize variables for the best move
        best_moves = []
        best_score = float('-inf')
        
        # Order moves by a simple heuristic for better pruning
        ordered_moves = self._order_moves(all_moves, board)

        # Create a deep copy of the board to simulate the move
        board_copy = copy.deepcopy(board)
        for move in ordered_moves:
            # Make the move on the board copy
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
                
            start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
            target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
            # Move on the copied board
            try:
                capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                if capture[1] == 'G' and capture[0] != self.color:
                    # Immediately return a move that captures the opponent's general
                    return move
            except Exception as e:
                continue
                
            # Use minimax with alpha-beta pruning to evaluate
            score = self._alpha_beta(board_copy, self.search_depth - 1, float('-inf'), float('inf'), False)
                
            # Check if this move is better
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
                
            # Undo the move
            board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
            board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell
                
        # Return a random move from the best ones (in case of ties)
        if len(best_moves)>0:
            return random.choice(best_moves)
        else:
            # Fallback to a random move if something went wrong
            return random.choice(all_moves)
    
    def _order_moves(self, moves: list, board: Board) -> list:
        """
        Order moves to improve alpha-beta pruning efficiency.
        Capturing moves and center moves are checked first.
        
        Args:
            moves: List of possible moves
            board: Current board state
            
        Returns:
            list: Ordered list of moves
        """
        move_values = []
        
        for move in moves:
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            # Start with base value
            value = 0
            
            # Check if it's a capture
            source = board.grid[board.to_1d(from_x, from_y)]
            target = board.grid[board.to_1d(to_x, to_y)]
            if target != '  ' and target[0] != source[0]:
                # Value based on piece type
                piece_type = target[1]
                value = PIECE_VALUES[piece_type]
                    
            # Add to the list
            move_values.append((value, move))
        
        # Sort moves by value (highest first)
        move_values.sort(key=lambda x: x[0], reverse=True)
        
        # Return just the moves
        return [move for _, move in move_values]
    
    def _alpha_beta(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: Current board state
            depth: How many moves to look ahead
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: Whether we're maximizing or minimizing
            current_color: Current player's color
            
        Returns:
            float: Score for the current board position
        """
        
        # Base case: reached depth limit or game over
        if depth == 0:
            eval_score = self.evaluate_board(board)
            return eval_score
        
        # get the current player's color
        current_color = self.color if is_maximizing else 'B' if self.color == 'W' else 'W'

        # Get all possible moves for current player
        all_possible_moves = self.get_all_valid_moves(current_color, board)
        
        # No moves available (stalemate)
        if len(all_possible_moves) == 0:
            return 0
        
        # Order moves for better pruning
        ordered_moves = self._order_moves(all_possible_moves, board)
        
        board_copy = copy.deepcopy(board)
        if is_maximizing:
            best_score = float('-inf')
            for move in ordered_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Save original board state
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
                # Make move
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                    if capture[1] == 'G' and capture[0] != current_color:
                        # Return a high score for capturing the general
                        return 10000
                except Exception as e:
                    continue
                
                # Recursively evaluate this move
                score = self._alpha_beta(board_copy, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                
                # Undo move on the copied board
                board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell
                
                if best_score >= beta:
                    break  # Beta cutoff
                # Alpha update
                alpha = max(alpha, best_score)
                
            return best_score
        else:
            best_score = float('inf')
            for move in all_possible_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Save original board state
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
                # Make move
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                    if capture[1] == 'G' and capture[0] != current_color:
                        # Return a high score for capturing the general
                        return -10000
                except Exception:
                    continue
                
                # Recursively evaluate this move
                score = self._alpha_beta(board_copy, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                
                # Undo move on the copied board
                board_copy.grid[board.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board.to_1d(to_x, to_y)] = target_cell
                
                if best_score < alpha:
                    break  # Alpha cutoff
                # Beta update
                beta = min(beta, best_score)
                
            return best_score
    
    # def evaluate_board(self, board):
    #     """
    #     Advanced evaluation of the board position from AI's perspective.
    #     Higher values are better for the AI.
        
    #     Args:
    #         board: The game board to evaluate
            
    #     Returns:
    #         float: A score representing how favorable the position is
    #     """
    #     material_score = 0
    #     positional_score = 0
    #     mobility_score = 0
        
    #     # Material evaluation
    #     for idx in range(len(board.grid)):
    #         piece = board.grid[idx]
    #         if piece != '  ':
    #             # Base material value of the piece
    #             piece_color, piece_type = piece[0], piece[1]
    #             piece_value = PIECE_VALUES[piece_type]
    #             multiplier = 1 if piece_color == self.color else -1
    #             material_score += multiplier * piece_value
        
    #     # Check for checkmate conditions - this is simplified
    #     # We don't have an easy way to check for checkmate, so we'll just check
    #     # if either general is missing
        
    #     ai_has_general = False
    #     opponent_has_general = False
        
    #     for idx in range(len(board.grid)):
    #         piece = board.grid[idx]
    #         if piece and piece[1] == 'G':
    #             if piece[0] == self.color:
    #                 ai_has_general = True
    #             else:
    #                 opponent_has_general = True
        
    #     if not opponent_has_general:
    #         return 10000  # AI has won
    #     if not ai_has_general:
    #         return -10000  # AI has lost
        
    #     # Mobility evaluation
    #     # Count the number of valid moves for each piece
    #     for idx in range(len(board.grid)):
    #         piece = board.grid[idx]
    #         if piece and piece[0] == self.color:
    #             from_x, from_y = board.to_2d(idx)
    #             valid_moves = get_valid_moves(from_x, from_y, board)
    #             mobility_score += len(valid_moves)
            
            
    #     # Final score focusing primarily on material advantage
    #     return material_score + positional_score + mobility_score

