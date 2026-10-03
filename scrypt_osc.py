import time
import psutil
import os
import subprocess
from datetime import datetime
from pythonosc import udp_client

IP = "127.0.0.1"
PORT = 9000
client = udp_client.SimpleUDPClient(IP, PORT)

def get_os_name():
    try:
        with open('/etc/os-release') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    return line.split('=')[1].strip().strip('"').replace("Linux ", "")[:12]
    except:
        return "Linux"

def get_cpu_name():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    name = line.split(':')[1].strip()
                    name = name.replace("AMD ", "").replace(" 6-Core Processor", "")
                    return name[:15]
    except:
        return "CPU"

def get_gpu_name():
    # Priority 1: NVIDIA
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if out: return out.replace("NVIDIA GeForce ", "")[:15]
    except: pass
    
    # Priority 2: AMD
    try:
        out = subprocess.check_output("lspci | grep -i vga", shell=True, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if "Radeon" in out or "AMD" in out:
            if "RX 6600" in out: return "RX 6600 XT"
            return "AMD GPU"
    except: pass
    return "GPU"

def get_gpu_usage():
    # Priority 1: Check for NVIDIA cards first (Bypasses AMD integrated graphics bug)
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if out: return out
    except: pass

    # Priority 2: Check for AMD cards (For full-AMD systems)
    try:
        for card in ['card0', 'card1', 'card2']:
            path = f"/sys/class/drm/{card}/device/gpu_busy_percent"
            if os.path.exists(path):
                with open(path, 'r') as f:
                    usage = f.read().strip()
                    if usage: return usage
    except: pass
    
    return "N/A"

def get_temps():
    cpu_t, gpu_t = "", ""
    
    # CPU Temp
    try:
        temps = psutil.sensors_temperatures()
        if 'k10temp' in temps: cpu_t = f"{int(temps['k10temp'][0].current)}°C"
        elif 'coretemp' in temps: cpu_t = f"{int(temps['coretemp'][0].current)}°C"
    except: pass

    # GPU Temp - NVIDIA Priority
    try:
        nv_temp = subprocess.check_output(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if nv_temp: gpu_t = f"{nv_temp}°C"
    except:
        # GPU Temp - AMD Fallback
        try:
            if 'amdgpu' in temps: gpu_t = f"{int(temps['amdgpu'][0].current)}°C"
        except: pass
        
    return cpu_t, gpu_t

def get_uptime():
    try:
        uptime_sec = time.time() - psutil.boot_time()
        hours = int(uptime_sec // 3600)
        minutes = int((uptime_sec % 3600) // 60)
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    except: return "N/A"

def get_spotify():
    try:
        out = subprocess.check_output(["playerctl", "metadata", "--format", "{{ artist }} - {{ title }}"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        return out if out else ""
    except: return ""

print("Sending stats to VRChat Chatbox... (Press Ctrl+C to stop)")

OS_NAME = get_os_name()
CPU_NAME = get_cpu_name()
GPU_NAME = get_gpu_name()

while True:
    cpu_usage = psutil.cpu_percent()
    gpu_usage = get_gpu_usage()
    
    ram = psutil.virtual_memory()
    ram_used = round(ram.used / (1024**3), 1)
    ram_total = round(ram.total / (1024**3), 1)

    cpu_temp, gpu_temp = get_temps()
    song = get_spotify()
    uptime = get_uptime()
    
    current_time = datetime.now().strftime("%I:%M %p")

    banner = f"{current_time} | ⏳ Up: {uptime} | 🐧 {OS_NAME}"
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
