import os
import time
import logging
from pygame import mixer
import RPi.GPIO as GPIO

'''
Initialisation
'''
print("Initialisation du code")

# Variables
print("Initialisation des variables")
sonAmbiance = True
indexAudio = 0
pinBouton = 21  # Dernier GPIO disponible
GND_PIN = 39  # Dernier pin GND disponible
derniereAppui = 0  # Variable pour le délai anti-rebond
print("Variables OK")

# GPIO
print("Initialisation GPIO")
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinBouton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Initialisation GPIO OK")
except Exception as e:
    logging.exception(f"Erreur lors de la configuration GPIO : {e}")
    exit(1)

# Driver audio
print("Initialisation audio driver")
try:
    # os.environ["SDL_AUDIODRIVER"] = "dummy" # ou "alsa"
    mixer.init()
    print("Mixeur audio initialisé avec succès")
except Exception as e:
    logging.exception(f"Erreur de l'initialisation de l'audio driver : {e}")
    exit(1)

# Répertoire où mettre les fichiers audios à lire quand on appuie sur le bouton.
# Ils seront lus dans l'ordre du dossier, pour le changer, il faut les renommer avec leur position (ex : 1-'nom_du_fichier')
print("Initialisation des fichiers audio à lire")
try:
    listeFichiersAudio = [os.path.join("./Audio", fichier)
                          for fichier in os.listdir("./Audio") if fichier.endswith(".mp3")]
except FileNotFoundError:
    listeFichiersAudio = []
    logging.exception("Fichiers non trouvés")

print("Fin de l'initialisation")

'''
Code principal
'''
print("Lancement du code principal")
# Boucle infinie
while True:
    print("Détection de l'état de l'interrupteur")
    # Afficher l'état du bouton pour déboguer
    etat_bouton = GPIO.input(pinBouton)
    print(f"État du bouton : {etat_bouton}")

    # Si on appuie sur l'interrupteur, on écoute une histoire
    if etat_bouton == GPIO.HIGH:
        tempsActuel = time.time()
        if tempsActuel - derniereAppui > 0.3:  # Délai anti-rebond de 300ms
            derniereAppui = tempsActuel
            print("Lancement d'une histoire")
            if listeFichiersAudio:
                mixer.stop()
                mixer.music.load(listeFichiersAudio[indexAudio])
                mixer.music.play(0)
                indexAudio = (indexAudio + 1) % len(listeFichiersAudio)
            else:
                print("Aucun fichier audio à jouer")
    else:
        # Sinon, on attend que le bouton soit appuyé en écoutant le son d'ambiance
        if sonAmbiance and not mixer.music.get_busy():
            try:
                if not os.path.exists("./1-sonAmbiance.mp3"):
                    raise FileNotFoundError("Le fichier ./1-sonAmbiance.mp3 est introuvable.")
                mixer.music.load("./1-sonAmbiance.mp3")
                mixer.music.play(-1)
            except FileNotFoundError as e:
                logging.exception(f"Fichier de son d'ambiance non trouvé : {e}")

        time.sleep(0.5)
