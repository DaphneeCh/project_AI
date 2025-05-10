"""
pieces.py - Définit les pièces utilisées dans les Échecs Vietnamiens (Cờ Tướng)
Ce module contient la classe Piece et les constantes de valeur des pièces utilisées dans le jeu.
"""

# Définir les valeurs des pièces
PIECE_VALUES = {
    'G': 10000,
    'R': 9,
    'C': 4.5,
    'H': 4,
    'E': 2,
    'A': 2,
    'S': 1
}

# Définir les types de pièces
PIECE_TYPES = {
    'General': 'G',
    'Rook': 'R',
    'Cannon': 'C',
    'Horse': 'H',
    'Elephant': 'E',
    'Advisor': 'A',
    'Soldier': 'S',
    'White': 'W',
    'Black': 'B'
}
# Dictionnaire inversé des types de pièces
PIECE_TYPES_REVERSE = {v: k for k, v in PIECE_TYPES.items()}

# Dictionnaire des symboles de pièces et leurs explications
PIECE_SYMBOLS = {
    "R": "Rook (Xe): Se déplace horizontalement ou verticalement sur n'importe quel nombre de cases.",
    "C": "Cannon (Pháo): Se déplace comme une Tour mais capture en sautant par-dessus une pièce.",
    "H": "Horse (Mã): Se déplace en forme de 'L', deux cases dans une direction et une case perpendiculairement. Si une autre pièce se trouve à l'intersection adjacente à l'étape verticale ou horizontale, le Cheval est bloqué et ne peut pas se déplacer.",
    "E": "Éléphant (Tượng): Se déplace en diagonale de deux cases, ne peut pas traverser la rivière. Si une autre pièce se trouve au milieu de cette ligne diagonale, l'Éléphant est bloqué et ne peut pas se déplacer.",
    "A": "Advisor (Sĩ): Se déplace d'une case en diagonale, limité au palais.",
    "G": "General (Tướng): Se déplace d'une case dans n'importe quelle direction, limité au palais. Deux Généraux ne peuvent pas se faire face directement sur la même ligne. Si c'est le cas, il doit y avoir une pièce de l'un ou l'autre camp bloquant leur vue.",
    "S": "Soldier (Binh): Se déplace d'une case vers l'avant, peut se déplacer latéralement après avoir traversé la rivière.",
}
