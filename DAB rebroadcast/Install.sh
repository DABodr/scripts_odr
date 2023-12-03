#!/bin/bash

# Récupère le répertoire personnel de l'utilisateur courant
USER_HOME="$HOME"

# Chemin du répertoire dab
DAB_DIR="$USER_HOME/dab"

# Création du répertoire dab si nécessaire
if [ ! -d "$DAB_DIR" ]; then
    mkdir "$DAB_DIR"
fi

# Installation de eti-cmdline
cd "$DAB_DIR"
git clone https://github.com/DABodr/eti-stuff.git
cd eti-stuff/
mkdir build
cd build
cmake -DRTLSDR=ON  # Pour DABSticks
make
sudo make install

# Retour au répertoire dab
cd "$DAB_DIR"

# Installation de eti-tool
git clone https://github.com/DABodr/eti-tools.git
cd eti-tools/
make
sudo make install
sudo ldconfig

# Retour au répertoire de départ
cd "$USER_HOME"

echo "Installation terminée."

# Attendre une entrée de l'utilisateur avant de fermer le script
read -p "Appuyez sur n'importe quelle touche pour fermer le script..." -n1 -s
echo
