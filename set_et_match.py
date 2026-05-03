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

#Parametres Set et match
winner = None
nb_parties = 0
nb_parties_reserve = 0
VictoireRouge = 0
VictoireJaune = 0
VictoireRougeText = None
VictoireJauneText = None
Text_nb_parties = None

# Fonctions de logique de jeu
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def access(r, c, nb_jetons_valid, nb_parties):
    """Bouton qui prend le nombre de lignes et de colonne de la grille et qui change de fenêtre"""
    global ROWS, COLS, NB_JETONS_V, grid
    r, c = int(r), int(c)
    paragraphe_error = ("Un des nombres est invalide!\n"
                        "Veuillez verifier que l'une des conditions suivantes sont respecter: \n"
                        "1) Le nombre de lignes est compris entre 2 et 8 inclus \n"
                        "2) Le nombre de colonnes est compris entre 2 et 8 inclus \n"
                        "3) Le nombre de jetons à valider est inférieur au plus petit nombre entre les lignes ou les colonnes \n")
    if (1 < r < 9) and (1 < c < 9) and (int(nb_jetons_valid) <= min(r, c)):
        ROWS = r
        COLS = c
        NB_JETONS_V = int(nb_jetons_valid)
        grid = [[0] * COLS for _ in range(ROWS)]
        set_et_match(nb_parties)
    else:
        messagebox.showerror("Error", paragraphe_error)

def draw_grid():
    """Dessine la grille et les jetons déjà placés."""
    global ROWS, COLS, CELL_SIZE, RADIUS, PLAYER_COLORS, canvas

    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            color = PLAYER_COLORS[grid[row][col]]
            canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill=color, outline="black")

def check_winner():
    """Vérifie si un joueur a gagné."""
    global grid, NB_JETONS_V
    
    for row in range(ROWS):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]
            
    
    for row in range(ROWS - 3):
        for col in range(COLS):
            if grid[row][col] != 0 and all(grid[row + i][col] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]

    
    for row in range(3, ROWS):
         for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row - i][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]
            
    
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
                current_player = 3 - current_player  # Alterne entre 1 et 2
                canvas_tour.create_rectangle(25, 25, 180, 70, fill="white", outline="white")
                canvas_tour.create_text(100,CELL_SIZE//2,text="JOUEUR "+str(current_player), font=("Arial", 20, "bold"), fill="blue")
                canvas_tour.create_oval(CELL_SIZE//2, CELL_SIZE-25, 50+CELL_SIZE, 75+CELL_SIZE, fill=PLAYER_COLORS[current_player])
            return

# Boutons du jeu
def continuer(): 
    global grid, winner, nb_parties, VictoireRouge, VictoireJaune, VictoireRougeText, VictoireJauneText, Text_nb_parties

    if winner == 1:
        VictoireRouge += 1
        VictoireRougeText.config(text=f"Victoires du joueur Rouge: {VictoireRouge}")
    elif winner == 2:
        VictoireJaune += 1
        VictoireJauneText.config(text=f"Victoires du joueur Jaune: {VictoireJaune}")
    
    nb_parties -= 1
    Text_nb_parties.config(text=f"Nombre de parties restantes: {nb_parties}")
    if nb_parties != 0:
        grid = [[0] * COLS for _ in range(ROWS)]
        winner = None
        draw_grid()
    else:
        canvas.delete(all)
        draw_grid()
        if VictoireRouge > VictoireJaune:
            canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
                                   text=f"Joueur 1 a gagné avec\n   {VictoireRouge} points contre {VictoireJaune}!", font=("Arial", 30, "bold"), fill="black")
        elif VictoireJaune > VictoireRouge:
            canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
                                   text=f"Joueur 2 a gagné avec\n   {VictoireJaune} points contre {VictoireRouge}!", font=("Arial", 30, "bold"), fill="black")
        else:
            grid = [[0] * COLS for _ in range(ROWS)]
            winner = None
            draw_grid()
            nb_parties += 1

def recommencer():
    global grid, current_player, nb_parties, nb_parties_reserve, winner, VictoireRouge, VictoireJaune, VictoireRougeText, VictoireJauneText, Text_nb_parties

    grid = [[0] * COLS for _ in range(ROWS)]
    current_player = 1  # j1 commence
    nb_parties = nb_parties_reserve

    winner = None
    VictoireRouge = 0
    VictoireJaune = 0
    VictoireRougeText.config(text=f"Victoires du joueur Rouge: {VictoireRouge}")
    VictoireJauneText.config(text=f"Victoires du joueur Jaune: {VictoireJaune}")
    Text_nb_parties.config(text=f"Nombre de parties restantes: {nb_parties}")
    draw_grid()

# Fonctions d'interface utilisateur 
def fen_parties_set_et_match(fen):
    """Fenêtre de configuration stylisée pour Set et Match."""
    fenetre = tk.Toplevel()
    fenetre.title("Mode Set et Match")
    fenetre.configure(bg="#fff8dc")  # Fond crème

   
    titre = tk.Label(fenetre, text="Configurer le Set et Match", font=("Arial", 20, "bold"),
                     bg="#fff8dc", fg="#8b8000")
    titre.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # Champs de configuration
    champs = [
        ("Nombre de lignes :", 1),
        ("Nombre de colonnes :", 2),
        ("Jetons pour gagner :", 3),
        ("Nombre de parties :", 4)
    ]

    entries = {}

    for text, row in champs:
        label = tk.Label(fenetre, text=text, font=("Arial", 12), bg="#fff8dc", fg="black")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(fenetre, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=10, pady=5)
        entries[text] = entry

    # Boutons
    confirmer = tk.Button(
        fenetre, text="Confirmer", font=("Arial", 12, "bold"),
        bg="#FFD700", fg="black",
        command=lambda: access(entries["Nombre de lignes :"].get(),
                               entries["Nombre de colonnes :"].get(),
                               entries["Jetons pour gagner :"].get(),
                               entries["Nombre de parties :"].get())
    )
    confirmer.grid(row=5, column=1, pady=20)

    annuler = tk.Button(
        fenetre, text="Annuler", font=("Arial", 12, "bold"),
        bg="#e0e0e0", fg="black", command=fenetre.destroy
    )
    annuler.grid(row=5, column=0, pady=20)

def set_et_match(nb_parties_choisis):
    global canvas,canvas_tour, ROWS, COLS, CELL_SIZE, nb_parties, nb_parties_reserve, VictoireRougeText, VictoireJauneText, Text_nb_parties

    nb_parties = int(nb_parties_choisis)
    nb_parties_reserve = int(nb_parties_choisis)
    fenetre = tk.Toplevel()
    fenetre.title("Jouons au puissance 4 !")
    fenetre.attributes("-fullscreen", True)

    # Obtenir les dimensions de l'écran
    SCREEN_WIDTH = fenetre.winfo_screenwidth()
    SCREEN_HEIGHT = fenetre.winfo_screenheight()

    CANVAS_WIDTH = COLS * CELL_SIZE
    CANVAS_HEIGHT =ROWS * CELL_SIZE

    # Position de la grille dans la fenetre
    pos_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
    pos_y = (SCREEN_HEIGHT - CANVAS_HEIGHT) // 2

    VictoireRougeText = tk.Label(fenetre, text=f"Victoires du joueur Rouge: {VictoireRouge}", font=("Arial", 15))
    VictoireJauneText = tk.Label(fenetre, text=f"Victoires du joueur Jaune: {VictoireJaune}", font=("Arial", 15))
    VictoireRougeText.place(x=pos_x-400, y=pos_y+200)
    VictoireJauneText.place(x=pos_x+CANVAS_WIDTH+100, y=pos_y+400)
    
    # Créer le canvas avec la bonne taille
    canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
    canvas.place(x=pos_x, y=pos_y)
    canvas.bind("<Button-1>", handle_click)

    # Création d'une fenêtre qui montre le tour du joueur
    pos_x_canvas_tour = pos_x+CANVAS_WIDTH+CELL_SIZE
    pos_y_canvas_tour = pos_y+CANVAS_HEIGHT-(2*CELL_SIZE)
    canvas_tour = tk.Canvas(fenetre, width= 2*CELL_SIZE, height=2*CELL_SIZE, bg="blue")
    canvas_tour.place(x=pos_x_canvas_tour, y=pos_y_canvas_tour)

    # Texte indiquant le nombre de parties restantes
    Text_nb_parties = tk.Label(fenetre, text=f"Nombre de parties restantes: {nb_parties}", font=("Arial", 30))
    Text_nb_parties.place(x=pos_x+100, y=pos_y+CANVAS_HEIGHT+50)

   
    bouton_undo = tk.Button(fenetre, text="🔙", font=("Arial", 32), command=undo)
    bouton_undo.place(x=pos_x+(CANVAS_WIDTH-100), y=pos_y-85)

    
    button_continuer = tk.Button(fenetre, text="➡️", font=("Arial", 32), command=continuer)
    button_continuer.place(x=pos_x+(CANVAS_WIDTH), y=pos_y-85)

    
    button_recommencer = tk.Button(fenetre, text="⟳", font=("Arial", 32), command=recommencer)
    button_recommencer.place(x=pos_x+CANVAS_WIDTH+100, y=pos_y-85)


    bouton_detruire = tk.Button(fenetre, text="✖", font=("Arial", 32), command=fenetre.destroy)
    bouton_detruire.place(x=pos_x+CANVAS_WIDTH+300, y=pos_y-85)

    draw_grid()  

    return fenetre

