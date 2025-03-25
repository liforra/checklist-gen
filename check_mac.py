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
        return subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()
    except:
        return None

def processor_freq():
    try:
        return subprocess.check_output(['sysctl', '-n', 'hw.cpufrequency']).decode().strip()
    except:
        return None

def serial_number():
    try:
        return subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode().strip()
    except:
        return None

def ramamount():
    try:
        total_memory = subprocess.check_output(['sysctl', '-n', 'hw.memsize']).decode().strip()
        return str(round(int(total_memory) / (1024.**3)))
    except:
        return None

def ram_frequency():
    try:
        return subprocess.check_output(['system_profiler', 'SPMemoryDataType']).decode().strip()
    except:
        return None

def ram_type():
    try:
        output = subprocess.check_output(['system_profiler', 'SPMemoryDataType']).decode()
        if 'DDR5' in output: return 'DDR5'
        elif 'DDR4' in output: return 'DDR4'
        elif 'DDR3' in output: return 'DDR3'
        elif 'DDR2' in output: return 'DDR2'
        else: return 'DDR'
    except:
        return None

def windows_version():
    try:
        # Get the version number (e.g. 13.4.1)
        return subprocess.check_output(['sw_vers', '-productVersion']).decode().strip()
    except:
        return None

def windows_edition():
    try:
        # Get the marketing name (e.g. Monterey)
        version = subprocess.check_output(['sw_vers', '-productVersion']).decode().strip().split('.')[0]
        versions = {
            '14': 'Sonoma',
            '13': 'Ventura',
            '12': 'Monterey',
            '11': 'Big Sur',
            '10.15': 'Catalina',
            '10.14': 'Mojave',
            '10.13': 'High Sierra',
            '10.12': 'Sierra'
        }
        return versions.get(version, f"macOS {version}")
    except:
        return None

def lastupdatedate():
    try:
        output = subprocess.check_output(['softwareupdate', '--history']).decode()
        dates = re.findall(r'\d{2}/\d{2}/\d{4}', output)
        if dates:
            date_obj = datetime.datetime.strptime(dates[0], '%d/%m/%Y')
            return date_obj.strftime("%d.%m.%y")
    except:
        return None

def product_name():
    try:
        return subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode().strip()
    except:
        return None

def is_active():
    return None  # macOS-specific: Not applicable

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
        output = subprocess.check_output(['system_profiler', 'SPNVMeDataType', 'SPSerialATADataType']).decode()
        if 'NVMe' in output: return 'M.2 PCIe'
        elif 'SSD' in output: return 'SSD'
        else: return 'HDD'
    except:
        return None

def batteryHealth():
    try:
        output = subprocess.check_output(['system_profiler', 'SPPowerDataType']).decode()
        health = re.search(r'Condition: (.+)', output)
        if health:
            condition = health.group(1)
            return '100' if condition == 'Normal' else '50'
    except:
        return None

def dellexpressstr():
    return ""  # macOS-specific: Not implementing Dell Express

def userlist():
    try:
        output = subprocess.check_output(['dscl', '.', '-list', '/Users']).decode()
        users = [user for user in output.split() if not user.startswith('_') and user != 'root' and user != 'daemon']
        return ", ".join(sorted(users))
    except:
        return None

def bitlocker():
    try:
        output = subprocess.check_output(['diskutil', 'apfs', 'list']).decode()
        return "Encrypted" if 'FileVault' in output else "Not Encrypted"
    except:
        return None

def domain():
    try:
        return subprocess.check_output(['dsconfigad', '-show']).decode().strip() or "Keine"
    except:
        return "Keine"

def gpu():
    try:
        return subprocess.check_output(['system_profiler', 'SPDisplaysDataType']).decode().strip()
    except:
        return None

def get_ram_slots():
    try:
        output = subprocess.check_output(['system_profiler', 'SPMemoryDataType']).decode()
        total = output.count('BANK')
        used = output.count('Size:') - output.count('Empty')
        return f"{used}/{total}"
    except:
        return None

def ramsticktype():
    try:
        output = subprocess.check_output(['system_profiler', 'SPMemoryDataType']).decode()
        if 'SODIMM' in output: return 'SO-DIMM'
        elif 'DIMM' in output: return 'DIMM'
        else: return 'Unknown'
    except:
        return None