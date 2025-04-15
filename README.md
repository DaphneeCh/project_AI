# Jeu d'Échecs Vietnamien (Cờ Tướng)

## Introduction

Ce projet est une implémentation du jeu d'échecs vietnamien, également connu sous le nom de "Cờ Tướng". C'est un jeu stratégique traditionnel similaire aux échecs chinois, joué sur un plateau avec des pièces spécifiques ayant chacune leurs propres mouvements et capacités.

## Description du Jeu

Le Cờ Tướng est un jeu de stratégie opposant deux joueurs qui tentent de capturer le Général (ou "Tướng") de l'adversaire. Chaque joueur contrôle des pièces distinctes avec différentes capacités de mouvement sur un plateau de jeu.

## Structure du Projet

Le projet est organisé comme suit:

- `main.py` - Point d'entrée du jeu
- `game.py` - Gestion de la logique du jeu
- `board.py` - Représentation du plateau de jeu
- `pieces.py` - Définition des différentes pièces du jeu
- `moves.py` - Logique des mouvements valides

## Comment Exécuter le Jeu

Pour lancer le jeu, exécutez la commande suivante dans le terminal:

```bash
python main.py
```

## Comment Jouer

1. Le jeu se joue en tour par tour
2. À votre tour, entrez les coordonnées de la pièce que vous souhaitez déplacer au format `x,y`
3. Les mouvements valides pour cette pièce seront affichés
4. Entrez ensuite les coordonnées de destination au format `x,y`
5. Pour annuler la sélection d'une pièce, tapez `back`
6. Pour quitter le jeu, tapez `quit` ou `exit`

## Technologies Utilisées

- Python 3
- Programmation orientée objet

## Note aux Développeurs

Pour contribuer au projet, assurez-vous de comprendre la structure du code et la logique du jeu d'échecs vietnamien.
