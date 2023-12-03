#!/bin/bash

# Création du répertoire dab si nécessaire
if [ ! -d "dab" ]; then
    mkdir dab
fi

# Installation de eti-cmdline
cd dab
git clone https://github.com/DABodr/eti-stuff.git
cd eti-stuff/eti-cmdline
mkdir build
cd build
cmake -DRTLSDR=ON  # Pour DABSticks
make
sudo make install

# Retour au répertoire dab
cd ../../..

# Installation de eti-tool
git clone https://github.com/DABodr/eti-tools.git
cd eti-tools/
make
sudo make install
sudo ldconfig

# Retour au répertoire de départ
cd ..

echo "Installation terminée."
