"""
AI_optimal.py - Implémente une IA avancée utilisant l'algorithme minimax avec élagage alpha-bêta
Cette IA utilise des techniques avancées pour trouver les coups optimaux dans le jeu d'échecs vietnamien.
"""

from AI.AI_base import BaseAI
import random
import copy
from Jeux.pieces import PIECE_VALUES
from Jeux.board import Board
from Jeux.moves import get_valid_moves

class AI(BaseAI):
    """
    IA Optimale - Effectue des mouvements en utilisant l'algorithme minimax avec élagage alpha-bêta.
    Cette IA utilise des heuristiques avancées et des techniques d'optimisation pour un jeu plus fort.
    """
    
    def __init__(self, color: str):
        """
        Initialise l'IA.
        
        Args:
            color (str): La couleur de l'IA ('White' ou 'Black')
        """
        super().__init__(color)
        self.name = "Optimal AI (Advanced)"
        self.search_depth = 3 # Profondeur de recherche 
    
    def get_move(self, board: Board) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """
        Sélectionne un mouvement en utilisant l'algorithme minimax avec élagage alpha-bêta.
        
        Args:
            board: L'état actuel du plateau
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) représentant le mouvement choisi
        """
        
        # Obtient tous les mouvements valides possibles
        all_moves = self.get_all_valid_moves(self.color, board)
        
        if len(all_moves) == 0:
            return None  # Aucun mouvement valide disponible
        
        # Si un seul mouvement est possible, le retourner immédiatement
        if len(all_moves) == 1:
            return all_moves[0]
        
        # Initialise les variables pour le meilleur mouvement
        best_moves = []
        best_score = float('-inf')
        
        # Ordonner les mouvements selon une heuristique simple pour un meilleur élagage
        ordered_moves = self._order_moves(all_moves, board)

        # Créer une copie du plateau pour l'évaluation
        board_copy = copy.deepcopy(board)
        for move in ordered_moves:
            # Effecuer le mouvement sur une copie du plateau
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
                
            start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
            target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
            # Essayer de faire le mouvement sur la copie du plateau
            try:
                capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                if capture[1] == 'G' and capture[0] != self.color:
                    # Retourner immédiatement un mouvement qui capture le général adverse
                    return move
            except Exception as e:
                continue
                
            # Utiliser minimax avec élagage alpha-bêta pour évaluer
            score = self._alpha_beta(board_copy, self.search_depth - 1, float('-inf'), float('inf'), False)
                
            # Verifier si le score est meilleur que le meilleur score actuel
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
                
            # Annuler le mouvement sur la copie du plateau
            board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
            board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell
                
        # Si plusieurs mouvements ont le même meilleur score, choisir l'un d'eux au hasard
        if len(best_moves)>0:
            return random.choice(best_moves)
        else:
            # Revenir à un mouvement aléatoire si quelque chose s'est mal passé
            return random.choice(all_moves)
    
    def _order_moves(self, moves: list, board: Board) -> list:
        """
        Ordonne les mouvements pour améliorer l'efficacité de l'élagage alpha-bêta.
        Les mouvements de capture et les mouvements vers le centre sont vérifiés en premier.
        
        Args:
            moves: Liste des mouvements possibles
            board: État actuel du plateau
            
        Returns:
            list: Liste ordonnée des mouvements
        """
        move_values = []
        
        for move in moves:
            from_pos, to_pos = move
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            # Initialiser la valeur du mouvement
            value = 0
            
            # Vérifier si le mouvement est une capture
            source = board.grid[board.to_1d(from_x, from_y)]
            target = board.grid[board.to_1d(to_x, to_y)]
            if target != '  ' and target[0] != source[0]:
                # Valeur basée sur le type de pièce
                piece_type = target[1]
                value = PIECE_VALUES[piece_type]
                    
            move_values.append((value, move))
        
        # Trier les mouvements en ordre décroissant de valeur
        move_values.sort(key=lambda x: x[0], reverse=True)
        
        # Retourner uniquement les mouvements
        return [move for _, move in move_values]
    
    def _alpha_beta(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool):
        """
        Algorithme minimax avec élagage alpha-bêta.
        
        Args:
            board: État actuel du plateau
            depth: Nombre de coups à anticiper
            alpha: Valeur alpha pour l'élagage
            beta: Valeur bêta pour l'élagage
            is_maximizing: Si nous maximisons ou minimisons
            
        Returns:
            float: Score pour la position actuelle du plateau
        """
        
        # Cas de base : limite de profondeur atteinte ou partie terminée
        if depth == 0:
            eval_score = self.evaluate_board(board)
            return eval_score
        
        # Obtient la couleur du joueur actuel
        current_color = self.color if is_maximizing else 'B' if self.color == 'W' else 'W'

        # Obtient tous les mouvements valides possibles pour le joueur actuel
        all_possible_moves = self.get_all_valid_moves(current_color, board)
        
        # Si aucun mouvement valide n'est disponible
        if len(all_possible_moves) == 0:
            return 0
        
        # Ordonner les mouvements pour améliorer l'efficacité de l'élagage
        ordered_moves = self._order_moves(all_possible_moves, board)
        
        # Créer une copie du plateau pour l'évaluation
        board_copy = copy.deepcopy(board)
        if is_maximizing:
            best_score = float('-inf')
            for move in ordered_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Sauvegarder l'état d'origine du plateau
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
                # Simuler le mouvement
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                    if capture[1] == 'G' and capture[0] != current_color:
                        # Retourner une haute valeur pour capturer le général
                        return 10000
                except Exception as e:
                    continue
                
                # Évaluer ce mouvement récursivement
                score = self._alpha_beta(board_copy, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                
                # Annuler le mouvement sur la copie du plateau
                board_copy.grid[board_copy.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board_copy.to_1d(to_x, to_y)] = target_cell
                
                if best_score >= beta:
                    break  # Elagage bêta
                # mise à jour alpha
                alpha = max(alpha, best_score)
                
            return best_score
        else:
            best_score = float('inf')
            for move in all_possible_moves:
                from_pos, to_pos = move
                from_x, from_y = from_pos
                to_x, to_y = to_pos
                
                # Sauvegarder l'état d'origine du plateau
                start_cell = board_copy.grid[board_copy.to_1d(from_x, from_y)]
                target_cell = board_copy.grid[board_copy.to_1d(to_x, to_y)]
                
                # Simuler le mouvement
                try:
                    capture = board_copy.move_piece(from_x, from_y, to_x, to_y)
                    if capture[1] == 'G' and capture[0] != current_color:
                        # Retourner une basse valeur pour capturer le général
                        return -10000
                except Exception:
                    continue
                
                # Évaluer ce mouvement récursivement
                score = self._alpha_beta(board_copy, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                
                # Annuler le mouvement sur la copie du plateau
                board_copy.grid[board.to_1d(from_x, from_y)] = start_cell
                board_copy.grid[board.to_1d(to_x, to_y)] = target_cell
                
                if best_score < alpha:
                    break  # Elagage alpha
                # Mise à jour bêta
                beta = min(beta, best_score)
                
            return best_score
    