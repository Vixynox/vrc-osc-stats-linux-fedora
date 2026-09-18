# VRChat OSC Stats (Linux / Fedora) 🐧

A lightweight, native Python script for Linux users that sends PC hardware stats and Spotify currently playing status directly to the VRChat Chatbox via OSC.

## Features
* ⌚ Current time in 12-hour format (AM/PM)
* 🧠 CPU usage and temperature
* ⚙️ AMD GPU usage and temperature
* 💾 RAM usage tracking
* 🎧 Spotify integration via `playerctl` with smart truncation for VRChat's 144-character limit.

## Prerequisites
Tested on Fedora Linux with AMD hardware. You need the following dependencies:
```bash
pip install psutil python-osc
sudo dnf install playerctl

How to use
You can run this automatically with VRChat via Steam Launch Options using a shell script (start_with_game.sh):
~/vrc-osc-stats/start_with_game.sh %command%
