#!/bin/bash

# Boucle infinie pour relancer la commande si elle s'arrête.
while true; do
    # Exécutez votre commande spécifique ici.
    eti-cmdline-rtlsdr -D 5 -C 9D -Q | /home/$USER/dab/eti-tools/eti2zmq -v -a -d -o "zmq+tcp://*:18081"

    # Affiche un message et attend 5 secondes avant de relancer la commande.
    echo "La commande a été interrompue. Relance dans 5 secondes..."
    sleep 5
done
