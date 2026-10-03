# VRChat OSC Hardware & Media Telemetry (Linux Edition) 🐧

A highly optimized, zero-configuration Python telemetry service designed specifically for Linux environments. This script seamlessly integrates with VRChat via the OSC (Open Sound Control) protocol to broadcast real-time system diagnostics and media playback status directly to your in-game Chatbox.

## ✨ Features (Zero-Config)
* 🐧 **Auto-Detection:** Dynamically reads your exact OS Name, CPU Model, and GPU Model natively from the system. No manual configuration required.
* ⚙️ **Universal GPU Support:** Monitors utilization natively from AMD (via `sysfs`) or NVIDIA (via `nvidia-smi`).
* ⌚ **Time & Uptime:** Displays the current 12-hour time and your Linux system uptime (⏳).
* 🧠 **Hardware Diagnostics:** Real-time tracking of CPU/GPU utilization, thermal metrics, and RAM (💾) allocation.
* 🎧 **Spotify Integration:** Hooks into `playerctl` to display current tracks, featuring dynamic text truncation to perfectly comply with VRChat's 144-character OSC limit.

## 📦 Prerequisites
Tested on Fedora Linux. Ensure you have the required dependencies installed:

```bash
pip install psutil python-osc
sudo dnf install playerctl


🚀 Installation & Usage
⚠️ Important: VRChat & Steam Configuration
Before the script can display stats on your avatar, you must allow VRChat to receive local network data:

Restart Steam completely (this ensures no background processes are blocking the 9000 network port).

Launch VRChat.

Open your in-game Action Menu (Radial Menu).

Navigate to Options ➔ OSC ➔ and set it to Enabled.

Option A: Steam Launch Options (Auto-start with VRChat)
You can trigger the script automatically when launching VRChat through Steam by modifying the game's launch options. Add this line:

Bash
~/vrc-osc-stats/start_with_game.sh %command%
Option B: Native System Service (systemd)
For a fully seamless background experience without keeping terminal windows open, run the telemetry as a native Linux user service.

Create the systemd user directory and copy the service file:

Bash
mkdir -p ~/.config/systemd/user/
cp ~/vrc-osc-stats/vrc-osc.service ~/.config/systemd/user/
Reload the systemd manager configuration:

Bash
systemctl --user daemon-reload
Start the telemetry service:

Bash
systemctl --user start vrc-osc.service
(Optional) Enable the service to start automatically upon system login:

Bash
systemctl --user enable vrc-osc.service
🛑 Stopping the Service
If you need to stop the background service, simply run:

Bash
systemctl --user stop vrc-osc.service

3. Click the green **Commit changes...** button.
4. To sync this final fix back to your local Fedora PC, run this in your terminal:

```bash
cd ~/vrc-osc-stats
git pull
