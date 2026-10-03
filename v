[Unit]
Description=VRChat OSC Stats Monitor
After=network.target

[Service]
Type=simple
# Assuming the file is located in ~/vrc-osc-stats/
ExecStart=/usr/bin/python3 %h/vrc-osc-stats/skrypt_osc.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
