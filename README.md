# Jeu d'Échecs Vietnamien (Cờ Tướng)

## Introduction

Ce projet est une implémentation complète du jeu d'échecs vietnamien, également connu sous le nom de "Cờ Tướng" ou "Xiangqi". Il s'agit d'un jeu de stratégie traditionnel originaire d'Asie, similaire aux échecs occidentaux mais avec des règles et des pièces distinctes. Cette version numérique permet de jouer en mode humain contre humain, humain contre IA, ou même d'organiser des tournois d'IA pour comparer différents niveaux d'intelligence artificielle.

## Description du Jeu

Le Cờ Tướng se joue sur un plateau de 9×10 cases. L'objectif est de mettre en échec et mat le Général adverse. Contrairement aux échecs occidentaux, les pièces sont placées aux intersections des lignes plutôt qu'à l'intérieur des cases.

### Caractéristiques du plateau

- Le plateau est divisé par une "rivière" au milieu
- Chaque côté possède un "palais" de 3×3 cases où le Général et ses Conseillers doivent rester
- Les pièces ont des mouvements spécifiques qui peuvent changer après avoir traversé la rivière

## Fonctionnalités

- Interface en ligne de commande intuitive
- Multiples modes de jeu:
  - Humain contre Humain
  - Humain contre IA (4 niveaux de difficulté)
  - IA contre IA
  - Tournois automatisés entre différentes IA
- Système d'IA à plusieurs niveaux:
  - Niveau 0: Mouvements aléatoires
  - Niveau 1: IA débutante (capture prioritaire)
  - Niveau 2: IA intermédiaire (algorithme minimax)
  - Niveau 3: IA avancée (minimax avec élagage alpha-bêta)
- Visualisation du plateau et des mouvements possibles
- Système d'analyse et d'explication des pièces du jeu

## Structure du Projet

Le projet est organisé comme suit:

- `Jeux/main.py` - Point d'entrée du programme et gestion de l'interface
- `Jeux/game.py` - Gestion de la logique du jeu et des tours
- `Jeux/board.py` - Implémentation du plateau et de son état
- `Jeux/pieces.py` - Définition des différentes pièces et leurs valeurs
- `Jeux/moves.py` - Logique des mouvements valides pour chaque type de pièce
- `AI/AI_base.py` - Classe de base pour toutes les implémentations d'IA
- `AI/AI_lv0.py` - Implémentation de l'IA de niveau 0 (aléatoire)
- `AI/AI_lv1.py` - Implémentation de l'IA de niveau 1 (débutant)
- `AI/AI_lv2.py` - Implémentation de l'IA de niveau 2 (intermédiaire)
- `AI/AI_optimal.py` - Implémentation de l'IA de niveau 3 (avancée)

## Installation et Prérequis

### Prérequis

- Python 3.11

### Installation

```bash

# Exécutez le jeu
python Jeux/main.py
```

## Comment Exécuter le Jeu

Pour lancer le jeu, exécutez la commande suivante dans le terminal:

```bash
python Jeux/main.py
```

## Comment Jouer

### Commandes de base

1. Le jeu se joue en tour par tour
2. À votre tour, entrez les coordonnées de la pièce que vous souhaitez déplacer au format `x,y`
3. Les mouvements valides pour cette pièce seront affichés
4. Entrez ensuite les coordonnées de destination au format `x,y`

### Commandes spéciales

- `back` - Annuler la sélection d'une pièce
- `quit` ou `exit` - Quitter le jeu
- `help` - Afficher les instructions du jeu
- `explain x,y` - Obtenir des informations sur la pièce à la position x,y

## Types de Pièces

- **Général (G)**: Se déplace d'une case dans toutes les directions, confiné au palais
- **Advisor (A)**: Se déplace d'une case en diagonale, confiné au palais
- **Éléphant (E)**: Se déplace exactement de deux cases en diagonale, ne peut pas traverser la rivière
- **Cheval (H)**: Se déplace en forme de "L", peut être bloqué
- **Chariot (R)**: Se déplace horizontalement et verticalement sans limite de distance
- **Canon (C)**: Se déplace comme le Chariot, mais doit sauter par-dessus une pièce pour capturer
- **Soldat (S)**: Se déplace d'une case vers l'avant, peut se déplacer latéralement après avoir traversé la rivière

## Mode Tournoi d'IA

Le programme inclut un mode tournoi pour évaluer les performances des différentes IA:

- Exécution automatisée de plusieurs parties entre différentes combinaisons d'IA
- Statistiques détaillées (taux de victoire, nombre moyen de coups, etc.)
- Exportation des résultats au format CSV pour analyse

## Technologies Utilisées

- Python 3
- Programmation orientée objet
- Algorithmes d'IA (minimax, élagage alpha-bêta)
- Structures de données optimisées pour la représentation du jeu

## Contribuer au Projet

Pour contribuer:

1. Assurez-vous de comprendre les règles du jeu d'échecs vietnamien
2. Respectez la structure de code existante
3. Ajoutez des tests pour les nouvelles fonctionnalités
4. Documentez clairement vos modifications

## Auteurs

- [Daphnee] - Développement initial
