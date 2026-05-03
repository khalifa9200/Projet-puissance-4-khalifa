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

# Fonctions de logique de jeu
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def access(r, c, nb_jetons_valid):
    """Bouton qui prend le nombre de lignes et de colonne de la grille et qui change de fenêtre"""
    global ROWS, COLS, NB_JETONS_V, grid
    r, c = int(r), int(c)
    paragraphe_error = ("Un des nombres est invalide!\n"
                        "Veuillez verifier que l'une des conditions suivantes sont respecter: \n"
                        "1) Le nombre de lignes est compris entre 2 et 8 inclus \n"
                        "2) Le nombre de colonnes est compris entre 2 et 8 inclus \n"
                        "3) Le nombre de jetons à valider est inférieur au plus petit nombre entre les lignes ou les colonnes \n")
    if (1 < r < 9) and (1 < c < 9) and (int(nb_jetons_valid) <= min(r, c)):
        ROWS = int(r)
        COLS = int(c)
        NB_JETONS_V = int(nb_jetons_valid)
        grid = [[0] * COLS for _ in range(ROWS)]
        main()
    else:
        messagebox.showerror("Error", paragraphe_error)


def draw_grid():
    """Dessine la grille et les jetons déjà placés."""
    global ROWS, COLS, CELL_SIZE, RADIUS, PLAYER_COLORS, canvas, grid

    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            color = PLAYER_COLORS[grid[row][col]]
            canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill=color, outline="black")

def handle_click(event):
    """Ajoute un jeton dans la colonne sélectionnée et vérifie la victoire."""
    global canvas, canvas_tour, current_player, grid, liste_jetons, winner
    col = event.x // CELL_SIZE
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = current_player
            liste_jetons.append((row, col))
            draw_grid()
            winner = check_winner()
            if winner:
                #canvas.unbind("<Button-1>")  # Désactive les clics après la victoire
                canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
                                   text=f"Joueur {winner} a gagné !", font=("Arial", 45, "bold"), fill="black")
            else:
                current_player = 3 - current_player  
                canvas_tour.create_rectangle(25, 25, 180, 70, fill="white", outline="white")
                canvas_tour.create_text(100,CELL_SIZE//2,text="JOUEUR "+str(current_player), font=("Arial", 20, "bold"), fill="blue")
                canvas_tour.create_oval(CELL_SIZE//2, CELL_SIZE-25, 50+CELL_SIZE, 75+CELL_SIZE, fill=PLAYER_COLORS[current_player])
            return

def check_winner():
    """Vérifie si un joueur a gagné."""
    global grid, NB_JETONS_V
    
    # Vérification horizontale
    for row in range(ROWS):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]
            
     # Vérification verticale
    for row in range(ROWS - 3):
        for col in range(COLS):
            if grid[row][col] != 0 and all(grid[row + i][col] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]

    # Vérification diagonale 1
    for row in range(3, ROWS):
         for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row - i][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]
            
    # Vérification diagonale 2
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row + i][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]

    return None  # Aucun gagnant pour l'instant

def undo():
    """Fonction permmettant de revenir en arrière"""
    global grid, liste_jetons
    if liste_jetons != []:
        element = liste_jetons[len(liste_jetons)-1]
        liste_jetons.remove(element)
        row, col = element[0], element[1]
        grid[row][col] = 0
        draw_grid()

def recommencer():
    """" Effacer la grille et remmetre toutes les positions de grid à 0 pour pouvoir reccommencer la partie"""
    global grid, liste_jetons
    liste_jetons = []
    grid = [[0] * COLS for _ in range(ROWS)] 
    draw_grid()

# Sauvegarde / chargement de partie
def enregistrer_partie():
    """ Fonction qui sauvegarde la partie du joueur"""
    with open("sauvegarde.txt", "w") as fichier:
        fichier.write(f"{len(grid)}\n")
        fichier.write(f"{len(grid[0])} \n")
        for i in grid:
            for j in i:
                fichier.write(f"{j}\n")

def partie_enregistrer():
    """Fonction qui lance la Partie enregistrée par le joueur auparavant"""
    global ROWS, COLS, grid

    fichier_sauvegarde = open('sauvegarde.txt', 'r') 
    ROWS = int(fichier_sauvegarde.readline()) 
    COLS = int(fichier_sauvegarde.readline()) 
    grid = [[]for i in range(ROWS)]
    ligne = fichier_sauvegarde.readline()
    nb_col = 0
    indice_ligne = 0
    #Boucle qui enregistre les position des jetons dans la grille global grid réinitialisée
    while ligne !='':
        if nb_col < COLS:
            grid[indice_ligne].append(int(ligne))
            ligne = fichier_sauvegarde.readline()
            nb_col += 1
        else:
            nb_col = 0
            indice_ligne += 1
    
    main()
    # Fonctions d'interface utilisateur 
def fen_parties():
    """Fenêtre d'accueil permettant de changer les parametres du jeu"""
    #Fenêtre de la liste
    fenetre = tk.Toplevel()  
    fenetre.title("Puissance 4")
    fenetre.configure(bg="#fff8dc") 

    titre = tk.Label(
        fenetre, text="Puissance 4", font=("Arial", 28, "bold"),
        bg="#fff8dc", fg="#8b8000"  
    )
    sous_titre = tk.Label(
        fenetre, text="Choisissez une option", font=("Arial", 16),
        bg="#fff8dc", fg="#8b8000"
    )

    button_nouvelle_partie = tk.Button(
        fenetre, text="Nouvelle Partie", command=lambda: fen_accueil(fenetre),
        font=("Arial", 14), bg="#ffeb3b", fg="black", padx=30, pady=15
    )
    button_partie_enregistrer = tk.Button(
        fenetre, text="Reprendre Partie", command=partie_enregistrer,
        font=("Arial", 14), bg="#ffd700", fg="black", padx=30, pady=15
    )

    # Placement
    titre.pack(pady=(30, 10))
    sous_titre.pack(pady=(0, 20))
    button_nouvelle_partie.pack(pady=10)
    button_partie_enregistrer.pack(pady=10)
    
def fen_accueil(fen):
    """Fenêtre de configuration du jeu avec style jaune."""
    global grid

    clear_frame(fen)
    fenetre = tk.Frame(fen, bg="#fff8dc") 
    fenetre.pack(fill="both", expand=True)
    #fenetre.title("Configuration de la Partie")
    #fenetre.configure(bg="#fff8dc")
    
    
    titre = tk.Label(
        fenetre, text="Configurer la Partie", font=("Arial", 20, "bold"),
        bg="#fff8dc", fg="#8b8000"
    )
    titre.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # Labels
    label_lignes = tk.Label(fenetre, text="Nombre de lignes :", font=("Arial", 12),
                            bg="#fff8dc", fg="black")
    label_colonnes = tk.Label(fenetre, text="Nombre de colonnes :", font=("Arial", 12),
                              bg="#fff8dc", fg="black")
    label_jetons_valid = tk.Label(fenetre, text="Jetons pour gagner :", font=("Arial", 12),
                                  bg="#fff8dc", fg="black")

    # Champs de saisie
    entre_lignes = tk.Entry(fenetre, font=("Arial", 12))
    entre_colonnes = tk.Entry(fenetre, font=("Arial", 12))
    entre_jetons_valid = tk.Entry(fenetre, font=("Arial", 12))

    # Boutons
    button_confirmer = tk.Button(
        fenetre, text="Confirmer", font=("Arial", 12, "bold"),
        bg="#ffeb3b", fg="black",
        command=lambda: access(entre_lignes.get(), entre_colonnes.get(), entre_jetons_valid.get())
    )
    button_default = tk.Button(
        fenetre, text="Par défaut", font=("Arial", 12, "bold"),
        bg="#ffd54f", fg="black",
        command=main
    )

   
    label_lignes.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entre_lignes.grid(row=1, column=1, padx=10, pady=10)
    label_colonnes.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entre_colonnes.grid(row=2, column=1, padx=10, pady=10)
    label_jetons_valid.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entre_jetons_valid.grid(row=3, column=1, padx=10, pady=10)

    button_default.grid(row=4, column=0, pady=20)
    button_confirmer.grid(row=4, column=1, pady=20)

    return fenetre

def main():
    """ Fenêtre principale où le jeu se joue et où toutes les fonctions sont utilisée"""
    global canvas, canvas_tour, ROWS, COLS, CELL_SIZE

    fenetre = tk.Toplevel()
    fenetre.title("Jouons au puissance 4 !")
    fenetre.attributes("-fullscreen", True)

    # Obtenir les dimensions de l'écran
    SCREEN_WIDTH = fenetre.winfo_screenwidth()
    SCREEN_HEIGHT = fenetre.winfo_screenheight()

    CANVAS_WIDTH = COLS * CELL_SIZE
    CANVAS_HEIGHT =ROWS * CELL_SIZE

   
    pos_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
    pos_y = (SCREEN_HEIGHT - CANVAS_HEIGHT) // 2

    # Créer le canvas avec la bonne taille
    canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="#005BBB")
    canvas.place(x=pos_x, y=pos_y)
    canvas.bind("<Button-1>", handle_click)

    # Création d'une fenêtre qui montre le tour du joueur
    pos_x_canvas_tour = pos_x+CANVAS_WIDTH+CELL_SIZE
    pos_y_canvas_tour = pos_y+CANVAS_HEIGHT-(2*CELL_SIZE)
    canvas_tour = tk.Canvas(fenetre, width= 2*CELL_SIZE, height=2*CELL_SIZE, bg="#005BBB")
    canvas_tour.place(x=pos_x_canvas_tour, y=pos_y_canvas_tour)

    # Bouton pour revenir en arrière
    bouton_undo = tk.Button(fenetre, text="🔙", font=("Arial", 32), command=undo)
    bouton_undo.place(x=pos_x+(CANVAS_WIDTH-100), y=pos_y-85)

    # Bouton pour recommencer la partie
    button_recommencer = tk.Button(fenetre, text="⟳", font=("Arial", 32), command=recommencer)
    button_recommencer.place(x=pos_x+CANVAS_WIDTH, y=pos_y-85)

    # Bouton pour enregistrer la partie
    bouton_enregistrer = tk.Button(fenetre, text="🖫", font=("Arial", 32), command=enregistrer_partie)
    bouton_enregistrer.place(x=pos_x+(CANVAS_WIDTH+100), y=pos_y-85)

     # Création du bouton pour supprimer la fenêtre principale
    bouton_detruire = tk.Button(fenetre, text="✖", font=("Arial", 32), command=fenetre.destroy)
    bouton_detruire.place(x=pos_x+CANVAS_WIDTH+200, y=pos_y-85)

    draw_grid()  

    return fenetre
