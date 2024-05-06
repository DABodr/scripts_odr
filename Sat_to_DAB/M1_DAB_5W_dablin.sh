#!/bin/bash


dvbstream -f 11461000 -s 5780 8192 -p H -o | /home/$USER/dab/eti-tools/ts2na -s 12  -p 301 | /home/$USER/dab/eti-tools/na2ni | /home/$USER/dab/dablin/build/src/dablin_gtk
