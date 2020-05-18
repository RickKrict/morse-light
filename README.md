# morse-light

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

Dépôt du projet de générateur de code morse. Le programme s’installe sur Raspberry et permet, après l’écriture d’un mot, de l’envoyer en faisant clignoter une lumière.

## Dépendances

Pour pouvoir utiliser ce programme, il vous faut installer :
* RPi
* PyQt5 (facultatif pour cli.py, obligatoire pour gui.py)

Vous pouvez les installer sur le Raspberry avec cette commande : 

```
pip3 install RPi.GPIO
sudo apt install python3-pyqt5
```

## Installation

### Avec une LED

Vous pouvez faire ce montage avec LED pour tester le programme. Voici un schéma expliquant comment faire le montage.

![image montage led](https://raspberry-pi.fr/wp-content/uploads/2019/05/raspberry-pi-led-939x528.png)
*[Source](https://raspberry-pi.fr/led-raspberry-pi/)*

Vous pouvez modifier le montage à votre guise, n’oubliez pas de configurer le port GPIO cependant.

### Avec un relai

L’utilisation d’un relai permettra d’envoyer les messages avec des lampes plus puissantes. Voici le schéma pour le branchement du relai. Vous pouvez aussi modifier le port GPIO tant que vous le configurer correctement.

![image montage relai](https://blog.bandinelli.net/public/.Rpi_et_relai_m.png)
*[Source](https://blog.bandinelli.net/index.php?post/2015/07/18/Raspberry-Pi%2C-un-relai%2C-quelques-branchements-%3A-interrupteur-intelligent)*

## Utilisation

Une fois le repo cloné, vous devez garder tous les fichiers au même niveau. 

* morse.py : classe permettant de traduire et transmettre le morse.
* cli.py : script pour utiliser la classe dans un terminal
* gui.py : script pour lancer l’interface graphique

Les dossiers contiennent des éléments indispensables pour l’interface graphique (controllers, les vues…). Ils doivent se trouver au même niveau que les fichiers morse.py et gui.py.

**Vous ne pouvez que lancer les scripts sur un Raspbery. Dans le cas contraire, une erreur sera communiquée dès le lancement.**

### cli.py

#### Explication

Lorsque vous lancez le script, il vous sera demandé d’entrez un mot ou une phrase. Vous pouvez sortir du programme en tapant `:q`.

Vous pouvez configurer le port GPIO avec le paramètre `--gpio port` et préciser la durée d’un point en seconde avec `--point point`. Le port par défaut est le 7 et le temps d’un point est de 0,1 seconde.

Vous pouvez aussi juste passer un message sans rentrer dans la boucle avec le paramètre `-m`. Il est possible d’entrer des phrases si on la met entre guillemets.

#### --help

```
usage: cli.py [-h] [-m MESSAGE] [--point POINT] [--gpio GPIO] [-v]

Permet d’entrer des phrases ou des mots qui seront traduient en morse grace à
la classe traducteurMorse. Cette traduction sera ensuite convertie en flash
lumineux.

optional arguments:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        Permet de juste passer un message à traduire.
  --point POINT         Définit la durée en seconde d’un point.
  --gpio GPIO           Définit le port GPIO du relai ou de la LED.
  -v, --verbose         Affiche de manière détaillée le processus.
```

### gui.py

Vous pouvez lancer l’interface graphique avec le fichier `gui.py`. L’interface est constitué de 3 boutons : 

* Envoyer : pour envoyer le message en morse
* Effacer : permet d’effacer la zone de saisi
* Configuration : permet de configurer le port GPIO et le temps d’un point
* Quitter : pour quitter le programme

La barre en bas est utilisée pour afficher les logs de la classe morse.py. Elle est activable via le menu de configuration. 

## Raizo sociaux

* Matrix : [#morsi:gnous.eu](https://matrix.to/#/!gqYSEaWPviXAEsIHYk:gnous.eu?via=gnous.eu)
* [Mastodon](https://toot.gnous.eu/web/accounts/1693)

## Sources dépendances

* [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
* [PyQt5](https://pypi.org/project/PyQt5/)


[![GPLv3 license](https://www.gnu.org/graphics/gplv3-or-later.png)](http://perso.crans.org/besson/LICENSE.html)
