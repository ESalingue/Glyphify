# img2ascii

`img2ascii` est un outil en ligne de commande écrit en **Python** permettant de convertir une image
(PNG, JPG, etc.) en **ASCII art**, avec prise en compte **pixel par pixel** de la luminosité et
(optionnellement) de la **couleur** via ANSI TrueColor (24-bit).

L’objectif est d’obtenir un rendu **100 % ASCII**, proche de l’esthétique *neofetch-like*,
mais totalement personnalisable.

---

## ✨ Fonctionnalités

- Conversion image → ASCII caractère par caractère
- Support des images **PNG / JPG / JPEG**
- Rendu :
  - ASCII **en couleur** (ANSI TrueColor)
  - ASCII **sans couleur** (grayscale)
- Ajustements avancés :
  - luminosité
  - contraste
  - gamma (récupération des fonds sombres)
  - ratio hauteur/largeur des caractères
- Palette ASCII personnalisable
- Compatible Linux (Ubuntu, Debian, Arch…)

---

## 📸 Exemples

ASCII couleur :
```bash
./img2ascii.py image.png -w 90

## 📦 Installation

## 1️⃣ Dépendances système

sudo apt update
sudo apt install python3 python3-pip

## 2️⃣ Dépendances Python

pip3 install -r requirements.txt

## 🚀 Utilisation

./img2ascii.py <image> [options]

## Options principales

| Option          | Description                                    |
| --------------- | ---------------------------------------------- |
| `-w, --width`   | Largeur de sortie en caractères                |
| `--no-color`    | Désactive la couleur (ASCII pur)               |
| `--brightness`  | Ajuste la luminosité                           |
| `--contrast`    | Ajuste le contraste                            |
| `--gamma`       | Ajuste la gamma (utile pour les fonds sombres) |
| `--aspect`      | Correction du ratio des caractères             |
| `--ramp`        | Palette ASCII prédéfinie                       |
| `--custom-ramp` | Palette ASCII personnalisée                    |

## 🖥️ Intégration type neofetch

paste \
  <(./img2ascii.py image.png -w 45) \
  <(fastfetch) | sed 's/\t/  /g'


