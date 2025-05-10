"""
board.py - Implémente le plateau de jeu pour les Échecs Vietnamiens (Cờ Tướng)
Ce module contient la classe Board qui gère la grille de jeu, le placement des pièces,
les mouvements et la visualisation de l'état du plateau.
"""

class Board:
    """
    Représente le plateau de jeu avec une grille de 9x10.
    
    Le plateau est orienté avec (0,0) dans le coin supérieur gauche.
    Les pièces noires commencent en haut (lignes 0-4) et les pièces blanches en bas (lignes 5-9).
    
    Attributs:
        grid (list): Une liste 2D représentant le plateau 9x10 avec des pièces ou None
    """
    def __init__(self):
        # Initialise une liste 1D représentant le plateau 9x10 (90 positions)
        self.grid = ['  '] * 90
        
        # Méthodes auxiliaires pour convertir entre les coordonnées 1D et 2D
        self.to_1d = lambda x, y: y * 9 + x
        self.to_2d = lambda i: (i % 9, i // 9)
        self.place_initial_pieces()

    def place_initial_pieces(self):
        """
        Configure la position initiale de toutes les pièces sur le plateau selon
        les règles traditionnelles des Échecs Vietnamiens.
        """
        # Place les généraux
        self.grid[self.to_1d(4, 0)] = 'BG'
        self.grid[self.to_1d(4, 9)] = 'WG'

        # Place les conseillers
        self.grid[self.to_1d(3, 0)] = 'BA'
        self.grid[self.to_1d(5, 0)] = 'BA'
        self.grid[self.to_1d(3, 9)] = 'WA'
        self.grid[self.to_1d(5, 9)] = 'WA'
        
        # Place les éléphants
        self.grid[self.to_1d(2, 0)] = 'BE'
        self.grid[self.to_1d(6, 0)] = 'BE'
        self.grid[self.to_1d(2, 9)] = 'WE'
        self.grid[self.to_1d(6, 9)] = 'WE'

        # Place les chevaux
        self.grid[self.to_1d(1, 0)] = 'BH'
        self.grid[self.to_1d(7, 0)] = 'BH'
        self.grid[self.to_1d(1, 9)] = 'WH'
        self.grid[self.to_1d(7, 9)] = 'WH'
        
        # Place les chariots
        self.grid[self.to_1d(0, 0)] = 'BR'
        self.grid[self.to_1d(8, 0)] = 'BR'
        self.grid[self.to_1d(0, 9)] = 'WR'
        self.grid[self.to_1d(8, 9)] = 'WR'

        # Place les canons
        self.grid[self.to_1d(1, 2)] = 'BC'
        self.grid[self.to_1d(7, 2)] = 'BC'
        self.grid[self.to_1d(1, 7)] = 'WC'
        self.grid[self.to_1d(7, 7)] = 'WC'

        # Place les soldats
        for i in range(0, 9, 2):
            self.grid[self.to_1d(i, 3)] = 'BS'
            self.grid[self.to_1d(i, 6)] = 'WS'

    def move_piece(self, curr_x: int, curr_y: int, new_x: int, new_y: int):
        """
        Déplace une pièce vers une nouvelle position sur le plateau.
        
        Args:
            curr_x (int): La coordonnée x actuelle de la pièce
            curr_y (int): La coordonnée y actuelle de la pièce
            new_x (int): La coordonnée x de destination
            new_y (int): La coordonnée y de destination
            
        Returns:
            capture (str or None): La pièce capturée, le cas échéant

        """
        capture = None
        curr_idx = self.to_1d(curr_x, curr_y)
        new_idx = self.to_1d(new_x, new_y)
        
        if self.grid[curr_idx] == '  ': 
            raise ValueError("No piece at the current position")
        if not self.is_in_bounds(new_x, new_y):
            raise ValueError("New position out of bounds")
            
        current_piece = self.grid[curr_idx]
        self.grid[curr_idx] = '  '
        capture = self.grid[new_idx]
        self.grid[new_idx] = current_piece
        
        return capture


    def display(self):
        """
        Affiche l'état actuel du plateau dans une grille formatée.
        """
        print("  ", end="")
        for i in range(9):
            print(f"  {i}  ", end="")
        print()
        print("  +----+----+----+----+----+----+----+----+----+")
        
        for y in range(10):
            print(f"{y} |", end="")
            for x in range(9):
                piece = self.grid[self.to_1d(x, y)]
                piece_str = str(piece) if piece else "  "
                print(f"{piece_str:^4}", end="|")
            print()
            print("  +----+----+----+----+----+----+----+----+----+")
        print()

    def is_in_bounds(self, x:int, y:int)-> bool:
        return 0 <= x < 9 and 0 <= y < 10

    def is_general_facing_general(self)-> bool:
        # Trouver les deux généraux
        white_general = None
        black_general = None
        
        for i in range(90):
            piece = self.grid[i]
            if piece == 'WG':
                white_general = self.to_2d(i)
            elif piece == 'BG':
                black_general = self.to_2d(i)
        
        if not white_general or not black_general:
            return False
            
        # Vérifier s'ils sont dans la même colonne
        if white_general[0] != black_general[0]:
            return False
        
        x = white_general[0]
        # Vérifier s'il y a des pièces entre eux
        min_y = min(white_general[1], black_general[1])  
        max_y = max(white_general[1], black_general[1])  
        
        for y in range(min_y + 1, max_y):
            if self.grid[self.to_1d(x, y)] != '  ': 
                # Il y a une pièce bloquant la ligne de vue
                return False
                
        return True
    
    def _hash_board(self) -> str:
        """
        Crée un simple hash de l'état actuel du plateau pour la table de transposition.
        
        Returns:
            str: Une chaîne de hash représentant l'état du plateau
        """
        return "|".join(self.grid)
    
    def to_string(self) -> str:
        """
        Convertit le plateau en une représentation sous forme de chaîne de caractères.
        
        Returns:
            str: Une représentation sous forme de chaîne de caractères du plateau
        """
        return self._hash_board()