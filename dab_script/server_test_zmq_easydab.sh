#!/bin/bash

/home/$USER/dab/mmbtools-aux/zmqtest/zmq-sub/zmq-sub core.mpb.li 9100 | /home/$USER/dab/eti-tools/eti2zmq -a -l -d -o "zmq+tcp://*:18081"





