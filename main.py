import tkinter as tk
from tkinter import messagebox

# Paramètres de la grille
ROWS = 6
COLS = 7
NB_JETONS_V = 4
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 5

# Couleurs des jetons
PLAYER_COLORS = {0:"white", 1: "#FF0000", 2: "#FFD700"}

# Grille de jeu (0 = vide, 1 = joueur 1, 2 = joueur 2)
grid = [[0] * COLS for _ in range(ROWS)]
liste_jetons = []
current_player = 1  # j1 commence
canvas = None
canvas_tour = None
winner = None
