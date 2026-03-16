import tkinter as tk
import main

def ouvrir_fenetre():
    main.fen_accueil()

fen = tk.Tk()
fen.title("Puissance 4")

label_haut  = tk.Label(fen, text="Mode de jeu")
button_1vs1 = tk.Button(fen, text="1 VS 1", command=ouvrir_fenetre)
button_1vsRobot = tk.Button(fen, text="1 VS ROBOT", command=ouvrir_fenetre)

label_haut.pack(padx=10, pady=10)
button_1vs1.pack(padx=10, pady=10)
button_1vsRobot.pack(padx=10, pady=10)


fen.mainloop()
