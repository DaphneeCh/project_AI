"""
main.py - Entry point for the Vietnamese Chess (Cờ Tướng) game
This module initializes the game and handles the main game loop, user input,
and game flow control.
"""

import time
import os
from Jeux.game import Game
from Jeux.moves import get_valid_moves

# Import AI modules (assuming they're implemented)
try:
    from AI.AI_lv0 import AI as RandomAI
    from AI.AI_lv1 import AI as BeginnerAI
    from AI.AI_lv2 import AI as IntermediateAI
    from AI.AI_optimal import AI as AdvancedAI
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: AI modules not found or incomplete. AI options will be limited.")

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

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title():
    """Display the game title"""
    print("\n" + "=" * 60)
    print("               VIETNAMESE CHESS (CỜ TƯỚNG)")
    print("=" * 60)

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

def display_main_menu():
    """Display the main menu options"""
    clear_screen()
    display_title()
    print("\nMAIN MENU:")
    print("1. Human vs. Human")
    print("2. Human vs. AI")
    print("3. Instructions")
    print("4. Exit")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")

def display_ai_menu():
    """Display the AI difficulty selection menu"""
    clear_screen()
    display_title()
    print("\nSELECT AI DIFFICULTY:")
    print("1. Level 0 - Random AI (Makes completely random moves)")
    
    if AI_AVAILABLE:
        print("2. Level 1 - Beginner AI (Basic strategy, prioritizes captures)")
        print("3. Level 2 - Intermediate AI (Looks ahead a few moves)")
        print("4. Level 3 - Advanced AI (Optimal play)")
    else:
        print("(Additional AI levels not available)")
    
    print("5. Back to Main Menu")
    
    max_option = 5 if AI_AVAILABLE else 2
    
    while True:
        try:
            choice = int(input(f"\nEnter your choice (1-{max_option}): "))
            if 1 <= choice <= max_option:
                return choice
            else:
                print(f"Please enter a number between 1 and {max_option}.")
        except ValueError:
            print("Please enter a valid number.")

def display_color_menu():
    """Display the player color selection menu"""
    clear_screen()
    display_title()
    print("\nSELECT YOUR COLOR:")
    print("1. Red (moves first)")
    print("2. Black")
    print("3. Back to AI Menu")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")

def play_human_vs_human():
    """
    Play game between two human players.
    This is the original play_game function.
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
                # Existing explain code...
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
                
            # Rest of the human player turn logic...
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
        print(f"Game over! Winner: {game.winner}")
    
    input("\nPress Enter to continue...")

def play_human_vs_ai(ai_level, human_color='Red'):
    """
    Play game between a human and an AI.
    
    Args:
        ai_level (int): The difficulty level of the AI (0-3)
        human_color (str): The color of the human player ('Red' or 'Black')
    """
    game = Game()
    display_instructions()
    
    ai_color = 'Black' if human_color == 'Red' else 'Red'
    
    # Create the appropriate AI based on the selected level
    if ai_level == 0:
        ai = RandomAI(ai_color)
        ai_name = "Random AI (Level 0)"
    elif ai_level == 1 and AI_AVAILABLE:
        ai = BeginnerAI(ai_color)
        ai_name = "Beginner AI (Level 1)"
    elif ai_level == 2 and AI_AVAILABLE:
        ai = IntermediateAI(ai_color)
        ai_name = "Intermediate AI (Level 2)"
    elif ai_level == 3 and AI_AVAILABLE:
        ai = AdvancedAI(ai_color)
        ai_name = "Advanced AI (Level 3)"
    else:
        # Fallback to Random AI
        ai = RandomAI(ai_color)
        ai_name = "Random AI (Level 0)"
    
    print(f"\nYou are playing as {human_color} against {ai_name} ({ai_color}).")
    time.sleep(2)
    
    while not game.game_over:
        game.display_game()
        
        # Human player's turn
        if game.current_player == human_color:
            print(f"Your turn ({human_color}).")
            
            try:
                from_input = input("Enter piece position (x,y), 'explain x,y', or 'help': ")
                if from_input.lower() == 'quit' or from_input.lower() == 'exit':
                    print("Game terminated.")
                    break
                
                # Display instructions
                if from_input.lower() == 'help':
                    display_instructions()
                    continue
                
                # Check for explain command
                if from_input.lower().startswith('explain '):
                    # Same explain code as in human vs human...
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
                
                # Rest of human player logic...
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
                
        # AI player's turn
        else:
            print(f"\n{ai_name} is thinking...")
            time.sleep(1)  # Add a small delay to make it seem like the AI is "thinking"
            
            ai_move = ai.get_move(game)
            
            if ai_move:
                from_pos, to_pos = ai_move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Show what piece the AI is moving
                piece = game.board.grid[from_y][from_x]
                print(f"AI moves {piece} from ({from_x},{from_y}) to ({to_x},{to_y})")
                
                success, message = game.make_move((from_x, from_y), (to_x, to_y))
                print(message)
                
                time.sleep(1)  # Give player time to see the AI's move
            else:
                print("AI couldn't find a valid move!")
                game.game_over = True
                game.winner = human_color
    
    # Final game state
    if game.game_over:
        game.display_game()
        print(f"Game over! Winner: {game.winner}")
    
    input("\nPress Enter to continue...")

def main():
    """Main function that handles the game menu and selection logic"""
    while True:
        choice = display_main_menu()
        
        if choice == 1:  # Human vs. Human
            play_human_vs_human()
            
        elif choice == 2:  # Human vs. AI
            ai_choice = display_ai_menu()
            
            if ai_choice == 5:  # Back to main menu
                continue
            
            color_choice = display_color_menu()
            
            if color_choice == 3:  # Back to AI menu
                continue
            
            human_color = 'Red' if color_choice == 1 else 'Black'
            ai_level = ai_choice - 1  # Convert menu choice to 0-based level
            
            play_human_vs_ai(ai_level, human_color)
            
        elif choice == 3:  # Instructions
            clear_screen()
            display_title()
            display_instructions()
            input("\nPress Enter to return to the Main Menu...")
            
        elif choice == 4:  # Exit
            print("\nThanks for playing Vietnamese Chess (Cờ Tướng)!")
            break

if __name__ == "__main__":
    main()