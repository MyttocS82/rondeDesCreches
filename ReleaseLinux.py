import os
import time
import logging
import RPi.GPIO as GPIO
from pygame import mixer

'''
Initialisation
'''
print("Initialisation du code")

# Driver audio
print("Initialisation audio driver")
try:
    # os.environ["SDL_AUDIODRIVER"] = "dummy" # ou "alsa"
    mixer.init()
    print("Mixeur audio initialisé avec succès")
except Exception as e:
    logging.exception(f"Erreur de l'initialisation de l'audio driver : {e}")
    exit(1)

# Variables
print("Initialisation des variables")
sonAmbiance = True
indexAudio = 0
pinBouton = 21  # Dernier GPIO disponible
print("Variables OK")

# GPIO
print("Initialisation GPIO")
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinBouton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("Initialisation GPIO OK")
except Exception as e:
    logging.exception(f"Erreur lors de la configuration GPIO : {e}")
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


def ecouterHistoire():
    global indexAudio
    mixer.stop()

    # Lecture de l'histoire numéro 'indexAudio'
    mixer.music.load(listeFichiersAudio[indexAudio])
    mixer.music.play(0)
    indexAudio = (indexAudio + 1) % len(listeFichiersAudio)


def checkEvent():
    if sonAmbiance and not mixer.music.get_busy():
        try:
            mixer.music.load("./1-sonAmbiance.mp3")
            mixer.music.play(-1)
        except FileNotFoundError as FNFE:
            logging.exception(f"Fichier de son d'ambiance non trouvé : {FNFE}")


def attendrePressionBouton():
    print("En attente d'une pression sur le bouton pour démarrer...")
    dernierePression = 0
    while GPIO.input(pinBouton) == GPIO.HIGH:
        tempsActuel = time.time()
        if tempsActuel - dernierePression > 1:
            dernierePression = tempsActuel
        time.sleep(0.1)
    print("Bouton pressé, démarrage du programme principal...")


'''
Connexion au Raspberry Pi 4b
'''
def main():
    dernierAppui = 0
    try:
        print("Lancement du code principal")
        # Boucle infinie
        while True:
            print("Détection de l'état de l'interrupteur")
            print(f"État du bouton : {GPIO.input(pinBouton)}")
            # Si on appuie sur l'interrupteur, on écoute une histoire
            if GPIO.input(pinBouton) == GPIO.LOW:
                tempsActuel = time.time()
                if tempsActuel - dernierAppui > 0.3:  # Délai anti-rebond de 300ms
                    dernierAppui = tempsActuel
                    print("Lancement d'une histoire")
                    if listeFichiersAudio:
                        ecouterHistoire()
                    else:
                        print("Aucun fichier audio à jouer")
            else:
                # Sinon, on attend que le bouton soit appuyé en écoutant le son d'ambiance
                checkEvent()
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("Interruption clavier")

    finally:
        GPIO.cleanup()


# Lancement de la boucle principale à l'exécution du code
if __name__ == "__main__":
    attendrePressionBouton()
    main()
