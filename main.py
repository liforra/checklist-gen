import os
import platform
import re
import subprocess
import shutil
import datetime
import battery
import wmi

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
    # Get the actual RAM frequency in MHz (as shown in Task Manager) 
    try:
        if platform.system() == "Windows":
            # Using ConfiguredClockSpeed instead of Speed to get the actual running frequency
            command = ["powershell", "Get-CimInstance -ClassName Win32_PhysicalMemory | Select-Object -First 1 -ExpandProperty ConfiguredClockSpeed"]
            return subprocess.check_output(command).decode().strip()
        else:
            return None
    except Exception as e:
        return f"Error retrieving RAM frequency: {e}"
def ram_type():
    # Get the RAM Type like DDR4
    try:
        if platform.system() == "Windows":
            command = ["powershell", "Get-CimInstance -ClassName Win32_PhysicalMemory | Select-Object -ExpandProperty SMBIOSMemoryType -First 1"]
            ram_type = subprocess.check_output(command).decode().strip()
            memory_types = {
                "20": "DDR",
                "21": "DDR2",
                "24": "DDR3",
                "26": "DDR4",
                "34": "DDR5"
            }
            return memory_types.get(ram_type, f"Unknown ({ram_type})")
        else:
            return None
    except Exception as e:
        return f"Error retrieving RAM type: {e}"
def windows_version():
    # Get the Version like 24H2
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').DisplayVersion"]
            version = subprocess.check_output(command).decode().strip()
            # Remove any carriage returns, newlines, and extra whitespace
            version = version.replace('\r', '').replace('\n', '').strip()
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
    """Returns the last update date of Windows in DD.MM.YY format."""
    try:
        # Check if running on Windows
        if platform.system() != "Windows":
            return "Function only works on Windows systems."
        
        # Try using wmic which is more reliable with encoding
        cmd = "wmic qfe list brief /format:table"
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse the output to find dates
            date_pattern = r'\d{1,2}/\d{1,2}/\d{4}'
            dates = re.findall(date_pattern, result.stdout)
            
            if dates:
                # Convert found dates to datetime objects
                parsed_dates = []
                for date_str in dates:
                    try:
                        parsed_dates.append(datetime.datetime.strptime(date_str, "%m/%d/%Y"))
                    except ValueError:
                        try:
                            parsed_dates.append(datetime.datetime.strptime(date_str, "%d/%m/%Y"))
                        except ValueError:
                            continue
                
                # Return the most recent date if any were found and parsed
                if parsed_dates:
                    latest_date = max(parsed_dates)
                    return latest_date.strftime("%d.%m.%y")
            
            # If no dates found or parsed, try alternative method
            cmd2 = "systeminfo | findstr /C:\"Last Hotfix\""
            result2 = subprocess.run(
                cmd2,
                capture_output=True,
                text=True,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )
            
            if result2.returncode == 0 and result2.stdout.strip():
                # Extract date using regex
                match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', result2.stdout)
                if match:
                    date_str = match.group(0)
                    try:
                        date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y")
                        return date_obj.strftime("%d.%m.%y")
                    except ValueError:
                        try:
                            date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
                            return date_obj.strftime("%d.%m.%y")
                        except ValueError:
                            pass
        
        # If all else fails, use PowerShell with explicit encoding handling
        cmd3 = "powershell -Command \"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-HotFix | Sort-Object -Property InstalledOn -Descending | Select-Object -First 1 -ExpandProperty InstalledOn\""
        result3 = subprocess.run(
            cmd3,
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result3.returncode == 0 and result3.stdout.strip():
            date_str = result3.stdout.strip()
            formats = [
                "%m/%d/%Y %I:%M:%S %p",
                "%d/%m/%Y %I:%M:%S %p",
                "%m/%d/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%Y-%m-%d %H:%M:%S"
            ]
            
            for fmt in formats:
                try:
                    date_obj = datetime.datetime.strptime(date_str, fmt)
                    return date_obj.strftime("%d.%m.%y")
                except ValueError:
                    continue
        
        return "Could not determine last update date."
    except Exception as e:
        return f"Error determining last update date: {str(e)}"

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


def driveSize(path=None):
    """
    Calculate the drive size for a Windows system in GB, rounded to common values.
    
    Args:
        path (str, optional): Path to check. Defaults to Windows installation directory.
    
    Returns:
        int: Drive size in GB, rounded to common values like 128, 256, 1024, etc.
    """
    if path is None:
        # Default to Windows installation directory
        path = os.environ.get("WINDIR", "C:\\Windows")
    
    # Get the drive from the path (e.g., 'C:' from 'C:\Windows')
    drive = os.path.splitdrive(path)[0]
    if not drive:
        drive = "C:"  # Fallback if drive can't be determined
    
    try:
        # Get total size in bytes
        total_bytes = shutil.disk_usage(drive).total
        
        # Convert to GB
        total_gb = total_bytes / (1024 ** 3)
        
        # Round to nearest power of 2
        power = 0
        while (2 ** power) < total_gb:
            power += 1
        
        # If we're closer to the lower power of 2, use that
        if total_gb - (2 ** (power - 1)) < (2 ** power) - total_gb and power > 0:
            power -= 1
        
        return 2 ** power
    
    except Exception as e:
        print(f"Error determining drive size: {e}")
        return 0


def driveType():
    # Get the type of the drive
    # Possible Values are: HDD, SSD, M.2 Sata, M.2 PCIe
    try:
        if platform.system() == "Windows":
            # Get drive info for C: drive
            cmd = ["powershell", """
                $disk = Get-PhysicalDisk | Where-Object { 
                    $_.DeviceId -eq ((Get-Partition -DriveLetter C).DiskNumber) 
                }
                $bus = $disk.BusType
                $media = $disk.MediaType
                "$bus,$media"
            """]
            result = subprocess.check_output(cmd).decode().strip()
            bus_type, media_type = result.split(',')
            
            if "NVMe" in bus_type:
                return "M.2 PCIe"
            elif "SATA" in bus_type:
                if "SSD" in media_type:
                    if "M.2" in result:
                        return "M.2 SATA"
                    return "SSD"
                else:
                    return "HDD"
            return f"Unknown ({bus_type})"
        else:
            return None
    except Exception as e:
        return f"Error retrieving drive type: {e}"

def batteryHealth():
    return battery.get_battery_health()

def dellexpressstr():
    if dell:
        express = toexpress(serial_number())
        return f"; Express Service Tag: {str(express)}"
    else:
        return ""

def userlist():
    # Get the list of users minus the standard ones, so no SYSTEM, Administrator, etc.
    # Important. The format is like this: "User1, User2, User3"
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_UserProfile | Where-Object { $_.Special -eq $false }).LocalPath"]
            users = subprocess.check_output(command).decode().strip()
            # Remove the C:\Users\ part
            users = [user.split("\\")[-1] for user in users.splitlines()]
            # Remove duplicates and sort
            users = sorted(set(users))
            return ", ".join(users)
        else:
            return None
    except Exception as e:
        return f"Error retrieving user list: {e}"
    
def bitlocker():
    # Check if the Main Drive is encrypted with Bitlocker
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-BitLockerVolume -MountPoint 'C:').ProtectionStatus"]
            status = subprocess.check_output(command).decode().strip()
            return "Encrypted" if status == "1" else "Not Encrypted"
        else:
            return None
    except Exception as e:
        return f"Error checking BitLocker status: {e}"

def domain():
    # Check in what domain the computer is registered in. if there is none return the string "Keine"
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_ComputerSystem).Domain"]
            domain = subprocess.check_output(command).decode().strip()
            return domain if domain else "Keine"
        else:
            return None
    except Exception as e:
        return f"Error retrieving domain: {e}"

def gpu():
    # Get the GPU name
    try:
        if platform.system() == "Windows":
            command = ["powershell", "(Get-CimInstance -ClassName Win32_VideoController).Name"]
            gpu_name = subprocess.check_output(command).decode().strip()
            return gpu_name
        else:
            return None
    except Exception as e:
        return f"Error retrieving GPU name: {e}"
def get_ram_slots():
    c = wmi.WMI()
    inserted = len(c.Win32_PhysicalMemory())
    total = c.Win32_PhysicalMemoryArray()[0].MemoryDevices
    return f"{inserted}/{total}"



print(f"Produkt: {product_name()}; Serial Nr: {serial_number()}{dellexpressstr()}")
print(f"CPU: {processor()}; Akkuzustand: {batteryHealth()}%")
print(f"GPU: {gpu()}")
print(f"RAM: {ramamount()} GB; {ram_frequency()} MHz; {ram_type()};  Slots: {get_ram_slots()}")
print(f"Hauptfestplatte: {driveSize()} GB; {driveType()}")
print(f"Betriebsystem: {windows_edition()}; Version: {windows_version()}")
print(f"Letztes Update: {lastupdatedate()}")
print("\n")
print(f"Benutzer: {userlist()}")
print(f"Bitlocker: {bitlocker()}")
print(f"In der Domäne: {domain()}")
print("\n")


# import file choice.py
import choice # This runs continously and will eventually exit the program if the user decides so
