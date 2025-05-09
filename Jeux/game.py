"""
game.py - Manages the game state for Vietnamese Chess (Cờ Tướng)
This module contains the Game class which handles turn management, move validation,
win conditions, and game state tracking.
"""

from Jeux.board import Board
from Jeux.moves import get_valid_moves

class Game:
    """
    Manages the overall game state and rules.
    
    Attributes:
        board (Board): The game board
        current_player (str): The current player ('White' or 'Black')
        game_over (bool): Whether the game has ended
        winner (str or None): The winner of the game, if any
        captured_pieces (dict): Pieces captured by each player
        board_states (dict): Record of board positions for detecting repetition
    """
    def __init__(self):
        self.board = Board()
        self.current_player = 'White'
        self.game_over = False
        self.winner = None
        self.captured_pieces = {'White': [], 'Black': []}
        self.board_states = {}  # Track board positions
        self.update_board_state()  # Track initial state

    def get_board_state_key(self):
        """
        Creates a hashable representation of the current board state.
        Returns a string that represents the board position and whose turn it is.
        """
        # Create a representation of the current board state
        board_str = self.board.to_string()
        
        # Include current player in the state
        state = board_str + "-" + self.current_player
        return state
        
    def update_board_state(self):
        """
        Update the board state history.
        Converts the current board position to a string representation and counts occurrences.
        """
        state = self.get_board_state_key()
        if state in self.board_states:
            self.board_states[state] += 1
        else:
            self.board_states[state] = 1
            
        # Check for threefold repetition
        if self.board_states[state] > 3:
            self.game_over = True
            self.winner = "Draw (Threefold Repetition)"

    def switch_player(self):
        """
        Switches the current player from White to Black or vice versa.
        """
        self.current_player = 'Black' if self.current_player == 'White' else 'White'

    def make_move(self, from_pos: tuple[int,int], to_pos: tuple[int,int]) -> tuple[bool, str]:
        """
        Attempts to move a piece from one position to another.
        
        Args:
            from_pos (tuple): The starting position (x, y)
            to_pos (tuple): The destination position (x, y)
            
        Returns:
            tuple: (success, message) where success is a boolean and
                  message is a string explaining the result
        """
        if self.game_over:
            return False, "Game is already over"

        from_x, from_y = from_pos
        to_x, to_y = to_pos

        if not self.board.is_in_bounds(from_x, from_y) or not self.board.is_in_bounds(to_x, to_y):
            return False, "Position out of bounds"

        piece = self.board.grid[self.board.to_1d(from_x, from_y)]
        if piece == '  ':
            return False, "No piece at the selected position"

        if piece[0] != self.current_player[0]:
            return False, "Not your piece"

        valid_moves = get_valid_moves(from_x,from_y, self.board)
        if (to_x, to_y) not in valid_moves:
            return False, "Invalid move"

        # Make the move
        captured = self.board.move_piece(from_x, from_y, to_x, to_y)
        if captured != '  ':
            self.captured_pieces[self.current_player].append(captured)
            if captured[1] == 'G':
                self.game_over = True
                self.winner = self.current_player

        # Switch to the next player
        self.switch_player()
        
        # Update board state history and check for threefold repetition
        self.update_board_state()
        
        return True, "Move successful"

    def display_game(self):
        print(f"\nCurrent player: {self.current_player}")
        self.board.display()
        print(f"Captured by White: {', '.join(str(p) for p in self.captured_pieces['White'])}")
        print(f"Captured by Black: {', '.join(str(p) for p in self.captured_pieces['Black'])}")
        if self.game_over:
            if self.winner and isinstance(self.winner, str) and self.winner.startswith("Draw"):
                print(f"Game over! {self.winner}")
            else:
                print(f"Game over! Winner: {self.winner}")