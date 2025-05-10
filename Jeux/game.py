"""
game.py - Gère l'état du jeu pour les Échecs Vietnamiens (Cờ Tướng)
Ce module contient la classe Game qui gère les tours de jeu, la validation des mouvements,
les conditions de victoire et le suivi de l'état du jeu.
"""

from Jeux.board import Board
from Jeux.moves import get_valid_moves

class Game:
    """
    Gère l'état global du jeu et ses règles.
    
    Attributs:
        board (Board): Le plateau de jeu
        current_player (str): Le joueur actuel ('White' pour Blanc ou 'Black' pour Noir)
        game_over (bool): Indique si le jeu est terminé
        winner (str ou None): Le vainqueur du jeu, s'il y en a un
        captured_pieces (dict): Pièces capturées par chaque joueur
        board_states (dict): Enregistrement des positions du plateau pour détecter les répétitions
    """
    def __init__(self):
        self.board = Board()
        self.current_player = 'White'
        self.game_over = False
        self.winner = None
        self.captured_pieces = {'White': [], 'Black': []}
        self.board_states = {}  # Dictionnaire pour stocker les états du plateau (clé: état, valeur: occurrences)
        self.update_board_state() 

    def get_board_state_key(self):
        """
        Crée une représentation hachée de l'état actuel du plateau.
        Retourne une chaîne de caractères qui représente la position du plateau et à qui c'est le tour.
        """
        # Convertit le plateau en une chaîne de caractères
        board_str = self.board.to_string()
        
        # Ajoute le joueur actuel à la chaîne
        state = board_str + "-" + self.current_player
        return state
        
    def update_board_state(self):
        """
        Met à jour l'historique de l'état du plateau.
        Convertit la position actuelle du plateau en une représentation sous forme de chaîne de caractères et compte les occurrences.
        """
        state = self.get_board_state_key()
        if state in self.board_states:
            self.board_states[state] += 1
        else:
            self.board_states[state] = 1
            
        # Vérifie si l'état du plateau a été répété trois fois ce qui entraîne une partie nulle
        if self.board_states[state] >= 3:
            self.game_over = True
            self.winner = "Draw (Threefold Repetition)"

    def switch_player(self):
        """
        Change le joueur actuel de Blanc à Noir ou vice versa.
        """
        self.current_player = 'Black' if self.current_player == 'White' else 'White'

    def make_move(self, from_pos: tuple[int,int], to_pos: tuple[int,int]) -> tuple[bool, str]:
        """
        Tente de déplacer une pièce d'une position à une autre.
        
        Args:
            from_pos (tuple): La position de départ (x, y)
            to_pos (tuple): La position de destination (x, y)
            
        Returns:
            tuple: (succès, message) où succès est un booléen et
                  message est une chaîne de caractères expliquant le résultat
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

        # Effectuer le mouvement
        captured = self.board.move_piece(from_x, from_y, to_x, to_y)
        if captured != '  ':
            self.captured_pieces[self.current_player].append(captured)
            if captured[1] == 'G':
                self.game_over = True
                self.winner = self.current_player

        # Passer au joueur suivant
        self.switch_player()
        
        # Mettre à jour l'état du plateau et vérifier les répétitions
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