# This is mainly AI Generated from check.py
import os
import platform
import subprocess
import shutil
import datetime
import re

"""
// vscode-fold=1
"""

def processor():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f.readlines():
                if 'model name' in line:
                    return line.split(':')[1].strip()
    except:
        try:
            return subprocess.check_output(['lscpu'], text=True).split('\n')[13].split(':')[1].strip()
        except:
            try:
                return subprocess.check_output(['sudo', 'dmidecode', '-s', 'processor-version']).decode().strip()
            except:
                return None

def processor_freq():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f.readlines():
                if 'cpu MHz' in line:
                    return str(float(line.split(':')[1].strip()) / 1000)
    except:
        try:
            output = subprocess.check_output(['lscpu'], text=True)
            for line in output.split('\n'):
                if 'CPU MHz' in line:
                    return str(float(line.split(':')[1].strip()) / 1000)
        except:
            try:
                output = subprocess.check_output(['cpufreq-info'], text=True)
                freq = re.search(r'current CPU frequency is ([\d.]+) MHz', output)
                if freq:
                    return str(float(freq.group(1)) / 1000)
            except:
                return None

def serial_number():
    try:
        return subprocess.check_output(['sudo', 'dmidecode', '-s', 'system-serial-number']).decode().strip()
    except:
        try:
            output = subprocess.check_output(['hostnamectl'], text=True)
            for line in output.split('\n'):
                if 'Hardware ID' in line:
                    return line.split(':')[1].strip()
        except:
            try:
                with open('/sys/devices/virtual/dmi/id/product_serial', 'r') as f:
                    return f.read().strip()
            except:
                return None

def ramamount():
    try:
        total_memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        return str(round(total_memory / (1024.**3)))
    except:
        return None

def ram_frequency():
    try:
        return subprocess.check_output(['sudo', 'dmidecode', '-t', 'memory']).decode().strip()
    except:
        return None

def ram_type():
    try:
        output = subprocess.check_output(['sudo', 'dmidecode', '-t', 'memory']).decode()
        if 'DDR5' in output: return 'DDR5'
        elif 'DDR4' in output: return 'DDR4'
        elif 'DDR3' in output: return 'DDR3'
        elif 'DDR2' in output: return 'DDR2'
        else: return 'DDR'
    except:
        return None

def windows_version():
    return None  # Linux-specific: Not applicable

def windows_edition():
    return None  # Linux-specific: Not applicable

def lastupdatedate():
    try:
        # For apt-based systems
        last_update = subprocess.check_output(['stat', '/var/lib/apt/periodic/update-success-stamp']).decode()
        date_str = re.search(r'Modify: (.+?)\.', last_update).group(1)
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date_obj.strftime("%d.%m.%y")
    except:
        return None

def product_name():
    try:
        return subprocess.check_output(['sudo', 'dmidecode', '-s', 'system-product-name']).decode().strip()
    except:
        return None

def is_active():
    return None  # Linux-specific: Not applicable

def driveSize(path='/'):
    try:
        total_bytes = shutil.disk_usage(path).total
        total_gb = total_bytes / (1024 ** 3)
        power = 0
        while (2 ** power) < total_gb:
            power += 1
        if total_gb - (2 ** (power - 1)) < (2 ** power) - total_gb and power > 0:
            power -= 1
        return 2 ** power
    except:
        return 0

def driveType():
    try:
        output = subprocess.check_output(['lsblk', '-d', '-o', 'name,rota']).decode()
        for line in output.split('\n'):
            if 'sda' in line or 'nvme0n1' in line:
                return 'HDD' if '1' in line else 'SSD'
    except:
        return None

def batteryHealth():
    try:
        energy_full = int(subprocess.check_output(['cat', '/sys/class/power_supply/BAT0/energy_full']).decode())
        energy_full_design = int(subprocess.check_output(['cat', '/sys/class/power_supply/BAT0/energy_full_design']).decode())
        return str(round((energy_full / energy_full_design) * 100))
    except:
        return None

def dellexpressstr():
    return ""  # Linux-specific: Not implementing Dell Express

def userlist():
    try:
        users = []
        with open('/etc/passwd', 'r') as f:
            for line in f:
                user = line.split(':')[0]
                if 1000 <= int(line.split(':')[2]) < 60000:  # Regular users
                    users.append(user)
        return ", ".join(sorted(users))
    except:
        return None

def bitlocker():
    try:
        output = subprocess.check_output(['sudo', 'blkid']).decode()
        return "Encrypted" if 'LUKS' in output else "Not Encrypted"
    except:
        return None

def domain():
    try:
        return subprocess.check_output(['domainname']).decode().strip() or "Keine"
    except:
        return "Keine"

def gpu():
    try:
        return subprocess.check_output(['lspci', '-v', '-s', "$(lspci | grep ' VGA ' | cut -d' ' -f 1)"]).decode().strip()
    except:
        return None

def get_ram_slots():
    try:
        output = subprocess.check_output(['sudo', 'dmidecode', '-t', 'memory']).decode()
        total = output.count('Memory Device')
        used = len([l for l in output.split('\n') if 'Size:' in l and 'No Module Installed' not in l])
        return f"{used}/{total}"
    except:
        return None

def ramsticktype():
    try:
        output = subprocess.check_output(['sudo', 'dmidecode', '-t', 'memory']).decode()
        if 'SODIMM' in output: return 'SO-DIMM'
        elif 'DIMM' in output: return 'DIMM'
        else: return 'Unknown'
    except:
        return None