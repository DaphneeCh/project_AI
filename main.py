"""
main.py - Entry point for the Vietnamese Chess (Cờ Tướng) game
This module initializes the game and handles the main game loop, user input,
and game flow control.
"""

from game import Game
from moves import get_valid_moves

# Dictionary of piece symbols and their explanations
PIECE_SYMBOLS = {
    "CH": "Chariot (Xe): Moves horizontally or vertically any number of spaces.",
    "CA": "Cannon (Pháo): Moves like a Chariot but captures by jumping over one piece.",
    "HO": "Horse (Ngựa): Moves in an 'L' shape, two spaces in one direction and one space perpendicular.",
    "EL": "Elephant (Tượng): Moves diagonally two spaces, cannot cross the river.",
    "AD": "Advisor (Sĩ): Moves one space diagonally, restricted to the palace.",
    "GE": "General (Tướng): Moves one space in any direction, restricted to the palace.",
    "SO": "Soldier (Binh): Moves one space forward, can move sideways after crossing the river.",
}

def display_instructions():
    """Display game instructions"""
    print("\n=== VIETNAMESE CHESS (CỜ TƯỚNG) INSTRUCTIONS ===")
    print("1. Enter the coordinates of a piece in 'x,y' format to select it")
    print("2. Valid moves for that piece will be displayed")
    print("3. Enter destination coordinates in 'x,y' format to move the piece")
    print("4. Special commands:")
    print("   - 'explain x,y' : displays information about the piece and its meaning at position x,y")
    print("   - 'back' : cancels selection and allows you to choose another piece")
    print("   - 'quit' or 'exit' : quits the game")
    print("   - 'help' : displays these instructions again")
    print("=== ENJOY THE GAME! ===\n")

def play_game():
    """
    Main game function that handles the game loop and user interaction.
    Allows players to select pieces, view valid moves, and make moves until the game ends.
    """
    game = Game()
    display_instructions()
    
    while not game.game_over:
        game.display_game()
        
        try:
            from_input = input(f"{game.current_player}'s turn.\nEnter piece position (x,y), 'explain x,y', or 'help': ")
            if from_input.lower() == 'quit' or from_input.lower() == 'exit':
                print("Game terminated.")
                break
            
            # Display instructions
            if from_input.lower() == 'help':
                display_instructions()
                continue
            
            # Check for explain command
            if from_input.lower().startswith('explain '):
                coords = from_input.lower().replace('explain ', '')
                try:
                    exp_x, exp_y = map(int, coords.split(','))
                    
                    if not game.board.is_in_bounds(exp_x, exp_y):
                        print("Position out of bounds. Try again.")
                        continue
                        
                    piece = game.board.grid[exp_y][exp_x]
                    if not piece:
                        print("No piece at the selected position.")
                        continue
                    
                    # Display piece information
                    print(f"\n--- {piece} Information ---")
                    print(f"Type: {piece.type}")
                    print(f"Player's Color: {piece.color}")
                    print(f"Position: ({piece.x}, {piece.y})")
                    
                    # Add piece description from PIECE_SYMBOLS
                    piece_type_abbr = piece.type[:2].upper()
                    if piece_type_abbr in PIECE_SYMBOLS:
                        print(f"Description: {PIECE_SYMBOLS[piece_type_abbr]}")
                    
                    # Additional info if available
                    if hasattr(piece, 'get_description'):
                        print(f"Additional Information: {piece.get_description()}")
                    
                    continue
                except ValueError:
                    print("Invalid format for explain command. Use 'explain x,y'")
                    continue
                
            from_x, from_y = map(int, from_input.split(','))
            
            # Check if the position is valid and has a piece
            if not game.board.is_in_bounds(from_x, from_y):
                print("Position out of bounds. Try again.")
                continue
                
            piece = game.board.grid[from_y][from_x]
            if not piece:
                print("No piece at the selected position. Try again.")
                continue
                
            # Show valid moves for the selected piece
            if piece.color == game.current_player:
                valid_moves = get_valid_moves(piece, game.board)
                if not valid_moves:
                    print(f"No valid moves for {piece}. Please select another piece.")
                    continue
                print(f"Valid moves for {piece}: {valid_moves}")
            else:
                print("Invalid selection")
                continue
                
            to_input = input("Enter destination position (x,y): ")
            if to_input.lower() == 'quit' or to_input.lower() == 'exit':
                print("Game terminated.")
                break
                
            if to_input.lower() == 'back':
                continue  # Allow player to select a different piece
                
            to_x, to_y = map(int, to_input.split(','))
            
            success, message = game.make_move((from_x, from_y), (to_x, to_y))
            print(message)
            
        except ValueError:
            print("Invalid input format. Use 'x,y' format.")
        except IndexError:
            print("Position out of bounds.")
        except KeyboardInterrupt:
            print("\nGame terminated.")
            break
    
    # Final game state
    if game.game_over:
        game.display_game()

if __name__ == "__main__":
    play_game()