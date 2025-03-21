import os
import platform
import re
import subprocess
dell = "Dell" in subprocess.check_output(["powershell", "Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty Manufacturer"]).decode().strip()
def processor(): 
    if platform.system() == "Windows":
        return platform.processor()
    else:
        return None

def serial_number():
    try:
        if platform.system() == "Windows":
            command = ["powershell", "Get-CimInstance -ClassName Win32_BIOS | Select-Object -ExpandProperty SerialNumber"]
            return subprocess.check_output(command).decode().strip()
        elif platform.system() == "Darwin":
            return None
        elif platform.system() == "Linux":
            return None
    except Exception as e:
        return f"Error retrieving serial number: {e}"

def toexpress(SerialNumber: int):
    return int(SerialNumber, 36)

def ramamount():
    if platform.system() == "Windows":
        command = ["powershell", "(Get-CimInstance -ClassName Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum / 1GB"]
        return subprocess.check_output(command).decode().strip()
    else:
        return None 

def windows_version():
    # Get the Version like 24H2
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_OperatingSystem).Version"]
            version = subprocess.check_output(command).decode().strip()
            return re.sub(r'(\d+)\.(\d+)', r'\1.\2', version)
        else:
            return None
    except Exception as e:
        return f"Error retrieving Windows version: {e}"
def windows_edition():
    # Get the Edition like Windows 11 Pro
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_OperatingSystem).Caption"]
            edition = subprocess.check_output(command).decode().strip()
            return re.sub(r'(\w+)\s+(\d+)', r'\1 \2', edition)
        else:
            return None
    except Exception as e:
        return f"Error retrieving Windows edition: 


        


print(f"Processor {processor}"())
print(f"Serial Number {serial_number()}")
if dell:
    print(f"Express Service Code {toexpress(serial_number())}")
print(f"RAM Amount {ramamount()} GB")

print(serial_number())
print(toexpress(serial_number()))
print(ramamount())

if(dell):
    toexpress(serial_number())
