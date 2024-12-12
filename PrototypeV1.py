import os
import time
import tkinter as tk
from pygame import mixer

import RPi.GPIO as GPIO

'''
Initialisation
'''
print("Initialisation du code")

#Driver audio
#os.environ["SDL_AUDIODRIVER"] = "dummy" # ou "alsa"
mixer.init()

#Variables
sonAmbiance = True
indexAudio = 0
pinBouton = 16

# Répertoire où mettre les fichiers audios à lire quand on appuie sur le bouton.
# Ils seront lu dans l'ordre du dossier, pour le changer, il faut les renommer avec leur position (ex:  : 1-'nom_du_fichier')
listeFichiersAudio = [os.path.join("./Audio", fichier)
                      for fichier in os.listdir("./Audio")]

# Définition du mode et du bouton GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinBouton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def ecouterHistoire():
    global indexAudio
    mixer.stop()

    # Lecture de l'histoire numéro 'indexAudio'
    mixer.music.load(listeFichiersAudio[indexAudio])
    mixer.music.play(0)
    indexAudio = (indexAudio + 1) % len(listeFichiersAudio)


def checkEvent():
    if not mixer.music.get_busy():
        # Son de fond à mettre dans le répertoire principal (à renommer en cas de besoin)
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
    try:
        print("Lancement du code principal")
        # Boucle infinie
        while True:
            print("Détection de l'état de l'interrupteur")
            # Si on appuie sur l'interrupteur, on écoute une histoire
            if GPIO.input(pinBouton) == GPIO.HIGH:
                print("Lancement d'une histoire")
                ecouterHistoire()
            else:
                # Sinon on attend que le bouton soit appuyé en écoutant le son d'ambiance
                checkEvent()
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("Interruption clavier")

    finally:
        GPIO.cleanup()


# Lancement de la boucle principale à l'exécution du code
if __name__ == "__main__":
    main()
