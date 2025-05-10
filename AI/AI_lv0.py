"""
AI_lv0.py - Implémente l'IA la plus simple qui fait des mouvements aléatoires
Cette IA sélectionne aléatoirement parmi les mouvements valides disponibles sans aucune stratégie.
"""

import random
from AI.AI_base import BaseAI
from Jeux.board import Board

class AI(BaseAI):
    """
    IA niveau 0 - Fait des mouvements complètement aléatoires.
    C'est l'implémentation d'IA la plus simple sans aucune considération stratégique.
    """
    
    def __init__(self, color: str):
        """
        Initialise l'IA aléatoire.
        
        Args:
            color (str): La couleur des pièces que l'IA contrôle ('White' ou 'Black')
        """
        super().__init__(color)
        self.name = "Random AI (Level 0)"
    
    def get_move(self, board: Board)-> tuple[tuple[int, int], tuple[int, int]]:
        """
        Sélectionne un mouvement valide aléatoire.
        
        Args:
            board: L'état actuel du plateau de jeu
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) représentant le mouvement choisi
        """
        all_moves = self.get_all_valid_moves(self.color, board)
        
        if len(all_moves) == 0:
            # Aucun mouvement valide disponible
            return None
            
        return random.choice(all_moves)
