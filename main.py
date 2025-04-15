"""
main.py - Entry point for the Vietnamese Chess (Cờ Tướng) game
This module initializes the game and handles the main game loop, user input,
and game flow control.
"""

from game import Game
from moves import get_valid_moves

def play_game():
    """
    Main game function that handles the game loop and user interaction.
    Allows players to select pieces, view valid moves, and make moves until the game ends.
    """
    game = Game()
    
    while not game.game_over:
        game.display_game()
        
        try:
            from_input = input(f"{game.current_player}'s turn. Enter piece position (x,y): ")
            if from_input.lower() == 'quit' or from_input.lower() == 'exit':
                print("Game terminated.")
                break
                
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