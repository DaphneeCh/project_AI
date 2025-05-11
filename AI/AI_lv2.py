"""
AI_lv2.py - Implémente une IA de niveau intermédiaire utilisant l'algorithme minimax
Cette IA anticipe quelques coups pour prendre des décisions plus stratégiques.
"""

from AI.AI_base import BaseAI
import random
import copy
from Jeux.pieces import PIECE_VALUES
from Jeux.board import Board

class AI(BaseAI):
    """
    IA de niveau 2 - Utilise l'algorithme minimax avec une profondeur limitée.
    Cette IA anticipe quelques coups pour prendre de meilleures décisions stratégiques.
    """
    
    def __init__(self, color: str):
        """
        Initialise l'IA intermédiaire.
        
        Args:
            color (str): La couleur des pièces contrôlées par l'IA ('White' ou 'Black')
        """
        super().__init__(color)
        self.name = "Intermediate AI (Level 2)"
        self.search_depth = 2  # Profondeur de recherche pour l'algorithme minimax
    
    def get_move(self, board:Board) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Utilise l'algorithme minimax pour trouver le meilleur coup en anticipant quelques mouvements.
        
        Args:
            board: L'état actuel du plateau
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) représentant le coup choisi
        """
        # Récupérer tous les mouvements valides
        all_moves = self.get_all_valid_moves(self.color,board)
        
        if len(all_moves) == 0:
            return None  # Aucun mouvement possible
        
        best_score = float('-inf')
        best_moves = []  # Stocker les meilleurs mouvements
        
        # Évaluer chaque mouvement en créant une copie du plateau
        board_copy = copy.deepcopy(board)
        for move in all_moves:
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos

            start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
            target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
            
            # Déplacer la pièce dans la grille copiée
            try:
                capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                if capture[1] == 'G' and capture[0] != self.color:
                    # Si ce mouvement capture le général, c'est un coup gagnant
                    return move
            except Exception as e:
                continue  

            # Évaluer ce mouvement en utilisant minimax
            score = self.minimax(board_copy, self.search_depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)  # Ajouter à la liste des meilleurs mouvements
                
            # Annuler le mouvement
            board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
            board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell
        
        
        # Choisir un mouvement parmi les meilleurs
        if len(best_moves) > 0:
            return random.choice(best_moves)
        else:
            # Si aucun mouvement meilleur n'est trouvé, choisir un mouvement aléatoire parmi tous les mouvements valides
            return random.choice(all_moves) if all_moves else None
    
    def minimax(self, board: Board, depth: int, is_maximizing: bool) -> float:
        """
        Implémentation de l'algorithme minimax.
        
        Args:
            game: État actuel du jeu
            depth: Combien de couches supplémentaires à explorer
            is_maximizing: Vrai s'il s'agit du tour du joueur maximisant (tour de l'IA)
            
        Returns:
            float: Score pour cet état du jeu
        """
        # Condition d'arrêt
        if depth == 0:
            return self.evaluate_board(board)
        
        # Obtenir la couleur du joueur actuel
        current_color = self.color if is_maximizing else 'B' if self.color == 'W' else 'W'
        
        # Obtenir tous les mouvements valides pour le joueur actuel
        all_moves = self.get_all_valid_moves(current_color, board)
        
        # S'il n'y a pas de mouvements disponibles, c'est un état terminal
        if len(all_moves) == 0:
            return 0  # Draw
        
        # Créer une copie du plateau pour évaluer les mouvements
        board_copy = copy.deepcopy(board)
        if is_maximizing:
            max_eval = float('-inf')
            for move in all_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                # Déplacer la pièce dans la grille copiée
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                except Exception as e:
                    continue
                # Évaluer ce mouvement en utilisant minimax            
                eval = self.minimax(board_copy, depth - 1, False)
                max_eval = max(max_eval, eval)
                # Annuler le mouvement
                board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell
            # Si l'IA maximisante est en train de jouer, retourner le meilleur score
            return max_eval
        else:
            min_eval = float('inf')
            for move in all_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
                # Déplacer la pièce dans la grille copiée
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)

                except Exception as e:
                    continue
                # Évaluer ce mouvement en utilisant minimax
                eval = self.minimax(board_copy, depth - 1, True)
                min_eval = min(min_eval, eval)
            
                # Annuler le mouvement
                board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell

            # Si l'IA minimisant est en train de jouer, retourner la valeur minimale
            return min_eval