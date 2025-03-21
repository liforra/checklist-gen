import os
import platform
import re
import subprocess
dell = "Dell" in subprocess.check_output(["powershell", "Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty Manufacturer"]).decode().strip()
def processor(): 
    # Formatted as Intel i5-6300U
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_Processor).Name"]
            return subprocess.check_output(command).decode().strip()
        elif platform.system() == "Darwin":
            return None
        elif platform.system() == "Linux":
            return None
    except Exception as e:
        return f"Error retrieving processor name: {e}"

def processor_freq():
    # in GHz
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_Processor).CurrentClockSpeed"]
            return subprocess.check_output(command).decode().strip()
        else:
            return None
    except Exception as e:
        return f"Error retrieving processor frequency: {e}"
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
def ram_frequency():
    # Get the Ram Frequenzy in MHz
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_PhysicalMemory | Measure-Object -Property Speed -Sum).Sum"]
            return subprocess.check_output(command).decode().strip()
        else:
            return None
    except Exception as e:
        return f"Error retrieving RAM frequency: {e}"
def ram_type():
    # Get the RAM Type like DDR4
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_PhysicalMemory | Measure-Object -Property MemoryType -Sum).Sum"]
            ram_type = subprocess.check_output(command).decode().strip()
            if ram_type == "24":
                return "DDR3"
            elif ram_type == "26":
                return "DDR4"
            elif ram_type == "20":
                return "DDR5"
            else:
                return None
        else:
            return None
    except Exception as e:
        return f"Error retrieving RAM type: {e}"
    
def windows_version():
    # Get the Version like 24H2
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').DisplayVersion"]
            version = subprocess.check_output(command)
            return version
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
        return f"Error retrieving Windows edition: {e}"

def lastupdatedate():
    # Get the date when windows was last updated
    try:
        if platform.system() == "Windows":
            command = ["powershell", "Get-WmiObject -Class Win32_QuickFixEngineering | Select-Object -ExpandProperty InstalledOn | Sort-Object -Descending | Select-Object -First 1"]
            return subprocess.check_output(command).decode().strip()
        else:
            return None
    except Exception as e:
        return f"Error retrieving last update date: {e}"

def product_name():
    # Get the Product Name formatted like Dell Latitude 7280
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_ComputerSystem).Model"]
            return subprocess.check_output(command).decode().strip()
        else:
            return None
    except Exception as e:
        return f"Error retrieving product name: {e}"

def is_active():
    # Check if the Windows is activated
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName SoftwareLicensingProduct | Where-Object { $_.PartialProductKey -ne $null } | Select-Object -ExpandProperty LicenseStatus)"]
            if subprocess.check_output(command).decode().strip() == "1":
                return "Windows is activated"
            else:
                return "Windows is not activated"
        else:
            return None
    except Exception as e:
        return f"Error checking activation status: {e}"

def driveSize():
    # Get the Primary drive Size in GB, only round numbers like 256, 512, 1024
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_LogicalDisk -Filter 'DeviceID=\"C:\"').Size / 1GB"]
            drive_size = subprocess.check_output(command).decode().strip()
            return round(float(drive_size))
        else:
            return None
    except Exception as e:
        return f"Error retrieving drive size: {e}"


print(f"Produkt: {product_name()}; Serial Nr: {serial_number()}")
print(f"CPU: {processor()}/ {processor_freq()} GHz")
print(f"RAM: {ramamount()} GB; {ram_frequency()} MHz; {ram_type()}")

print("---Unsorted---")

print(f"Windows Version: {windows_version()}; Edition: {windows_edition()}")
print(f"Last Update: {lastupdatedate()}")
print(f"Drive Size: {driveSize()} GB")
print(f"Windows Activation Status: {is_active()}")



print("---Debug---")
print(serial_number())
print(toexpress(serial_number()))
print(ramamount())

if(dell):
    toexpress(serial_number())
