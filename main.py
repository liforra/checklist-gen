# AI Disclaimer: This script was created heavily using AI.
# Good Luck.
import time
from blessed import Terminal
import threading
import time
import platform
import os
import subprocess
match platform.system():
    case "Windows":
        import check as c
    case "Linux":
        import check_linux as c
    case "Darwin":
        import check_mac as c
    case _:
        raise NotImplementedError(f"Unsupported platform: {platform.system()}")


def check_number(number):
    os_type = platform.system()
    
    if os_type == "Windows":
        match number:
            case 1:
                os.system("start devmgmt.msc")
            case 2:
                os.system("start ms-settings:windowsupdate")
            case 3:
                os.system("start https://liforra.de/keyboardtest.exe")
            case 4:
                os.system("start cmd /c powercfg /batteryreport")
            case 5:
                raw_input_test()
            case 6:
                run_CrystalDiskMark()
            case 801:
                os.system("powershell -c \"irm https://get.activated.win | iex\"")
            case _:
                print(f"Option {number} nicht verfügbar für Windows")
    
    elif os_type == "Darwin":  # macOS
        match number:
            case 1:
                subprocess.run(["open", "/System/Library/PreferencePanes/Security.prefPane"])
            case 2:
                subprocess.run(["open", "/System/Library/PreferencePanes/SoftwareUpdate.prefPane"])
            case 4:
                subprocess.run(["system_profiler", "SPPowerDataType"])
            case 5:
                raw_input_test()
            case _:
                print(f"Option {number} nicht verfügbar für macOS")
    
    elif os_type == "Linux":
        match number:
            case 1:
                subprocess.run(["lshw"])
            case 2:
                if os.path.exists("/usr/bin/software-properties-gtk"):
                    subprocess.run(["software-properties-gtk"])
                else:
                    print("Software updater not found")
            case 4:
                subprocess.run(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"])
            case 5:
                raw_input_test()
            case _:
                print(f"Option {number} nicht verfügbar für Linux")
    
    else:
        print(f"Betriebssystem {os_type} wird nicht unterstützt")



cthread = 0
check_threads = []

def check_runner():
    check()

def start_check_threads():
    global cthread, check_threads
    for i in range(3):
        cthread += 1
        thread = threading.Thread(target=check_runner, daemon=True)
        check_threads.append(thread)
        thread.start()

def check():
    
    global cthread
    match cthread:
        case 1:
            # Hardware information
            cpu = c.processor()
            cpu_freq = c.processor_freq()
            gpu = c.gpu()
            battery_health = c.batteryHealth()
            product = c.product_name()
            serial = c.serial_number()
            dell_express = c.dellexpressstr()
            
        case 2:
            # Memory and storage information
            ram_amount = c.ramamount()
            ram_freq = c.ram_frequency()
            ram_type = c.ram_type()
            ram_slots = c.get_ram_slots()
            ram_stick_type = c.ramsticktype()
            drive_size = c.driveSize()
            drive_type = c.driveType()
            
        case 3:
            # System and software information
            windows_ed = c.windows_edition()
            windows_ver = c.windows_version()
            activation = c.is_active()
            last_update = c.lastupdatedate()
            users = c.userlist()
            bitlocker_status = c.bitlocker()
            domain_info = c.domain()
            
        case _:
            return None





class Menu:
    def __init__(self, options):
        self.options = options
        self.current_option = 0
        self.term = Terminal()
        self.number_buffer = ""
        self.error_message = ""
        self.error_time = 0
        self.last_selected = None

    def is_visible(self, num):
        return not (800 <= num <= 999)
        
    def get_layout(self):
        # Calculate max item width and terminal space
        max_width = max(len(option[1]) for option in self.options) + 4  # +4 for prefix and padding
        term_width = self.term.width
        
        # Calculate number of possible columns
        num_columns = max(1, term_width // max_width)
        num_rows = (len(self.options) + num_columns - 1) // num_columns
        
        return max_width, num_columns, num_rows
        
    def display(self):
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear)
                print(self.term.move_y(0) + "=== Menu ===\n")
                
                # Filter visible options for display only
                visible_options = [(idx, opt) for idx, opt in enumerate(self.options) 
                                 if self.is_visible(opt[0])]
                
                max_width, num_columns, num_rows = self.get_layout()
                
                # Display items in grid (visible only)
                for row in range(num_rows):
                    line = ""
                    for col in range(num_columns):
                        idx = col * num_rows + row
                        if idx < len(visible_options):
                            orig_idx, (num, text) = visible_options[idx]
                            prefix = '>' if orig_idx == self.current_option else ' '
                            item = f"{prefix} [{num:2}] {text}"
                            line += item.ljust(max_width)
                    print(line)
                
                # Show number buffer or error
                if self.error_message and time.time() - self.error_time < 2:
                    print(f"\nError: {self.error_message}")
                elif self.number_buffer:
                    print(f"\nEntering: {self.number_buffer}")
                    
                # Show last selection
                if self.last_selected is not None:
                    print(f"\nLast selected: {self.last_selected}")
                
                key = self.term.inkey()
                
                if key.isdigit():
                    self.number_buffer += key
                    self.error_message = ""
                    # Try to find matching option
                    try:
                        num = int(self.number_buffer)
                        found = False
                        for idx, (opt_num, _) in enumerate(self.options):
                            if opt_num == num:  # Exact match only
                                self.current_option = idx
                                found = True
                                break
                        if not found and len(self.number_buffer) >= 3:
                            self.error_message = f"No option with number {num}"
                            self.error_time = time.time()
                    except ValueError:
                        pass
                elif key.name == 'KEY_BACKSPACE':
                    if self.number_buffer:
                        self.number_buffer = self.number_buffer[:-1]
                        self.error_message = ""
                elif key.name == 'KEY_ENTER' and self.number_buffer:
                    try:
                        num = int(self.number_buffer)
                        found = False
                        for idx, (opt_num, _) in enumerate(self.options):
                            if opt_num == num:
                                self.last_selected = num
                                return idx
                        if not found:
                            self.error_message = f"No option with number {num}"
                            self.error_time = time.time()
                            self.number_buffer = ""
                    except ValueError:
                        pass
                elif key.name == 'KEY_ENTER':
                    return self.current_option
                elif key == 'q':
                    return len(self.options) - 1
                # Clear buffer on escape
                elif key.name == 'KEY_ESCAPE':
                    self.number_buffer = ""
                elif key.name == 'KEY_UP' or key == 'k':
                    self.current_option = max(0, self.current_option - 1)
                elif key.name == 'KEY_DOWN' or key == 'j':
                    self.current_option = min(len(self.options) - 1, self.current_option + 1)
                elif key.name == 'KEY_LEFT' or key == 'h':
                    self.current_option = max(0, self.current_option - num_rows)
                elif key.name == 'KEY_RIGHT' or key == 'l':
                    self.current_option = min(len(self.options) - 1, self.current_option + num_rows)

def main():
    term = Terminal()
    menu_options = [
        (1, "Device Manager"),
        (2, "Windows Update"),
        (3, "Keyboard Test"),
        (4, "Battery Report"),
        (5, "Raw Input Test"),
        (6, "CrystalDiskMark"),
        (801, "Windows Activation"),
        (0, "Exit")
    ]
    
    try:
        # Start all check threads before creating menu
        start_check_threads()
        # Create and show menu while threads run in background
        menu = Menu(menu_options)
        while True:
            selection = menu.display()
            # Get the selected number from the menu options
            selected_num = menu_options[selection][0]
            if selected_num == 0:
                break
            # Handle selection using the existing check_number function
            print(term.clear)
            from choice import check_number
            check_number(selected_num)
            print("\nPress Enter to continue...")
            term.inkey()
    finally:
        # Cleanup threads on exit
        for thread in check_threads:
            thread.join(timeout=0.5)

if __name__ == "__main__":
    main()
