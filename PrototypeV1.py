import os
import time
import tkinter as tk
from pygame import mixer

import RPi.GPIO as GPIO


mixer.init()
sonAmbiance = True
listeFichiersAudio = [os.path.join("./Audio", fichier)
                      for fichier in os.listdir("./Audio")]
indexAudio = 0
pinBouton = 18


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


'''
Pratique pour les tests mais inutile si aucun affichage n'est présent
'''
# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Ronde des Crèches")
fenetre.geometry("400x200")

# Ajouter un bouton
button = tk.Button(fenetre, text="Lancer le dialogue", command=ecouterHistoire)
button.pack(pady=20)

# Charger le son d'ambiance
mixer.music.load("./1-sonAmbiance.mp3")
mixer.music.play(-1, fade_ms=2000)

checkEvent()
fenetre.mainloop()


'''
Connexion au Raspberry Pi 4b
'''
def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinBouton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    try:
        while True:
            if GPIO.input(pinBouton) == GPIO.HIGH:
                ecouterHistoire()
            else:
                mixer.music.load("./1-sonAmbiance.mp3")
                mixer.music.play(-1, fade_ms=2000)
                checkEvent()

    except KeyboardInterrupt:
        print("Interruption clavier")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
