"""
AI_base.py - Classe de base pour les implémentations d'IA dans les Échecs Vietnamiens
Ce module définit la classe IA de base avec des fonctionnalités communes que
les implémentations spécifiques d'IA peuvent étendre.
"""

from Jeux.moves import get_valid_moves
from Jeux.pieces import PIECE_VALUES
from Jeux.board import Board

class BaseAI:
    """
    Classe de base pour les implémentations d'IA.
    
    Cette classe fournit des fonctionnalités communes pour tous les niveaux d'IA et
    définit l'interface que les implémentations spécifiques d'IA devraient suivre.
    """
    
    def __init__(self, color: str):
        """
        Initialise l'IA avec une couleur spécifique.
        
        Args:
            color (str): La couleur des pièces que l'IA contrôle ('White' ou 'Black')
        """
        self.color = color[0].upper()  # Ensure color is uppercase
        self.name = "Base AI"
    
    def get_move(self, board: Board) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Détermine le prochain mouvement de l'IA en fonction de l'état actuel du jeu.
        Cette méthode doit être redéfinie par des implémentations spécifiques d'IA.
        
        Args:
            game: L'état actuel du jeu
            
        Returns:
            tuple: ((from_x, from_y), (to_x, to_y)) représentant le mouvement
        """
        raise NotImplementedError("Specific AI implementations must override get_move")
    
    def get_all_valid_moves(self, color:str, board: Board)-> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Obtient tous les mouvements valides pour le joueur actuel.
        
        Args:
            game: L'état actuel du jeu
            
        Returns:
            list: Une liste de tuples ((from_x, from_y), (to_x, to_y)) pour tous les mouvements valides
        """
        all_moves = []
    
        for i in range(90):
            piece = board.grid[i]
            if piece != '  ' and piece[0] == color:
                # Obtenir tous les mouvements valides pour cette pièce
                piece_x, piece_y = board.to_2d(i)
                valid_moves = get_valid_moves(piece_x,piece_y, board)
                for move in valid_moves:
                    all_moves.append(((piece_x, piece_y), move))
        
        return all_moves
    
    def evaluate_board(self, board: Board)-> int:
        """
        Évalue la position actuelle du plateau du point de vue de l'IA.
        Des valeurs plus élevées sont meilleures pour l'IA.
        
        Args:
            board: Le plateau de jeu à évaluer
            
        Returns:
            int: Un score représentant à quel point la position est favorable
        """
        # Évaluation simple: somme des valeurs de toutes les pièces sur le plateau
        score = 0
        for i in range(90):
            piece = board.grid[i]
            if piece != '  ':
                # Ajouter des points pour ses propres pièces, soustraire pour celles de l'adversaire
                multiplier = 1 if piece[0] == self.color else -1
                score += multiplier * PIECE_VALUES[piece[1]]
        
        return score