"""
AI_lv1.py - Implémente une IA de niveau débutant qui priorise la capture des pièces adverses
Cette IA utilise une approche simple et gourmande pour sélectionner les mouvements qui capturent les pièces de la plus haute valeur.
"""

from AI.AI_base import BaseAI
import random
from Jeux.board import Board
from Jeux.pieces import PIECE_VALUES

class AI(BaseAI):
    """
    IA de niveau 1 - Utilise une stratégie simple et gourmande.
    Cette IA priorise la capture des pièces adverses, en particulier celles de haute valeur.
    """
    
    def __init__(self, color: str):
        """
        Initialiser l'IA Débutant.
        
        Args:
            color (str): La couleur des pièces contrôlées par l'IA ('White' ou 'Black')
        """
        super().__init__(color)
        self.name = "Beginner AI (Level 1)"
    
    def get_move(self, board: Board)-> tuple[tuple[int, int], tuple[int, int]]:
        """
        Sélectionne un mouvement en priorisant la capture des pièces de haute valeur.
        
        Args:
            board: L'état actuel du plateau de jeu
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) représentant le mouvement choisi
        """
        all_moves = self.get_all_valid_moves(self.color,board)
        
        if len(all_moves) == 0:
            return None  # Aucun mouvement valide disponible
        
        # Calculer la valeur de chaque mouvement
        valued_moves = []
        for move in all_moves:
            # move est un tuple de ((from_x, from_y), (to_x, to_y))
            from_pos, to_pos = move
            # from_pos et to_pos sont des tuples (x, y)
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            # Vérifier si on capture une pièce
            target_piece = board.grid[board.to_1d(to_x, to_y)]
            
            if target_piece != '  ':
                if target_piece[0] != self.color:
                    # Plus grande valeur pour la capture de pièces de haute valeur
                    capture_value = PIECE_VALUES[target_piece[1]]  # Obtenir la valeur de la pièce capturée
                    valued_moves.append((move, capture_value))
            else:
                # Pas de capture
                valued_moves.append((move, 0))
        
        # Trier les mouvements par valeur (du plus élevé au plus bas)
        valued_moves.sort(key=lambda x: x[1], reverse=True)
        
        # S'il y a des captures disponibles, sélectionner celle de la plus haute valeur
        if valued_moves[0][1] > 0:
            return valued_moves[0][0]
        
        # Sinon, faire un mouvement aléatoire
        return random.choice(all_moves)