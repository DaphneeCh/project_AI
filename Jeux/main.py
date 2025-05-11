"""
main.py - Point d'entrée pour le jeu d'Échecs Vietnamien (Cờ Tướng)
Ce module initialise le jeu et gère la boucle principale du jeu, les entrées utilisateur,
et le contrôle du déroulement du jeu.
"""

import time
import os
import sys
import csv
from datetime import datetime

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from Jeux.game import Game
from Jeux.moves import get_valid_moves

from Jeux.pieces import *

try:
    from AI.AI_lv0 import AI as RandomAI
    from AI.AI_lv1 import AI as BeginnerAI
    from AI.AI_lv2 import AI as IntermediateAI
    from AI.AI_optimal import AI as AdvancedAI
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: AI modules not found or incomplete. AI options will be limited.")

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title():
    """Affichage du titre du jeu"""
    print("\n" + "=" * 60)
    print("               VIETNAMESE CHESS (CỜ TƯỚNG)")
    print("=" * 60)

def display_instructions():
    """Affichage des instructions du jeu"""
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
    """Affichage du menu principal"""
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
    """Affichage du menu de sélection de l'IA"""
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
    
    max_option = 5 if AI_AVAILABLE else 2

    print(f"{max_option-1}. Back to Main Menu")
    
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
    """Affichage du menu de sélection de la couleur"""
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
    Selectionner AI pour le mode IA contre IA

    Args:
        player_name: String à afficher (e.g., "First AI" or "Second AI")
        
    Returns:
        tuple: (ai_level, ai_name)
    """
    clear_screen()
    display_title()
    print(f"\nSELECT {player_name} DIFFICULTY:")
    print("0. Level 0 - Random AI")
    
    if AI_AVAILABLE:
        print("1. Level 1 - Beginner AI")
        print("2. Level 2 - Intermediate AI")
        print("3. Level 3 - Advanced AI")
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
                
                ai_level = choice # Convertir le choix en niveau d'IA
                
                # Déterminer le nom de l'IA en fonction du niveau
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
    Partie entre deux joueurs humains.
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
            
            # Afficher les instructions
            if from_input.lower() == 'help':
                display_instructions()
                continue
            
            # Vérifier la commande d'explication
            if from_input.lower().startswith('explain '):
                # Extraire les coordonnées
                coords = from_input.lower().replace('explain ', '')
                try:
                    exp_x, exp_y = map(int, coords.split(','))
                    
                    if not game.board.is_in_bounds(exp_x, exp_y):
                        print("Position out of bounds. Try again.")
                        continue
                        
                    piece = game.board.grid[game.board.to_1d(exp_x, exp_y)]  # Fixed access
                    if not piece:
                        print("No piece at the selected position.")
                        continue
                    
                    # Afficher les informations sur la pièce
                    print(f"\n--- {piece} Information ---")
                    print(f"Type: {PIECE_TYPES_REVERSE[piece[1]]}")
                    print(f"Player's Color: {'White' if piece[0] == 'W' else 'Black'}")
                    print(f"Position: ({exp_x}, {exp_y})")
                    
                    # Ajouter la description de la pièce à partir de PIECE_SYMBOLS
                    if piece[1] in PIECE_SYMBOLS:
                        print(f"Description: {PIECE_SYMBOLS[piece[1]]}")

                    continue
                except ValueError:
                    print("Invalid format for explain command. Use 'explain x,y'")
                    continue
                
            # La logique pour le tour du joueur humain...
            from_x, from_y = map(int, from_input.split(','))
            
            # Vérifier si la position est valide et a une pièce
            if not game.board.is_in_bounds(from_x, from_y):
                print("Position out of bounds. Try again.")
                continue
                
            piece = game.board.grid[game.board.to_1d(from_x, from_y)]
            if piece == '  ':
                print("No piece at the selected position. Try again.")
                continue
                
            # Afficher les mouvements valides pour la pièce sélectionnée
            if (piece[0] == 'W' and game.current_player == 'White') or (piece[0] == 'B' and game.current_player == 'Black'):
                valid_moves = get_valid_moves(from_x,from_y, game.board)
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
                continue  # Permettre au joueur de sélectionner une autre pièce
                
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
    
    # État final du jeu
    if game.game_over:
        game.display_game()
        print(f"Game over! Winner: {game.winner}")
    
    input("\nPress Enter to continue...")

def play_human_vs_ai(ai_level, human_color='White'):
    """
    Joue une partie entre un humain et une IA.
    
    Args:
        ai_level (int): Le niveau de difficulté de l'IA (0-3)
        human_color (str): La couleur du joueur humain ('White' ou 'Black')
    """
    game = Game()
    display_instructions()
    
    ai_color = 'Black' if human_color == 'White' else 'White'
    
    # Créer l'IA en fonction du niveau sélectionné
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
        # Si l'IA n'est pas disponible, utiliser RandomAI par défaut
        ai = RandomAI(ai_color)
        ai_name = "Random AI (Level 0)"
    
    print(f"\nYou are playing as {human_color} against {ai_name} ({ai_color}).")
    time.sleep(2)
    
    while not game.game_over:
        game.display_game()
        
        # Le tour du joueur humain
        if game.current_player == human_color:
            print(f"Your turn ({human_color}).")
            
            try:
                from_input = input("Enter piece position (x,y), 'explain x,y', or 'help': ")
                if from_input.lower() == 'quit' or from_input.lower() == 'exit':
                    print("Game terminated.")
                    break
                
                # Afficher les instructions
                if from_input.lower() == 'help':
                    display_instructions()
                    continue
                
                # Vérifier la commande d'explication
                if from_input.lower().startswith('explain '):
                    coords = from_input.lower().replace('explain ', '')
                    try:
                        exp_x, exp_y = map(int, coords.split(','))
                        
                        if not game.board.is_in_bounds(exp_x, exp_y):
                            print("Position out of bounds. Try again.")
                            continue
                            
                        piece = game.board.grid[game.board.to_1d(exp_x, exp_y)] 
                        if not piece:
                            print("No piece at the selected position.")
                            continue
                        
                        # Afficher les informations sur la pièce
                        print(f"\n--- {piece} Information ---")
                        print(f"Type: {PIECE_TYPES_REVERSE[piece[1]]}")
                        print(f"Player's Color: {'White' if piece[0] == 'W' else 'Black'}")
                        print(f"Position: ({exp_x}, {exp_y})")
                        
                        # Ajouter la description de la pièce à partir de PIECE_SYMBOLS
                        if piece[1] in PIECE_SYMBOLS:
                            print(f"Description: {PIECE_SYMBOLS[piece[1]]}")
                        
                        continue
                    except ValueError:
                        print("Invalid format for explain command. Use 'explain x,y'")
                        continue
                # La logique pour le tour du joueur humain...
                from_x, from_y = map(int, from_input.split(','))
                
                # Vérifier si la position est valide et a une pièce
                if not game.board.is_in_bounds(from_x, from_y):
                    print("Position out of bounds. Try again.")
                    continue
                    
                piece = game.board.grid[game.board.to_1d(from_x, from_y)]
                if not piece:
                    print("No piece at the selected position. Try again.")
                    continue
                    
                # Afficher les mouvements valides pour la pièce sélectionnée
                if (piece[0] == 'W' and game.current_player == 'White') or (piece[0] == 'B' and game.current_player == 'Black'):
                    valid_moves = get_valid_moves(from_x,from_y, game.board)
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
                    continue # Permettre au joueur de sélectionner une autre pièce

                # Extraire les coordonnées de destination
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
                
        # Le tour de l'IA
        else:
            print(f"\n{ai_name} is thinking...")
            time.sleep(1)
            
            ai_move = ai.get_move(game.board)
            
            if ai_move:
                from_pos, to_pos = ai_move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Afficher le mouvement de l'IA
                piece = game.board.grid[game.board.to_1d(from_x, from_y)] 
                print(f"AI moves {piece} from ({from_x},{from_y}) to ({to_x},{to_y})")
                
                success, message = game.make_move((from_x, from_y), (to_x, to_y))
                print(message)
                
                time.sleep(1) 
            else:
                print("AI couldn't find a valid move!")
                game.game_over = True
                print("Draw !")
    
    # État final du jeu
    if game.game_over:
        game.display_game()
        print(f"Game over! Winner: {game.winner}")
    
    input("\nPress Enter to continue...")

def play_ai_vs_ai():
    """
    Partie entre deux IA.
    """
    # Sélection de l'IA pour le joueur blanc
    white_ai_level, white_ai_name = select_ai("WHITE AI")
    if white_ai_level is None:
        return  # User went back to main menu
    
    # Selection de l'IA pour le joueur noir
    black_ai_level, black_ai_name = select_ai("BLACK AI")
    if black_ai_level is None:
        return  # L'utilisateur est revenu au menu principal
    
    # Créer une nouvelle partie
    game = Game()
    
    # Créer les IA en fonction des niveaux sélectionnés
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
    
    # Affichage des informations sur la partie
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
    max_moves = 100  #Par défaut, 100 coups maximum
    
    # Jeu en cours
    while not game.game_over and move_count < max_moves:
        # Affichage de l'état du jeu
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
        
        # Obtenir le mouvement de l'IA
        ai_move = current_ai.get_move(game.board)
        
        if ai_move:
            from_pos, to_pos = ai_move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            # Afficher le mouvement de l'IA
            piece = game.board.grid[game.board.to_1d(from_x, from_y)] 
            
            # Effectuer le mouvement
            success, message = game.make_move((from_x, from_y), (to_x, to_y))
            
            if mode >= 2:
                print(f"{current_name} moves {piece} from ({from_x},{from_y}) to ({to_x},{to_y})")
                print(message)
            
            move_count += 1
            
            # Ajouter un délai pour le mode normal
            if mode == 2:
                time.sleep(3)

            # Ajouter un délai pour le mode lent
            if mode == 3:
                # Pause entre les mouvements
                input("Press Enter to continue...")
        else:
            print(f"{current_name} couldn't find a valid move!")
            game.game_over = True
            print("Draw !")
    
    # Fin de la partie
    clear_screen()
    display_title()
    print("\nGAME OVER")
    game.display_game()
    
    if move_count >= max_moves:
        print(f"\nGame ended after {max_moves} moves (draw)")
    else:
        if (isinstance(game.winner, str) and game.winner.startswith("Draw")) or game.winner is None:
            print(f"\n{game.winner}")
        else:
            print(f"\nWinner: {game.winner}")
            winning_ai = white_ai_name if game.winner == 'White' else black_ai_name
            print(f"{winning_ai} wins!")
    
    # Afficher le nombre total de mouvements
    print(f"\nTotal moves: {move_count}")
    
    input("\nPress Enter to continue...")

def run_ai_tournament():
    """
    Exécute plusieurs parties entre différentes IA et enregistre les résultats dans un fichier CSV
    """
    clear_screen()
    display_title()
    print("\nAI TOURNAMENT MODE")
    
    # Tournament mode selection
    print("\nSelect tournament mode:")
    print("1. Full tournament (all AI combinations)")
    print("2. Single matchup (specific AI vs AI)")
    print("3. Back to main menu")
    
    mode_choice = 0
    while mode_choice not in [1, 2, 3]:
        try:
            mode_choice = int(input("\nEnter your choice (1-3): "))
        except ValueError:
            print("Please enter a valid number.")
    
    if mode_choice == 3:
        return
    
    # Le nombre de parties à effectuer
    try:
        num_games = int(input("\nEnter number of games to run (50-100): "))
        num_games = max(50, min(50, num_games))  
    except ValueError:
        num_games = 50
        print("Invalid input. Using default of 50 games.")
    
    print(f"\nRunning {num_games} games per matchup.")
    
    # Tous les niveaux d'IA disponibles
    ai_levels = [0] # Débuter avec l'IA de niveau 0
    ai_names = ["Random AI (Level 0)"]
    
    if AI_AVAILABLE:
        ai_levels.extend([1, 2, 3])
        ai_names.extend(["Beginner AI (Level 1)", "Intermediate AI (Level 2)", "Advanced AI (Level 3)"])
    
    # Créer un fichier CSV pour enregistrer les résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_tournament_results_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Ecrire l'en-tête du fichier CSV
        csvwriter.writerow(['White AI', 'Black AI', 'Total Games', 'White Wins', 'Black Wins', 
                           'Draws', 'White Win %', 'Black Win %', 'Draw %', 'Avg Moves'])
        
        if mode_choice == 1:  # Le tournoi complet
            print("\nRunning full tournament with all AI combinations...")
            
            # Exécuter tous les matchs entre les IA
            for white_idx, white_level in enumerate(ai_levels):
                for black_idx, black_level in enumerate(ai_levels):
                    run_matchup(white_level, black_level, ai_names[white_idx], ai_names[black_idx], 
                               num_games, csvwriter)
        
        else:  # Match spécifique entre deux IA
            # Sélectionner la première IA (Blanc)
            white_ai_level, white_ai_name = select_ai("WHITE AI")
            if white_ai_level is None:
                return  # L'utilisateur est revenu au menu principal
            
            # Sélectionner la deuxième IA (Noir)
            black_ai_level, black_ai_name = select_ai("BLACK AI")
            if black_ai_level is None:
                return  # L'utilisateur est revenu au menu principal
                
            # Exécuter le match entre les deux IA sélectionnées
            run_matchup(white_ai_level, black_ai_level, white_ai_name, black_ai_name, 
                       num_games, csvwriter)
    
    print(f"\nTournament complete! Results saved to {filename}")
    input("\nPress Enter to return to the Main Menu...")

def run_matchup(white_level, black_level, white_name, black_name, num_games, csvwriter):
    """
    Exécute un match entre deux IA spécifiques et enregistre les résultats
    
    Args:
        white_level (int): Niveau d'IA pour les Blancs
        black_level (int): Niveau d'IA pour les Noirs
        white_name (str): Nom de l'IA des Blancs
        black_name (str): Nom de l'IA des Noirs
        num_games (int): Nombre de parties à jouer
        csvwriter: Objet CSV writer pour l'enregistrement des résultats
    """
    print(f"\nRunning {num_games} games: {white_name} (White) vs {black_name} (Black)")
    
    # Initialiser les statistiques
    white_wins = 0
    black_wins = 0
    draws = 0
    total_moves = 0
    
    # La barre de progression
    for game_num in range(num_games):
        print(f"Game {game_num+1}/{num_games}...", end='\r')
        
        # Créer une nouvelle partie
        game = Game()
        
        # Créer les IA pour cette partie
        white_ai = create_ai('White', white_level)
        black_ai = create_ai('Black', black_level)
        
        # Exécuter la partie entre les IA
        move_count, winner = run_ai_game(game, white_ai, black_ai)
        
        # Mettre à jour les statistiques
        if winner == 'White':
            white_wins += 1
        elif winner == 'Black':
            black_wins += 1
        else:
            draws += 1
        
        total_moves += move_count
    
    # Calculer les resultats
    avg_moves = total_moves / num_games
    white_win_pct = (white_wins / num_games) * 100
    black_win_pct = (black_wins / num_games) * 100
    draw_pct = (draws / num_games) * 100
    
    # Enregistrer les résultats dans le fichier CSV
    csvwriter.writerow([
        white_name, 
        black_name, 
        num_games, 
        white_wins, 
        black_wins, 
        draws,
        f"{white_win_pct:.1f}%",
        f"{black_win_pct:.1f}%", 
        f"{draw_pct:.1f}%",
        f"{avg_moves:.1f}"
    ])
    
    # Afficher les résultats
    print(" " * 30, end='\r')  
    print(f"Results: White wins: {white_wins}, Black wins: {black_wins}, Draws: {draws}")
    print(f"Average moves per game: {avg_moves:.1f}")

def create_ai(color, level):
    """
    Crée une instance d'IA du niveau spécifié
    
    Args:
        color (str): 'White' ou 'Black'
        level (int): Niveau d'IA (0-3)
        
    Returns:
        Instance d'IA
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
        return RandomAI(color)  # Par défaut, IA aléatoire

def run_ai_game(game, white_ai, black_ai, max_moves=100):
    """
    Exécute une partie unique entre deux IAs
    
    Args:
        game: Instance de jeu
        white_ai: Instance d'IA pour le joueur Blanc
        black_ai: Instance d'IA pour le joueur Noir
        max_moves: Nombre maximum de coups avant de déclarer une partie nulle
    
    Returns:
        tuple: (nombre_de_coups, vainqueur)
    """
    move_count = 0
    
    while not game.game_over and move_count < max_moves:
        # Obtient l'IA actuelle en fonction du joueur
        current_ai = white_ai if game.current_player == 'White' else black_ai
        ai_move = current_ai.get_move(game.board)
        # Affiche le mouvement de l'IA
        if ai_move:
            from_pos, to_pos = ai_move
            success, message = game.make_move(from_pos, to_pos)  # Effectuer le mouvement
            if success:  # Si le mouvement est valide, on augmente le compteur de coups
                move_count += 1
            else:
                # Si le mouvement n'est pas valide, on affiche un message d'erreur
                print(f"AI attempted invalid move: {message}")
                game.game_over = True
                game.winner = 'Black' if game.current_player == 'White' else 'White'
        else:
            # Si l'IA ne trouve pas de mouvement valide, on déclare la partie nulle
            game.game_over = True
            game.winner = None  # Aucune victoire, partie nulle
    
    # Vérifier si la partie est nulle après le nombre maximum de coups (100 coups)
    if move_count >= max_moves and not game.game_over:
        return move_count, 'Draw'
    
    # Le match nul par répétition triple
    if (isinstance(game.winner, str) and game.winner.startswith("Draw")) or game.winner is None:
        return move_count, 'Draw'
    
    return move_count, game.winner

def main():
    """Fonction principale qui gère le menu du jeu et la logique de sélection"""
    while True:
        choice = display_main_menu()
        
        if choice == 1:  # Humain vs Humain
            play_human_vs_human()
            
        elif choice == 2:  # Humain vs IA
            ai_choice = display_ai_menu()
            
            if ai_choice == 5:  # Retour au menu principal
                continue
            
            color_choice = display_color_menu()
            
            if color_choice == 3:  # Retour au menu IA
                continue
            
            human_color = 'White' if color_choice == 1 else 'Black'
            ai_level = ai_choice - 1  # Convertir le choix en niveau d'IA
            
            play_human_vs_ai(ai_level, human_color)
            
        elif choice == 3:  # IA vs IA
            play_ai_vs_ai()
            
        elif choice == 4:  # Le tournoi IA
            run_ai_tournament()
            
        elif choice == 5:  # Les instructions
            clear_screen()
            display_title()
            display_instructions()
            input("\nPress Enter to return to the Main Menu...")
            
        elif choice == 6:  # Quitter le jeu
            print("\nThanks for playing Vietnamese Chess (Cờ Tướng)!")
            break

if __name__ == "__main__":
    main()