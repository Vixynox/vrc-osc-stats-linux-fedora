#!/bin/bash

/home/$USER/vrc-osc-stats/venv/bin/python /home/$USER/vrc-osc-stats/scrypt_osc.py &
OSC_PID=$!

"$@"

kill $OSC_PID
