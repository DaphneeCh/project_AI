"""
AI_optimal.py - Implements an advanced AI using minimax with alpha-beta pruning
This AI uses advanced techniques to find optimal moves in the Vietnamese Chess game.
"""

import random
import time
import copy
from AI.AI_base import BaseAI
from Jeux.pieces import PIECE_VALUES
from Jeux.board import Board
from Jeux.pieces import Piece

class AI(BaseAI):
    """
    Optimal AI - Makes moves using minimax algorithm with alpha-beta pruning.
    This AI uses advanced heuristics and optimization techniques for stronger play.
    """
    
    def __init__(self, color):
        """
        Initialize the Optimal AI.
        
        Args:
            color (str): The color of pieces the AI controls ('Red' or 'Black')
        """
        super().__init__(color)
        self.name = "Optimal AI (Advanced)"
        self.max_depth = 6  # Look ahead 4 moves
        self.max_time = 5.0  # Maximum thinking time in seconds
        self.transposition_table = {}  # For caching evaluated positions
        
        # Position value tables to encourage better piece positions
        self.position_tables = {
            'General': [
                # Generals should stay in the palace
                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 2, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 2, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0]
            ],
            'Chariot': [
                # Chariots are better at the edges and in open lines
                [9, 9, 9, 9, 9, 9, 9, 9, 9],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [7, 7, 7, 7, 7, 7, 7, 7, 7],
                [6, 6, 6, 6, 6, 6, 6, 6, 6],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [6, 6, 6, 6, 6, 6, 6, 6, 6],
                [7, 7, 7, 7, 7, 7, 7, 7, 7],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [9, 9, 9, 9, 9, 9, 9, 9, 9]
            ],
            'Soldier': [
                # Soldiers get more valuable as they advance
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2],
                [3, 3, 3, 3, 3, 3, 3, 3, 3],
                [4, 4, 4, 4, 4, 4, 4, 4, 4],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [6, 6, 6, 6, 6, 6, 6, 6, 6],
                [7, 7, 7, 7, 7, 7, 7, 7, 7],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [9, 9, 9, 9, 9, 9, 9, 9, 9],
                [10, 10, 10, 10, 10, 10, 10, 10, 10]
            ]
        }
    
    def get_move(self, game):
        """
        Select a move using the minimax algorithm with alpha-beta pruning.
        
        Args:
            game: The current game state
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) representing the chosen move
        """
        from Jeux.moves import get_valid_moves
        
        self.start_time = time.time()
        self.transposition_table = {}  # Clear cache for new search
        
        # Double-check that we're only considering valid moves with actual pieces
        all_moves = []
        pieces = game.board.get_all_pieces(self.color)
        
        for piece in pieces:
            # Make sure the piece actually exists at the reported position
            if game.board.grid[piece.y][piece.x] != piece:
                continue
            
            valid_destinations = get_valid_moves(piece, game.board)
            for dest_x, dest_y in valid_destinations:
                # Skip moves where destination is the same as source
                if dest_x == piece.x and dest_y == piece.y:
                    continue
                all_moves.append(((piece.x, piece.y), (dest_x, dest_y)))
        
        if not all_moves:
            return None  # No valid moves available
        
        # If there's only one move, return it immediately
        if len(all_moves) == 1:
            return all_moves[0]
        
        # Iterative deepening - start with shallow search and go deeper
        best_moves = []  # Initialize with all moves in case we run out of time immediately
        best_score = float('-inf')
        
        for current_depth in range(1, self.max_depth + 1):
            # Break if we're getting close to our time limit
            if time.time() - self.start_time > self.max_time * 0.8:
                break
                
            depth_best_moves = []
            depth_best_score = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            
            # Order moves by a simple heuristic for better pruning
            ordered_moves = self._order_moves(all_moves, game.board)
            
            for move in ordered_moves:
                # Create a deep copy of the board to simulate the move
                board_copy = copy.deepcopy(game.board)
                
                # Make the move on the board copy
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Get the piece from the original board to check if it exists
                piece = game.board.grid[from_y][from_x]
                if not piece:
                    continue  # Skip if there's no piece
                
                # Move on the copied board
                piece_copy = board_copy.grid[from_y][from_x]
                board_copy.grid[to_y][to_x] = piece_copy
                board_copy.grid[from_y][from_x] = None
                piece_copy.x = to_x
                piece_copy.y = to_y
                
                # Use minimax with alpha-beta pruning to evaluate
                opponent_color = 'Black' if self.color == 'Red' else 'Red'
                score = self._alpha_beta(board_copy, current_depth - 1, alpha, beta, False, opponent_color)
                
                # Check if this move is better
                if score > depth_best_score:
                    depth_best_score = score
                    depth_best_moves = [move]
                elif score == depth_best_score:
                    depth_best_moves.append(move)
                
                alpha = max(alpha, depth_best_score)
                
                # If we're running out of time, break early
                if time.time() - self.start_time > self.max_time:
                    break
            
            # Update overall best moves if we completed this depth
            if depth_best_moves and time.time() - self.start_time <= self.max_time:
                best_moves = depth_best_moves
                best_score = depth_best_score
        
        # Prioritize capturing opponent's general if possible
        for move in best_moves:
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            target = game.board.grid[to_y][to_x]
            if target and target.type == 'General':
                return move
        
        # Return a random move from the best ones (in case of ties)
        if best_moves:
            return random.choice(best_moves)
        else:
            # Fallback to a random move if something went wrong
            return random.choice(all_moves)
    
    def _order_moves(self, moves, board):
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
            target = board.grid[to_y][to_x]
            if target:
                value = 10 * PIECE_VALUES.get(target.type, 0)
                
                # Extra bonus for capturing the general
                if target.type == 'General':
                    value = 10000
            
            # Consider center control
            center_bonus = 0
            if 2 <= to_x <= 6 and 3 <= to_y <= 6:
                center_bonus = 5
            
            value += center_bonus
            
            # Add to the list
            move_values.append((value, move))
        
        # Sort moves by value (highest first)
        move_values.sort(reverse=True)
        
        # Return just the moves
        return [move for _, move in move_values]
    
    def _alpha_beta(self, board, depth, alpha, beta, is_maximizing, current_color):
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
        # Check time limit
        if time.time() - self.start_time > self.max_time:
            return self.evaluate_board(board) if is_maximizing else -self.evaluate_board(board)
        
        # Create a hash for the current board state (for transposition table)
        board_hash = self._hash_board(board)
        
        # Check if we've already evaluated this position
        if board_hash in self.transposition_table:
            cached_depth, cached_score = self.transposition_table[board_hash]
            if cached_depth >= depth:
                return cached_score
        
        # Base case: reached depth limit or game over
        if depth == 0:
            eval_score = self.evaluate_board(board)
            self.transposition_table[board_hash] = (0, eval_score)
            return eval_score
        
        # Check for win condition
        if self._is_game_over(board):
            if is_maximizing:
                return float('-inf')  # Opponent won
            else:
                return float('inf')   # AI won
        
        # Get all pieces for the current player
        from Jeux.moves import get_valid_moves
        
        all_possible_moves = []
        for y in range(10):
            for x in range(9):
                piece = board.grid[y][x]
                if piece and piece.color == current_color:
                    valid_moves = get_valid_moves(piece, board)
                    for move in valid_moves:
                        all_possible_moves.append(((piece.x, piece.y), move))
        
        # No moves available (stalemate)
        if not all_possible_moves:
            return 0
        
        # Order moves for better pruning
        ordered_moves = self._order_moves(all_possible_moves, board)
        
        if is_maximizing:
            best_score = float('-inf')
            for move in ordered_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Create a deep copy of the board for this move
                board_copy = self._deep_copy_board(board)
                
                # Move the piece on the copied board
                piece_copy = board_copy.grid[from_y][from_x]
                if piece_copy:  # Make sure the piece exists
                    board_copy.grid[to_y][to_x] = piece_copy
                    board_copy.grid[from_y][from_x] = None
                    piece_copy.x = to_x
                    piece_copy.y = to_y
                else:
                    continue  # Skip this move if piece doesn't exist
                
                # Recursively evaluate this move
                next_color = 'Black' if current_color == 'Red' else 'Red'
                score = self._alpha_beta(board_copy, depth - 1, alpha, beta, False, next_color)
                best_score = max(best_score, score)
                
                # Alpha-beta pruning
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break  # Beta cutoff
            
            # Cache the result
            self.transposition_table[board_hash] = (depth, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in ordered_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Create a deep copy of the board for this move
                board_copy = self._deep_copy_board(board)
                
                # Move the piece on the copied board
                piece_copy = board_copy.grid[from_y][from_x]
                if piece_copy:  # Make sure the piece exists
                    board_copy.grid[to_y][to_x] = piece_copy
                    board_copy.grid[from_y][from_x] = None
                    piece_copy.x = to_x
                    piece_copy.y = to_y
                else:
                    continue  # Skip this move if piece doesn't exist
                
                # Recursively evaluate this move
                next_color = 'Black' if current_color == 'Red' else 'Red'
                score = self._alpha_beta(board_copy, depth - 1, alpha, beta, True, next_color)
                best_score = min(best_score, score)
                
                # Alpha-beta pruning
                beta = min(beta, best_score)
                if alpha >= beta:
                    break  # Alpha cutoff
            
            # Cache the result
            self.transposition_table[board_hash] = (depth, best_score)
            return best_score
    
    def evaluate_board(self, board):
        """
        Advanced evaluation of the board position from AI's perspective.
        Higher values are better for the AI.
        
        Args:
            board: The game board to evaluate
            
        Returns:
            float: A score representing how favorable the position is
        """
        opponent_color = 'Black' if self.color == 'Red' else 'Red'
        material_score = 0
        positional_score = 0
        mobility_score = 0
        
        # Material evaluation
        for y in range(10):
            for x in range(9):
                piece = board.grid[y][x]
                if piece:
                    # Base material value of the piece
                    piece_value = PIECE_VALUES.get(piece.type, 0)
                    multiplier = 1 if piece.color == self.color else -1
                    material_score += multiplier * piece_value
                    
                    # Positional value based on piece type and location
                    if piece.type in self.position_tables:
                        # Adjust for perspective (board is flipped for black)
                        if piece.color == 'Black' and piece.color == self.color:
                            pos_y = 9 - y  # Flip for Black's perspective when Black is AI
                        elif piece.color == 'Red' and piece.color != self.color:
                            pos_y = 9 - y  # Flip for Red's perspective when Black is AI
                        else:
                            pos_y = y
                            
                        position_value = self.position_tables[piece.type][pos_y][x]
                        positional_score += multiplier * position_value * 0.1  # Scale down positional value
                    
                    # Calculate mobility for this piece
                    from Jeux.moves import get_valid_moves
                    valid_moves = get_valid_moves(piece, board)
                    mobility = len(valid_moves)
                    
                    # Mobility is good for our pieces, bad for opponent's
                    mobility_score += multiplier * mobility * 0.05  # Scale down mobility value
        
        # Check for checkmate or stalemate conditions
        ai_in_check = self._is_in_check(board, self.color)
        opponent_in_check = self._is_in_check(board, opponent_color)
        
        check_score = 0
        if ai_in_check:
            check_score -= 50  # Being in check is bad
        if opponent_in_check:
            check_score += 50  # Putting opponent in check is good
        
        # Final score combining all factors
        total_score = material_score + positional_score + mobility_score + check_score
        
        return total_score
    
    def _is_in_check(self, board, color):
        """
        Check if the given color's general is in check.
        
        Args:
            board: Current board state
            color: Color to check ('Red' or 'Black')
            
        Returns:
            bool: True if the general is in check
        """
        # Find the general's position
        general_pos = None
        for y in range(10):
            for x in range(9):
                piece = board.grid[y][x]
                if piece and piece.type == 'General' and piece.color == color:
                    general_pos = (x, y)
                    break
            if general_pos:
                break
        
        if not general_pos:
            return False  # No general found (shouldn't happen in a valid game)
        
        # Check if any opponent piece can capture the general
        opponent_color = 'Black' if color == 'Red' else 'Red'
        for y in range(10):
            for x in range(9):
                piece = board.grid[y][x]
                if piece and piece.color == opponent_color:
                    from Jeux.moves import get_valid_moves
                    valid_moves = get_valid_moves(piece, board)
                    if general_pos in valid_moves:
                        return True  # General is in check
        
        return False
    
    def _is_game_over(self, board):
        """
        Check if the game is over (general has been captured).
        
        Args:
            board: Current board state
            
        Returns:
            bool: True if game is over, False otherwise
        """
        # Check if either general exists
        red_general_exists = False
        black_general_exists = False
        
        for y in range(10):
            for x in range(9):
                piece = board.grid[y][x]
                if piece:
                    if piece.type == 'General' and piece.color == 'Red':
                        red_general_exists = True
                    elif piece.type == 'General' and piece.color == 'Black':
                        black_general_exists = True
        
        return not (red_general_exists and black_general_exists)
    
    def _hash_board(self, board):
        """
        Create a simple hash of the current board state for the transposition table.
        
        Args:
            board: Current board state
            
        Returns:
            str: A hash string representing the board state
        """
        hash_parts = []
        
        for y in range(10):
            row = []
            for x in range(9):
                piece = board.grid[y][x]
                if piece:
                    row.append(f"{piece.color[0]}{piece.type[:2]}")
                else:
                    row.append("--")
            hash_parts.append("".join(row))
        
        return "|".join(hash_parts)