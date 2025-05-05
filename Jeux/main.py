"""
main.py - Entry point for the Vietnamese Chess (Cờ Tướng) game
This module initializes the game and handles the main game loop, user input,
and game flow control.
"""

import time
import os
import sys
import csv
from datetime import datetime

# Fix import errors by adding the project root to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from Jeux.game import Game
from Jeux.moves import get_valid_moves

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
    "HO": "Horse (Mã): Move in an 'L' shape, two squares in one direction and one square perpendicular. If there is another piece standing at the intersection adjacent to the vertical or horizontal step, the Horse is blocked and cannot move.",
    "EL": "Elephant (Tượng): Moves diagonally two spaces, cannot cross the river. If there is another piece standing in the middle of that diagonal line, the Elephant is blocked and cannot move.",
    "AD": "Advisor (Sĩ): Moves one space diagonally, restricted to the palace.",
    "GE": "General (Tướng): Moves one space in any direction, restricted to the palace. Two Generals cannot face each other directly on the same line. If they do, there must be a piece from either side blocking their view.",
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
    print("3. AI vs. AI")
    print("4. AI Tournament (50 games per matchup)")
    print("5. Instructions")
    print("6. Exit")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Please enter a valid number.")

def display_ai_menu():
    """Display the AI difficulty selection menu"""
    clear_screen()
    display_title()
    print("\nSELECT AI DIFFICULTY:")
    print("0. Level 0 - Random AI (Makes completely random moves)")
    
    if AI_AVAILABLE:
        print("1. Level 1 - Beginner AI (Basic strategy, prioritizes captures)")
        print("2. Level 2 - Intermediate AI (Looks ahead a few moves)")
        print("3. Level 3 - Advanced AI (Optimal play)")
    else:
        print("(Additional AI levels not available)")
    
    print("4. Back to Main Menu")
    
    max_option = 5 if AI_AVAILABLE else 2
    
    while True:
        try:
            choice = int(input(f"\nEnter your choice (0-{max_option-1}): "))
            if 0 <= choice < max_option:
                return choice
            else:
                print(f"Please enter a number between 0 and {max_option-1}.")
        except ValueError:
            print("Please enter a valid number.")

def display_color_menu():
    """Display the player color selection menu"""
    clear_screen()
    display_title()
    print("\nSELECT YOUR COLOR:")
    print("1. White (moves first)")
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

def select_ai(player_name):
    """
    Select AI difficulty for AI vs AI mode
    
    Args:
        player_name: String to display (e.g., "First AI" or "Second AI")
        
    Returns:
        tuple: (ai_level, ai_name)
    """
    clear_screen()
    display_title()
    print(f"\nSELECT {player_name} DIFFICULTY:")
    print("0. Level 0 - Random AI (Makes completely random moves)")
    
    if AI_AVAILABLE:
        print("1. Level 1 - Beginner AI (Basic strategy, prioritizes captures)")
        print("2. Level 2 - Intermediate AI (Looks ahead a few moves)")
        print("3. Level 3 - Advanced AI (Optimal play)")
    else:
        print("(Additional AI levels not available)")
    
    print("4. Back to Main Menu")
    
    max_option = 5 if AI_AVAILABLE else 2
    
    while True:
        try:
            choice = int(input(f"\nEnter your choice (0-{max_option-1}): "))
            if 0 <= choice < max_option:
                if choice == 4:
                    return None, None
                
                ai_level = choice  # Convert to 0-based level
                
                # Get AI name based on level
                if ai_level == 0:
                    ai_name = "Random AI (Level 0)"
                elif ai_level == 1:
                    ai_name = "Beginner AI (Level 1)"
                elif ai_level == 2:
                    ai_name = "Intermediate AI (Level 2)"
                elif ai_level == 3:
                    ai_name = "Advanced AI (Level 3)"
                
                return ai_level, ai_name
            else:
                print(f"Please enter a number between 0 and {max_option-1}.")
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

def play_human_vs_ai(ai_level, human_color='White'):
    """
    Play game between a human and an AI.
    
    Args:
        ai_level (int): The difficulty level of the AI (0-3)
        human_color (str): The color of the human player ('White' or 'Black')
    """
    game = Game()
    display_instructions()
    
    ai_color = 'Black' if human_color == 'White' else 'White'
    
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

def play_ai_vs_ai():
    """
    Let two AI players compete against each other
    """
    # Select first AI (White)
    white_ai_level, white_ai_name = select_ai("WHITE AI")
    if white_ai_level is None:
        return  # User went back to main menu
    
    # Select second AI (Black)
    black_ai_level, black_ai_name = select_ai("BLACK AI")
    if black_ai_level is None:
        return  # User went back to main menu
    
    # Create the game
    game = Game()
    
    # Create AI players
    if white_ai_level == 0:
        white_ai = RandomAI('White')
    elif white_ai_level == 1:
        white_ai = BeginnerAI('White')
    elif white_ai_level == 2:
        white_ai = IntermediateAI('White')
    elif white_ai_level == 3:
        white_ai = AdvancedAI('White')
    
    if black_ai_level == 0:
        black_ai = RandomAI('Black')
    elif black_ai_level == 1:
        black_ai = BeginnerAI('Black')
    elif black_ai_level == 2:
        black_ai = IntermediateAI('Black')
    elif black_ai_level == 3:
        black_ai = AdvancedAI('Black')
    
    # Settings for AI vs AI display
    print(f"\nMatch: {white_ai_name} (White) vs. {black_ai_name} (Black)")
    print("\nOptions:")
    print("1. Fast play (minimal display)")
    print("2. Normal play (display each move)")
    print("3. Slow play (pause between moves)")
    
    mode = 0
    while mode not in [1, 2, 3]:
        try:
            mode = int(input("\nSelect display mode (1-3): "))
        except ValueError:
            print("Please enter a valid number.")
    
    move_count = 0
    max_moves = 200  # Prevent infinite games
    
    # Game loop
    while not game.game_over and move_count < max_moves:
        # Display the board based on selected mode
        if mode >= 2:
            clear_screen()
            display_title()
            print(f"\nMove #{move_count+1}")
            print(f"{white_ai_name} (White) vs. {black_ai_name} (Black)")
            game.display_game()
        
        current_ai = white_ai if game.current_player == 'White' else black_ai
        current_name = white_ai_name if game.current_player == 'White' else black_ai_name
        
        if mode >= 2:
            print(f"\n{current_name} is thinking...")
        
        # Get AI's move
        ai_move = current_ai.get_move(game)
        
        if ai_move:
            from_pos, to_pos = ai_move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            # Get the piece being moved
            piece = game.board.grid[from_y][from_x]
            
            # Make the move
            success, message = game.make_move((from_x, from_y), (to_x, to_y))
            
            if mode >= 2:
                print(f"{current_name} moves {piece} from ({from_x},{from_y}) to ({to_x},{to_y})")
                print(message)
            
            move_count += 1
            
            # Add delay for normal mode
            if mode == 2:
                time.sleep(3)

            # Add extra delay for slow mode
            if mode == 3:
                # wait for user input
                input("Press Enter to continue...")
        else:
            print(f"{current_name} couldn't find a valid move!")
            game.game_over = True
            game.winner = 'Black' if game.current_player == 'White' else 'White'
    
    # Final game state
    clear_screen()
    display_title()
    print("\nGAME OVER")
    game.display_game()
    
    if move_count >= max_moves:
        print(f"\nGame ended after {max_moves} moves (draw)")
    else:
        print(f"\nWinner: {game.winner}")
        winning_ai = white_ai_name if game.winner == 'White' else black_ai_name
        print(f"{winning_ai} wins!")
    
    # Game statistics
    print(f"\nTotal moves: {move_count}")
    
    input("\nPress Enter to continue...")

def run_ai_tournament():
    """
    Run multiple games between different AI levels and save results to CSV
    """
    clear_screen()
    display_title()
    print("\nAI TOURNAMENT MODE")
    print("\nThis will run 50 games for each AI pair combination and save results to a CSV file.")
    
    # Confirm with user
    confirm = input("\nStart tournament? This may take a while. (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Available AI levels
    ai_levels = [0]  # Always include Random AI
    ai_names = ["Random AI (Level 0)"]
    
    if AI_AVAILABLE:
        ai_levels.extend([1, 2, 3])
        ai_names.extend(["Beginner AI (Level 1)", "Intermediate AI (Level 2)", "Advanced AI (Level 3)"])
    
    # Number of games to run for each pair
    num_games = 50
    
    # Prepare results file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_tournament_results_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header row
        csvwriter.writerow(['White AI', 'Black AI', 'Total Games', 'White Wins', 'Black Wins', 
                           'Draws', 'White Win %', 'Black Win %', 'Draw %', 'Avg Moves'])
        
        # Run games for each pair of AIs
        for white_idx, white_level in enumerate(ai_levels):
            for black_idx, black_level in enumerate(ai_levels):
                print(f"\nRunning {num_games} games: {ai_names[white_idx]} (White) vs {ai_names[black_idx]} (Black)")
                
                # Statistics
                white_wins = 0
                black_wins = 0
                draws = 0
                total_moves = 0
                
                # Progress bar
                for game_num in range(num_games):
                    print(f"Game {game_num+1}/{num_games}...", end='\r')
                    
                    # Create a new game
                    game = Game()
                    
                    # Create AI players
                    white_ai = create_ai('White', white_level)
                    black_ai = create_ai('Black', black_level)
                    
                    # Run the game
                    move_count, winner = run_ai_game(game, white_ai, black_ai)
                    
                    # Update statistics
                    if winner == 'White':
                        white_wins += 1
                    elif winner == 'Black':
                        black_wins += 1
                    else:
                        draws += 1
                    
                    total_moves += move_count
                
                # Calculate final statistics
                avg_moves = total_moves / num_games
                White_win_pct = (white_wins / num_games) * 100
                black_win_pct = (black_wins / num_games) * 100
                draw_pct = (draws / num_games) * 100
                
                # Write results for this pair
                csvwriter.writerow([
                    ai_names[white_idx], 
                    ai_names[black_idx], 
                    num_games, 
                    white_wins, 
                    black_wins, 
                    draws,
                    f"{White_win_pct:.1f}%",
                    f"{black_win_pct:.1f}%", 
                    f"{draw_pct:.1f}%",
                    f"{avg_moves:.1f}"
                ])
                
                # Display results
                print(" " * 30, end='\r')  # Clear progress line
                print(f"Results: White wins: {white_wins}, Black wins: {black_wins}, Draws: {draws}")
                print(f"Average moves per game: {avg_moves:.1f}")
    
    print(f"\nTournament complete! Results saved to {filename}")
    input("\nPress Enter to return to the Main Menu...")

def create_ai(color, level):
    """
    Create an AI instance of the specified level
    
    Args:
        color (str): 'White' or 'Black'
        level (int): AI level (0-3)
        
    Returns:
        AI instance
    """
    if level == 0:
        return RandomAI(color)
    elif level == 1:
        return BeginnerAI(color)
    elif level == 2:
        return IntermediateAI(color)
    elif level == 3:
        return AdvancedAI(color)
    else:
        return RandomAI(color)  # Default to Random AI

def run_ai_game(game, white_ai, black_ai, max_moves=400):
    """
    Run a single game between two AIs
    
    Args:
        game: Game instance
        white_ai: AI instance for White player
        black_ai: AI instance for Black player
        max_moves: Maximum number of moves before declaring a draw
    
    Returns:
        tuple: (move_count, winner)
    """
    move_count = 0
    
    while not game.game_over and move_count < max_moves:
        # Get current AI
        current_ai = white_ai if game.current_player == 'White' else black_ai
        
        # Get and make move
        ai_move = current_ai.get_move(game)
        
        if ai_move:
            from_pos, to_pos = ai_move
            success, message = game.make_move(from_pos, to_pos)  # Capture return values
            if success:  # Only increment move count if move was successful
                move_count += 1
            else:
                # If move failed, there's an issue with the AI's move generation
                print(f"AI attempted invalid move: {message}")
                game.game_over = True
                game.winner = 'Black' if game.current_player == 'White' else 'White'
        else:
            # AI has no valid moves
            game.game_over = True
            game.winner = 'Black' if game.current_player == 'White' else 'White'
    
    # Check for draw due to move limit
    if move_count >= max_moves and not game.game_over:
        return move_count, 'Draw'
    
    return move_count, game.winner

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
            
            human_color = 'White' if color_choice == 1 else 'Black'
            ai_level = ai_choice - 1  # Convert menu choice to 0-based level
            
            play_human_vs_ai(ai_level, human_color)
            
        elif choice == 3:  # AI vs. AI
            play_ai_vs_ai()
            
        elif choice == 4:  # AI Tournament - NEW OPTION
            run_ai_tournament()
            
        elif choice == 5:  # Instructions
            clear_screen()
            display_title()
            display_instructions()
            input("\nPress Enter to return to the Main Menu...")
            
        elif choice == 6:  # Exit
            print("\nThanks for playing Vietnamese Chess (Cờ Tướng)!")
            break

if __name__ == "__main__":
    main()