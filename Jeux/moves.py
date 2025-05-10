"""
moves.py - Implémente les règles de mouvement pour les Échecs Vietnamiens (Cờ Tướng)
Ce module contient des fonctions pour calculer les mouvements valides pour chaque type de pièce
selon les règles traditionnelles des Échecs Vietnamiens.
"""
import copy
from Jeux.board import Board

def get_valid_moves(x:int,y:int,board: Board) -> list:
    """
    Détermine tous les mouvements valides pour une pièce donnée sur le plateau actuel.

    Implémente les règles de mouvement spécifiques pour chaque type de pièce :
    - General: Se déplace d'une case dans n'importe quelle direction, restreint au palais. Deux Généraux ne peuvent pas se faire face directement sur la même ligne. Si c'est le cas, il doit y avoir une pièce de l'un ou l'autre camp bloquant leur vue.
    - Advisor: Se déplace d'une case en diagonale, restreint au palais.
    - Elephant: Se déplace en diagonale de deux cases, ne peut pas traverser la rivière. S'il y a une autre pièce au milieu de cette ligne diagonale, l'Éléphant est bloqué et ne peut pas se déplacer.
    - Horse: Se déplace en forme de 'L', deux cases dans une direction et une case perpendiculaire. S'il y a une autre pièce à l'intersection adjacente à l'étape verticale ou horizontale, le Cheval est bloqué et ne peut pas se déplacer.
    - Rook: Se déplace horizontalement ou verticalement d'un nombre quelconque de cases.
    - Cannon: Se déplace comme une Rook mais capture en sautant par-dessus une pièce.
    - Soldier: Se déplace d'une case vers l'avant, peut se déplacer latéralement après avoir traversé la rivière.
    
    Args:
        x (int): La coordonnée x de la pièce
        y (int): La coordonnée y de la pièce
        board (Board): Le plateau de jeu actuel
        
    Returns:
        list: Une liste de tuples (x, y) représentant les coordonnées de destination valides
    """
    moves = []
    piece = board.grid[board.to_1d(x, y)]
    
    if piece[1] == 'G':  # General
        # General se déplace d'une case dans n'importe quelle direction, restrict au palais
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 3 <= nx <= 5 and ((0 <= ny <= 2 and piece[0] == 'B') or (7 <= ny <= 9 and piece[0] == 'W')):
                target = board.grid[board.to_1d(nx, ny)]
                if target == '  ' or target[0] != piece[0]:
                    # Créer un plateau temporaire pour vérifier si ce mouvement résulterait en des généraux face à face
                    temp_board = copy.deepcopy(board)
                    temp_board.move_piece(x,y, nx, ny)
                    if not temp_board.is_general_facing_general():
                        moves.append((nx, ny))
    
    elif piece[1] == 'A':  # Advisor
        # Advisor se déplace d'une case en diagonale, restreint au palais
        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 3 <= nx <= 5 and ((0 <= ny <= 2 and piece[0] == 'B') or (7 <= ny <= 9 and piece[0] == 'W')):
                target = board.grid[board.to_1d(nx, ny)] if board.is_in_bounds(nx, ny) else None
                if target == '  ' or target[0] != piece[0]:
                    moves.append((nx, ny))
    
    elif piece[1] == 'E':  # Elephant
        # Elephant se déplace en diagonale de deux cases, ne peut pas traverser la rivière
        directions = [(2,2), (2,-2), (-2,2), (-2,-2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Vérifier si le mouvement est dans les limites et ne traverse pas la rivière
            if board.is_in_bounds(nx, ny) and ((ny <= 4 and piece[0] == 'B') or (ny >= 5 and piece[0] == 'W')):
                # Vérifier s'il y a une pièce au milieu de la diagonale
                block_x, block_y = x + dx//2, y + dy//2
                if board.grid[board.to_1d(block_x, block_y)] == '  ': 
                    target = board.grid[board.to_1d(nx, ny)]
                    if target == '  ' or target[0] != piece[0]:
                        moves.append((nx, ny))
    
    elif piece[1] == 'H':  # Horse
        # Horse se déplace en forme de 'L', deux cases dans une direction et une case perpendiculairement
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            # Première étape
            step_x, step_y = x + dx, y + dy
            if board.is_in_bounds(step_x, step_y) and board.grid[board.to_1d(step_x, step_y)] == '  ':  # No blocking
                # Deuxième étape
                diagonals = []
                if dx == 0:  # Permiere étape verticale
                    diagonals = [(1, dy*2), (-1, dy*2)]
                else:  # Premiere étape horizontale
                    diagonals = [(dx*2, 1), (dx*2, -1)]
                
                for nx, ny in diagonals:
                    nx, ny = x + nx, y + ny
                    if board.is_in_bounds(nx, ny):
                        target = board.grid[board.to_1d(nx, ny)]
                        if target == '  ' or target[0] != piece[0]:
                            moves.append((nx, ny))
    
    elif piece[1] == 'R':  # Rook (Chariot)
        # Rook se déplace horizontalement ou verticalement d'un nombre quelconque de cases
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while board.is_in_bounds(nx, ny):
                target = board.grid[board.to_1d(nx, ny)]
                if target == '  ':
                    moves.append((nx, ny))
                else:
                    if target[0] != piece[0]:
                        moves.append((nx, ny))
                    break
                nx, ny = nx + dx, ny + dy
    
    elif piece[1] == 'C':  # Cannon
        # Cannon se déplace comme une Rook mais capture en sautant par-dessus une pièce
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Déplacement sans capture
            while board.is_in_bounds(nx, ny) and board.grid[board.to_1d(nx, ny)] == '  ':
                moves.append((nx, ny))
                nx, ny = nx + dx, ny + dy
            
            # Trouvé une plateforme potentielle pour sauter par-dessus
            if board.is_in_bounds(nx, ny):
                platform_x, platform_y = nx, ny
                nx, ny = nx + dx, ny + dy
                # Chercher une pièce à capturer après la plateforme
                while board.is_in_bounds(nx, ny):
                    target = board.grid[board.to_1d(nx, ny)]
                    if target != '  ':
                        if target[0] != piece[0]:
                            moves.append((nx, ny))
                        break
                    nx, ny = nx + dx, ny + dy
    
    elif piece[1] == 'S':  # Soldier
        # Soldier se déplace d'une case vers l'avant, peut se déplacer latéralement après avoir traversé la rivière
        directions = []
        
        # Déterminer la direction de mouvement en fonction de la couleur
        if piece[0] == 'B': # Black
            directions.append((0, 1))  # Se déplace vers le bas
            if y > 4:  # A traversé la rivière
                directions.extend([(1, 0), (-1, 0)])  # Peut se déplacer horizontalement
        else:  # White
            directions.append((0, -1))  # Se déplace vers le haut
            if y < 5:  # A traversé la rivière
                directions.extend([(1, 0), (-1, 0)])  # Peut se déplacer horizontalement
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if board.is_in_bounds(nx, ny):
                target = board.grid[board.to_1d(nx, ny)]
                if target == '  ' or target[0] != piece[0]:
                    moves.append((nx, ny))
    
    return moves