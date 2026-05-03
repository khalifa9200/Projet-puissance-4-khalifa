import tkinter as tk
from main import fen_parties
from set_et_match import fen_parties_set_et_match
from robot import fenetre_robot

fen = tk.Tk()
fen.title("Puissance 4")


button_style = {
    "font": ("Arial", 14),
    "width": 20,
    "height": 2,
    "bd": 5,
    "relief": "raised",
    "activebackground": "#32CD32",  
    "bg": "#FFD700",  
    "fg": "black"
}

label_haut  = tk.Label(fen, text="Mode de jeu")
button_1vs1 = tk.Button(fen, text="1 VS 1", **button_style, command= fen_parties)
button_1vsRobot = tk.Button(fen, text="1 VS ROBOT", **button_style, command=fenetre_robot)
button_Set_et_Match = tk.Button(fen, text="Set et Match", **button_style, command=lambda: fen_parties_set_et_match(fen))

label_haut.pack(padx=10, pady=10)
button_1vs1.pack(padx=10, pady=10)
button_1vsRobot.pack(padx=10, pady=10)
button_Set_et_Match.pack(padx=10, pady=10)

fen.mainloop()


# Sources
#https://www.unicode.org/emoji/charts/full-emoji-list.html
#https://htmlcolorcodes.com/fr/
