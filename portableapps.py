import os
from blessed import Terminal
import subprocess

def portableApps():
    # Windows specific
    from difflib import SequenceMatcher

    def similar(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def clean_name(name):
        return name.replace('Portable', '').strip()

    def find_most_similar_exe(folder_name, exe_files):
        best_match = None
        highest_similarity = 0
        
        clean_folder_name = clean_name(folder_name)
        
        for exe in exe_files:
            exe_name = os.path.splitext(os.path.basename(exe))[0]
            clean_exe_name = clean_name(exe_name)
            similarity = similar(clean_folder_name, clean_exe_name)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = exe
        return best_match if highest_similarity > 0.3 else None

    portable_apps = []
    for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_path = f"{drive}:\\"
        portable_apps_path = os.path.join(drive_path, "PortableApps")
        if os.path.exists(portable_apps_path):
            for app_dir in os.listdir(portable_apps_path):
                app_path = os.path.join(portable_apps_path, app_dir)
                if not os.path.isdir(app_path):
                    continue
                    
                # Look in standard PortableApps locations
                possible_paths = [
                    os.path.join(app_path, "App"),
                    os.path.join(app_path, "App", app_dir),
                    app_path
                ]
                
                for path in possible_paths:
                    if not os.path.exists(path):
                        continue
                        
                    exe_files = [os.path.join(path, f) for f in os.listdir(path) 
                               if f.endswith('.exe') and 'uninstall' not in f.lower()]
                    
                    if exe_files:
                        best_match = find_most_similar_exe(app_dir, exe_files)
                        if best_match:
                            # Store tuple of (program_name, exe_path)
                            portable_apps.append((clean_name(app_dir), best_match))
                            break

    if not portable_apps:
        print("Keine Portable Apps gefunden.")
        return

    term = Terminal()
    current_option = 0
    
    def display_menu():
        print(term.clear)
        print("=== Portable Apps ===\n")
        
        # Calculate layout
        max_width = max(len(name) for name, _ in portable_apps) + 8  # +8 for prefix and padding
        term_width = term.width
        num_columns = max(1, term_width // max_width)
        num_rows = (len(portable_apps) + num_columns - 1) // num_columns
        
        # Display items in grid
        for row in range(num_rows):
            line = ""
            for col in range(num_columns):
                idx = col * num_rows + row
                if idx < len(portable_apps):
                    name, _ = portable_apps[idx]
                    prefix = '>' if idx == current_option else ' '
                    item = f"{prefix} [{idx + 1:2}] {name}"
                    line += item.ljust(max_width)
            print(line)
        print("\n[0] Exit")

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        number_buffer = ""
        while True:
            display_menu()
            if number_buffer:
                print(f"\nCurrent input: {number_buffer}")
            
            key = term.inkey()
            
            # Calculate grid navigation parameters
            max_width = max(len(name) for name, _ in portable_apps) + 8
            term_width = term.width
            num_columns = max(1, term_width // max_width)
            num_rows = (len(portable_apps) + num_columns - 1) // num_columns
            
            if key.isdigit():
                number_buffer += key
            elif key.name == 'KEY_ENTER':
                if number_buffer:
                    num = int(number_buffer)
                    number_buffer = ""
                    if num == 0:
                        break
                    if 1 <= num <= len(portable_apps):
                        app_name, exe_path = portable_apps[num - 1]
                        print(f"\nStarting {app_name}...")
                        subprocess.Popen([exe_path])
                elif 0 <= current_option < len(portable_apps):
                    app_name, exe_path = portable_apps[current_option]
                    print(f"\nStarting {app_name}...")
                    subprocess.Popen([exe_path])
            elif key.name == 'KEY_UP':
                number_buffer = ""
                current_option = max(0, current_option - 1)
            elif key.name == 'KEY_DOWN':
                number_buffer = ""
                current_option = min(len(portable_apps) - 1, current_option + 1)
            elif key.name == 'KEY_LEFT':
                number_buffer = ""
                current_option = max(0, current_option - num_rows)
            elif key.name == 'KEY_RIGHT':
                number_buffer = ""
                current_option = min(len(portable_apps) - 1, current_option + num_rows)
            elif key == 'q':
                break
            elif key.name == 'KEY_BACKSPACE':
                if number_buffer:
                    number_buffer = number_buffer[:-1]


