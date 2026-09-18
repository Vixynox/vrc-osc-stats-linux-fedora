import time
import psutil
import os
import subprocess
from datetime import datetime
from pythonosc import udp_client

IP = "127.0.0.1"
PORT = 9000
client = udp_client.SimpleUDPClient(IP, PORT)

OS_NAME = "YOUR OS"
CPU_NAME = "YOUR CPU"
GPU_NAME = "YOUR GPU"

def get_amd_gpu_usage():
    try:
        for card in ['card0', 'card1']:
            path = f"/sys/class/drm/{card}/device/gpu_busy_percent"
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return f.read().strip()
        return "N/A"
    except:
        return "N/A"

def get_temps():
    cpu_t, gpu_t = "", ""
    try:
        temps = psutil.sensors_temperatures()
        if 'k10temp' in temps:
            cpu_t = f"{int(temps['k10temp'][0].current)}°C"
        if 'amdgpu' in temps:
            gpu_t = f"{int(temps['amdgpu'][0].current)}°C"
    except:
        pass
    return cpu_t, gpu_t

def get_spotify():
    try:
        out = subprocess.check_output(
            ["playerctl", "metadata", "--format", "{{ artist }} - {{ title }}"],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return out if out else ""
    except:
        return ""

print("Sending stats to VRChat Chatbox... (Press Ctrl+C to stop)")

while True:
    cpu_usage = psutil.cpu_percent()
    gpu_usage = get_amd_gpu_usage()
    
    ram = psutil.virtual_memory()
    ram_used = round(ram.used / (1024**3), 1)
    ram_total = round(ram.total / (1024**3), 1)

    cpu_temp, gpu_temp = get_temps()
    song = get_spotify()
    
    current_time = datetime.now().strftime("%I:%M %p")

    banner = f"{current_time} | 💻 {OS_NAME}"
    line2 = f"🧠 {CPU_NAME}: {cpu_usage}% {cpu_temp} | ⚙️ {GPU_NAME}: {gpu_usage}% {gpu_temp}"
    line3 = f"💾 RAM: {ram_used}/{ram_total} GB"
    
    msg = f"{banner}\n{line2}\n{line3}"
    
    if song:
        prefix = "\n🎧 Listening to:\n🎵 "
        
        chars_left = 144 - len(msg) - len(prefix)
        
        if chars_left > 5 and len(song) > chars_left:
            song = song[:chars_left-3] + "..."
            
        msg += f"{prefix}{song}"

    client.send_message("/chatbox/input", [msg, True, False])
    
    time.sleep(2)
