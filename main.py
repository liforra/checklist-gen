# AI Disclaimer: This script was created heavily using AI.
# Good Luck.
try:
    from blessed import Terminal
    import threading
    import time
    import platform
    import os
    import subprocess

except ImportError as e:
    print(f"Oops, you forgot to add the libraries to requirements.txt. ")
import liforra
testkeyboard = True
esc_press_count = 0  # Add this line

try:
    from pynput import keyboard, mouse
    from tkinter import filedialog, Tk
except ImportError as e:
    print(f"No X Server or Wayland Server found. Or keyboard and mouse library arent present.")
    print(f"Disabling Input Tester.")
    testkeyboard = False
try:
    from portableapps import portableApps
except ImportError:
    def portableApps():
        print("Portable Apps Funktion nicht verfügbar, da portableapps.py nicht gefunden wurde.")



match platform.system():
    case "Windows":
        import check as c
    case _:
        raise NotImplementedError(f"Unsupported platform: {platform.system()}")
"""    case "Linux":
        import check_linux as c
    case "Darwin":
        import check_mac as c"""


    

# Initialize global variables for hardware info
cpu = ""
cpu_freq = ""
gpu = ""
battery_health = ""
product = ""
serial = ""
dell_express = ""
ram_amount = ""
ram_freq = ""
ram_type = ""
ram_slots = ""
ram_stick_type = ""
drive_size = ""
drive_type = ""
windows_ed = ""
windows_ver = ""
activation = ""
last_update = ""
users = ""
bitlocker_status = ""
domain_info = ""

def dump():
    if "tkinter" in globals():
        root = Tk()
        root.withdraw()  # Hide the main tkinter window        
        # Find the first drive with the ChecklistDump directory
        drives_with_dump = liforra.find_dir("ChecklistDump")
        default_folder = drives_with_dump[0] if drives_with_dump else os.getcwd()
        
        folder_path = filedialog.askdirectory(
            title="Select Folder to Save Checklist Dump",
            initialdir=default_folder
        )
        if folder_path:
            print(f"Selected folder: {folder_path}")
            
            # Format the filename
            global product, serial
            if not product or not serial:
                print("Product or Serial information is missing. Cannot create file.")
                return
            
            filename_base = f"{product.replace(' ', '_')}_{serial}"
            file_types = [("Text File", "*.txt"), ("JSON File", "*.json"), ("CSV File", "*.csv")]
            file_path = filedialog.asksaveasfilename(
                initialdir=folder_path,
                initialfile=filename_base,
                title="Save Checklist Dump",
                filetypes=file_types,
                defaultextension=".txt"
            )
            
            if file_path:
                print(f"File will be saved as: {file_path}")
                # Determine file extension and save content accordingly
                _, ext = os.path.splitext(file_path)
                ext = ext.lower()
                content = {
                    "product": product,
                    "serial": serial,
                    "cpu": cpu,
                    "gpu": gpu,
                    "battery_health": battery_health,
                    "ram_amount": ram_amount,
                    "drive_size": drive_size,
                    "windows_version": windows_ver,
                }
                
                try:
                    if ext == ".json":
                        import json
                        with open(file_path, "w") as file:
                            json.dump(content, file, indent=4)
                    elif ext == ".csv":
                        import csv
                        with open(file_path, "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(content.keys())
                            writer.writerow(content.values())
                    else:  # Default to .txt
                        with open(file_path, "w") as file:
                            for key, value in content.items():
                                file.write(f"{key}: {value}\n")
                except Exception as e:
                    print(f"Error saving file: {e}")
            else:
                print("File save operation was canceled.")
        else:
            print("No folder selected.")
    else:
        print("GUI not available. Returning 0.")
        return 0
    liforra.find_dir("ChecklistDump")
    # use the first drive found
    drive = liforra.find_dir("ChecklistDump")[0]
    # Spawn a file explorer choose dialog, on the folder drive + "ChecklistDump"
    # with the file types Json, txt, and csv

def raw_input_test(from_gui=False):
    global esc_press_count
    esc_press_count = 0  # Reset counter when starting test
    if not testkeyboard:
        print("Input tester is disabled.")
        return
    if from_gui:
        return  # Skip terminal version when called from GUI
        
    # This will import one library and show every key up and down

    # Callback for keyboard events
    def on_key_press(key):
        global esc_press_count
        try:
            print(f"Taste: {key.char} gedrückt")
        except AttributeError:
            print(f"Spezielle Taste: {key} gedrückt")

        # Check for 'Esc' key
        if key == keyboard.Key.esc:
            esc_press_count += 1
            print(f"'Esc' {esc_press_count} mal gedrückt (Zwei mal drücken um zum Hauptmenü zurückzukehren)")
            if esc_press_count == 2:
                print("Returning to main menu...")
                return False  # Stop the keyboard listener

    def on_key_release(key):
        print(f"Key released: {key}")

    # Callback for mouse events
    def on_click(x, y, button, pressed):
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")
        else:
            print(f"Mouse released at ({x}, {y}) with {button}")

    def on_scroll(x, y, dx, dy):
        print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

    # Start keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    keyboard_listener.start()

    # Start mouse listener
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()

    # Keep the program running until 'Esc' is pressed twice
    keyboard_listener.join()
    mouse_listener.stop()







def check_number(number):
    os_type = platform.system()
    
    if os_type == "Windows":
        match number:
            case 1:
                info()
                return True
            case 2:
                os.system("start devmgmt.msc")
                return True
            case 3:
                os.system("start ms-settings:windowsupdate")
                return True
            case 5:
                raw_input_test()
                return True
            case 7:
                raw_input_test()
                return True
            case 6:
                portableApps()
                return True
            case 801:
                os.system("powershell -c \"irm https://get.activated.win | iex\"")
                return True
            case 4:
                os.system("start taskmgr")
                return True
            case 8:
                os.system("powercfg /batteryreport")
                os.system("start battery-report.html")
                return True
            case 9:
                dump()
            case _:
                print(f"Option {number} nicht verfügbar für Windows")
                return True
""" 
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
        return
    
    else:
        print(f"Betriebssystem {os_type} wird nicht unterstützt")
"""


cthread = 0
check_threads = []
threads_complete = False

def check_runner():
    check()

def start_check_threads():
    global cthread, check_threads, threads_complete
    threads_complete = False
    for i in range(3):
        cthread += 1
        thread = threading.Thread(target=check_runner, daemon=True)
        check_threads.append(thread)
        thread.start()

def wait_for_threads():
    global threads_complete
    for thread in check_threads:
        thread.join()
    threads_complete = True

def get_thread_status():
    return threads_complete

def check():
    global cthread, cpu, cpu_freq, gpu, battery_health, product, serial, dell_express
    global ram_amount, ram_freq, ram_type, ram_slots, ram_stick_type, drive_size, drive_type
    global windows_ed, windows_ver, activation, last_update, users, bitlocker_status, domain_info
    
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


def info():
    global threads_complete
    if not threads_complete:
        print("Please wait while system information is being gathered...")
        wait_for_threads()
    print(f"Produkt: {cpu}; Serial Nr: {serial}{dell_express}")
    print(f"CPU: {cpu}; Akkuzustand: {battery_health}%")
    print(f"GPU: {gpu}")
    print(f"RAM: {ram_amount} GB; {ram_freq} MHz; {ram_type};  Slots: {ram_slots}; RAM-Art: {ram_stick_type}")
    print(f"Hauptfestplatte: {drive_size} GB; {drive_type}")
    print(f"Betriebsystem: {windows_ed}; Version: {windows_ver}; Aktivierung: {activation}")
    print(f"Letztes Update: {last_update}")
    print("\n")
    print(f"Benutzer: {users}")
    print(f"Bitlocker: {bitlocker_status}")
    print(f"In der Domäne: {domain_info}")
    print("\n")

menu_options = [
    (1, "Hardware Information"),
    (2, "Device Manager"),
    (3, "Windows Update"),
    (8, "Battery Report"),
    (6, "Portable Apps"),
    (4, "TaskManager"),
    (801, "Windows Activation"),
    (0, "Exit"),
    (7, "Raw Input Test"),
    (8, "Dump to File")
]

if testkeyboard:
    menu_options.insert(2, (5, "Keyboard Test"))


class Menu:
    def __init__(self, options):
        self.options = options
        self.current_option = 0
        self.term = Terminal()
        self.term.reset()  # Reset terminal state on initialization
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

    def next_visible_option(self, current, direction):
        new_option = current + direction
        while 0 <= new_option < len(self.options):
            if self.is_visible(self.options[new_option][0]):
                return new_option
            new_option += direction
        return current
        
    def display(self):
        try:
            with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
                while True:
                    print(self.term.clear)
                    print(self.term.move_y(0) + "=== Menu ===\n")
                    
                    visible_options = [(idx, opt) for idx, opt in enumerate(self.options) 
                                     if self.is_visible(opt[0])]
                    
                    max_width, num_columns, num_rows = self.get_layout()
                    
                    for row in range(num_rows):
                        line = ""
                        for col in range(num_columns):
                            idx = col * num_rows + row
                            if idx < len(visible_options):
                                orig_idx, (num, text) = visible_options[idx]
                                prefix = '>' if orig_idx == self.current_option else ' '
                                item = f"{prefix} [{num}] {text}"
                                line += item.ljust(max_width)
                        print(line)
                    
                    if self.error_message and time.time() - self.error_time < 2:
                        print(f"\nError: {self.error_message}")
                    if self.number_buffer:
                        print(f"\nEntering: {self.number_buffer}")
                    
                    if self.last_selected is not None:
                        print(f"\nLast selected: {self.last_selected}")
                    
                    key = self.term.inkey()
                    
                    # Handle key input for both string and key object types
                    if isinstance(key, str):
                        if key.isdigit():
                            self.number_buffer += key
                            self.error_message = ""
                            try:
                                num = int(self.number_buffer)
                                for idx, (opt_num, _) in enumerate(self.options):
                                    if opt_num == num:
                                        self.current_option = idx
                                        break
                            except ValueError:
                                pass
                    elif hasattr(key, 'name'):
                        if key.name == 'KEY_BACKSPACE':
                            if self.number_buffer:
                                self.number_buffer = self.number_buffer[:-1]
                                self.error_message = ""
                                if self.number_buffer:
                                    try:
                                        num = int(self.number_buffer)
                                        for idx, (opt_num, _) in enumerate(self.options):
                                            if opt_num == num:
                                                self.current_option = idx
                                                break
                                    except ValueError:
                                        pass
                        elif key.name == 'KEY_ENTER':
                            if self.number_buffer:
                                try:
                                    num = int(self.number_buffer)
                                    found = False
                                    for idx, (opt_num, _) in enumerate(self.options):
                                        if opt_num == num:
                                            found = True
                                            self.last_selected = None  # Reset last selected
                                            self.number_buffer = ""
                                            return idx
                                    if not found:
                                        self.error_message = f"No option with number {num}"
                                        self.error_time = time.time()
                                        self.number_buffer = ""
                                except ValueError:
                                    self.error_message = "Invalid number"
                                    self.error_time = time.time()
                                    self.number_buffer = ""
                            else:
                                self.last_selected = None  # Reset last selected
                                return self.current_option
                        elif key == 'q':
                            return len(self.options) - 1
                        elif key.name == 'KEY_ESCAPE':
                            self.number_buffer = ""
                        elif key.name == 'KEY_UP' or key == 'k':
                            self.current_option = self.next_visible_option(self.current_option, -1)
                        elif key.name == 'KEY_DOWN' or key == 'j':
                            self.current_option = self.next_visible_option(self.current_option, 1)
                        elif key.name == 'KEY_LEFT' or key == 'h':
                            self.current_option = self.next_visible_option(self.current_option, -num_rows)
                        elif key.name == 'KEY_RIGHT' or key == 'l':
                            self.current_option = self.next_visible_option(self.current_option, num_rows)
        finally:
            self.term.reset()  # Ensure terminal is reset when display ends

import sys
import win32gui
import win32con

def hideConsole():
    if __name__ == "__main__":  # Only hide console when run directly
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        except:
            pass

def main():
    hideConsole()
    # Bypass terminal initialization completely for GUI mode
    import sys
    import os
    
    # Redirect stdout and stderr to null
    sys.stdout = open('nul', 'w')
    sys.stderr = open('nul', 'w')
    
    class TerminalMock:
        def __init__(self):
            self.width = 80
            self.height = 24
            self.fullscreen = self.cbreak = self.hidden_cursor = self.dummy_context
            self.clear = ''
            self.move_y = lambda y: ''
            
        def __call__(self, *args, **kwargs):
            return self
            
        def dummy_context(self):
            class DummyContext:
                def __enter__(self): pass
                def __exit__(self, *args): pass
            return DummyContext()
            
        def reset(self): pass
        
        def inkey(self, *args, **kwargs):
            time.sleep(0.1)  # Prevent CPU spin
            return type('Key', (), {'name': None, 'is_sequence': False})
            
        def clear(self): return ''
        def move_y(self, y): return ''
        def print(self, *args, **kwargs): pass
    
    # Replace Terminal() with our mock
    global Terminal
    Terminal = TerminalMock
    term = Terminal()
    
    try:
        start_check_threads()
        wait_thread = threading.Thread(target=wait_for_threads, daemon=True)
        wait_thread.start()
        
        while True:
            term.reset()  # Reset terminal state
            menu = Menu(menu_options)
            try:
                selection = menu.display()
                if selection is None:
                    continue
                selected_num = menu_options[selection][0]
                if selected_num == 0:
                    break
                print(term.clear)
                check_number(selected_num)
                input("\nPress Enter to continue...")
            finally:
                term.reset()  # Ensure terminal is reset after each menu iteration
    finally:
        term.reset()  # Final cleanup
        for thread in check_threads:
            thread.join(timeout=0.5)



def run(option:int):
    global threads_complete
    if option == 1 and not threads_complete:  # For hardware info, make sure threads are running
        if not check_threads:  # Only start if not already started
            start_check_threads()
    check_number(option)



if __name__ == "__main__":
    main()
