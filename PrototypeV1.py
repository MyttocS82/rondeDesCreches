import os
import tkinter as tk
from pygame import mixer

'''
// Connexion aux ports du Raspberry Pi 4
import RPi.GPIO as GPIO

bouton = ???
GPIO.setup(bouton.GPIO.IN)

while True:
    if GPIO.input(bouton) == 1:
        ecouterHistoire
    else:
        mixer.music.load("./1-sonAmbiance.mp3")
        mixer.music.play(-1, fade_ms=2000)
        checkEvent()
'''


mixer.init()
sonAmbiance = True
listeFichiersAudio = [os.path.join("./Audio", fichier)
                      for fichier in os.listdir("./Audio")]
indexAudio = 0


def ecouterHistoire():
    global indexAudio
    mixer.stop()

    mixer.music.load(listeFichiersAudio[indexAudio])
    mixer.music.play(0)
    indexAudio = (indexAudio + 1) % len(listeFichiersAudio)


def checkEvent():
    if not mixer.music.get_busy():
        mixer.music.load("./1-sonAmbiance.mp3")
        mixer.music.play(-1)
    fenetre.after(500, checkEvent)


def clickBouton():
    ecouterHistoire()

'''
Pratique pour les tests mais inutile si aucun affichage n'est présent
'''
# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Ronde des Crèches")
fenetre.geometry("400x200")

# Ajouter un bouton
button = tk.Button(fenetre, text="Lancer le dialogue", command=clickBouton)
button.pack(pady=20)

# Charger le son d'ambiance
mixer.music.load("./1-sonAmbiance.mp3")
mixer.music.play(-1, fade_ms=2000)

checkEvent()
fenetre.mainloop()
