# Ronde des Crèches

Ce projet permet de lire des fichiers audio de manière séquentielle, avec un son d'ambiance lorsqu'aucune histoire n'est jouée. Deux versions du code sont fournies, adaptées aux environnements **Windows** (avec interface graphique) et **Linux** (avec gestion GPIO pour Raspberry Pi).

---

## Fonctionnalités

- **Lecture d'histoires audio :** Les fichiers audio sont lus dans l'ordre défini par leurs noms dans le dossier `./Audio`.  
- **Son d'ambiance :** Un son de fond est joué en boucle lorsqu'aucune histoire n'est en cours.  
- **Gestion de bouton (Linux/Raspberry Pi) :** Sur Linux, un interrupteur connecté à une broche GPIO déclenche la lecture des histoires.  
- **Interface graphique (Windows) :** Une interface Tkinter avec un bouton pour lancer les histoires.  

---

## Pré-requis

### Windows
- **Python 3.11 ou supérieur**
- Bibliothèque Python :
  - `pygame`
  - `tkinter`

### Linux (Raspberry Pi)
- **Python 3.11 ou supérieur**
- Bibliothèque Python :
  - `pygame`
  - `RPi.GPIO`
- **Matériel :**
  - Raspberry Pi (testé sur Raspberry Pi 4B).
  - Un interrupteur connecté à la broche GPIO 18.

---

## Installation

1. **Cloner le projet :**
   ```bash
   git clone <URL_DU_PROJET>
   cd <NOM_DU_REPERTOIRE>

2. **Installer les dépendances :**
   ```bash
   pip install pygame RPi.GPIO  # RPi.GPIO est uniquement requis sur Linux

3. ** Préparer le dossier Audio :**
    - Placer vos fichier audio dans le dossier ./Audio
    - Renommez les fichiers pour les lire dans l'ordre souhaité (ex: 1-nom_du_fichier.mp3, 2-nom_du_fichier.mp3,...)
    - Placer également le fichier audio du son d'ambiance dans le répertoire principal (default : 1-sonAmbiance.mp3)

---

## Utilisation

### Version Windows : ReleaseWindows.py
1. Lancer le script :
   ```bash
   python ReleaseWindows.py
   
2. Une fenêtre s'ouvre avec un bouton intitulé "Lancer le dialogue" :
    - Cliquez sur le bouton pour jouer une histoire
    - Le son d'ambiance reprendra une fois l'histoire terminée jusqu'à la prochaine

### Version Linux (Raspberry Pi) : ReleaseLinux.py
1. Câblage de l'interrupteur :
    - Connectez l'interrupteur à la Raspberry Pi :
      - Une borne à la broche GPIO 18
      - L'autre borne au GND
    - Utilisation de la résistance interne "pull down" configurée par défault dans le code

2. Lancer le script :
   ```bash
   python ReleaseLinux.py
   
3. Une fenêtre s'ouvre avec un bouton intitulé `Lancer le dialogue` :
    - Le son d'ambiance se jouera au démarrage de la Raspberry Pi, plus qu'à appuyer sur l'interrupteur pour lancer une histoire
   
---

## Dépannage
### Erreur ALSA sur Raspberry Pi :
Si vous obtenez cette erreur :
```bash 
pygame.error: "ALSA Couldn't open audio device"
```
Assurez-vous qu'un périphérique audio (haut-parleur, casque) est connecté et configurez correctement la sortie audio :
Sinon, essayez de changer la variable : `os.environ["SDL_AUDIODRIVER"]`.

### Erreur son sur Windows :
Vérifiez que :
- Les pilotes audio sont installés.
- Vos fichiers audio sont lisibles et correctement encodés (format `.mp3` ou autre supporté par pygame).

---

## Auteur
- **Nom :** [Michelon Scott](https://github.com/MyttocS82)
- **Contact :** [Email](scottmichelon@gmail.com)
- **Description :** Ce projet a été conçu pour un événement interactif, avec des versions adaptées pour Windows et Linux.
