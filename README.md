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
