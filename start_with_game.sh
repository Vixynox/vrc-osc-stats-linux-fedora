#!/bin/bash

# Uruchamia skrypt OSC w tle (korzystając z Twojego wirtualnego środowiska)
/home/$USER/vrc-osc-stats/venv/bin/python /home/$USER/vrc-osc-stats/skrypt_osc.py &
OSC_PID=$!

# Uruchamia VRChat (Steam podstawi tu komendę startową)
"$@"

# Po wyłączeniu gry, zabija skrypt OSC działający w tle
kill $OSC_PID
