import os
import tkinter as tk
from pygame import mixer


'''
Initialisation
'''
print("Initialisation du code")

#Driver audio
os.environ["SDL_AUDIODRIVER"] = "dummy" # ou "alsa"
mixer.init()

#Variables
sonAmbiance = True
indexAudio = 0

# Répertoire où mettre les fichiers audios à lire quand on appuie sur le bouton.
# Ils seront lu dans l'ordre du dossier, pour le changer, il faut les renommer avec leur position (ex:  : 1-'nom_du_fichier')
listeFichiersAudio = [os.path.join("./Audio", fichier)
                      for fichier in os.listdir("./Audio")]



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
