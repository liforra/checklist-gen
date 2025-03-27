import os
from blessed import Terminal
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox

def portableApps():
    app = PortableAppsGui()
    
class PortableAppsGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Portable Apps")
        self.root.geometry("800x600")  # Larger initial size
        self.root.minsize(600, 400)    # Set minimum size
        
        # Configure dark theme colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.button_bg = "#444444"
        self.button_active_bg = "#555555"
        
        # Configure scrollbar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Vertical.TScrollbar",
                      background=self.button_bg,
                      troughcolor=self.bg_color,
                      width=10)
        
        self.root.configure(bg=self.bg_color)
        
        # Create canvas with scrollbar
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", 
                                     command=self.canvas.yview,
                                     style="Custom.Vertical.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)
        
        # Configure the canvas scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Configure canvas to expand
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure minimum canvas size
        self.canvas.configure(width=780)
        
        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Find and create app buttons
        self.apps = self.find_portable_apps()
        if not self.apps:
            messagebox.showerror("Error", "No portable apps found")
            self.root.destroy()
            return
            
        # Create buttons in a grid
        for i, (name, path) in enumerate(self.apps):
            row = i // 3
            col = i % 3
            btn = tk.Button(
                self.scrollable_frame,
                text=name,
                bg=self.button_bg,
                fg=self.fg_color,
                activebackground=self.button_active_bg,
                activeforeground=self.fg_color,
                width=25,              # Wider buttons
                height=3,              # Taller buttons
                command=lambda p=path: self.run_app(p)
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")  # More padding and stretch
            
        # Configure grid columns to be equal width
        for i in range(3):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def find_portable_apps(self):
        found_apps = []
        
        # Check local apps directory
        apps_dir = "apps"
        if os.path.exists(apps_dir):
            app_paths = {
                "CPU-Z": "cpuz\\cpuz.exe",
                "GPU-Z": "gpuz\\GPU-Z.exe",
                "CrystalDiskInfo": "crystaldiskinfo\\DiskInfo64.exe",
                "CrystalDiskMark": "crystaldiskmark\\DiskMark64.exe",
                "Driver Store Explorer": "dsx\\rapr.exe",
                "NVCleanstall": "nvcleaner\\NVCleanstall.exe",
                "Display Driver Uninstaller": "ddu\\Display Driver Uninstaller.exe",
                "Windows Update Blocker": "wub\\Wub.exe"
            }
            
            for name, rel_path in app_paths.items():
                full_path = os.path.join(apps_dir, rel_path)
                if os.path.exists(full_path):
                    found_apps.append((name, rel_path))
        
        # Check PortableApps directory on all drives
        for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            portable_apps_path = f"{drive}:\\PortableApps"
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
                        
                        exe_files = [f for f in os.listdir(path) 
                                   if f.endswith('.exe') and 'uninstall' not in f.lower()]
                        
                        if exe_files:
                            # Take first exe that's not an uninstaller
                            exe_path = os.path.join(portable_apps_path, app_dir, exe_files[0])
                            found_apps.append((app_dir, exe_path))
                            break
        
        return found_apps
    
    def run_app(self, path):
        if os.path.isabs(path):
            full_path = path
        else:
            full_path = os.path.join("apps", path)
            
        if os.path.exists(full_path):
            response = messagebox.askyesno(
                "Launch Option", 
                "Would you like to copy the program to temp folder before launching?",
                parent=self.root
            )
            
            if response:
                import tempfile
                import shutil
                
                # Create temp directory
                temp_dir = tempfile.mkdtemp()
                app_name = os.path.basename(os.path.dirname(full_path))
                temp_path = os.path.join(temp_dir, app_name)
                
                # Show progress dialog
                progress = CopyProgressDialog(self.root)
                
                # Get total file count
                total_files = sum([len(files) for _, _, files in os.walk(os.path.dirname(full_path))])
                copied_files = 0
                
                def copy_with_progress(src, dst, progress_callback):
                    nonlocal copied_files
                    if not os.path.exists(dst):
                        os.makedirs(dst)
                    for item in os.listdir(src):
                        s = os.path.join(src, item)
                        d = os.path.join(dst, item)
                        if os.path.isfile(s):
                            shutil.copy2(s, d)
                            copied_files += 1
                            progress_callback(int((copied_files / total_files) * 100))
                        else:
                            copy_with_progress(s, d, progress_callback)
                
                # Copy with progress updates
                copy_with_progress(
                    os.path.dirname(full_path),
                    temp_path,
                    lambda p: progress.update(p, f"Copying files... {copied_files}/{total_files}")
                )
                
                progress.close()
                
                # Update path to copied executable
                full_path = os.path.join(temp_path, os.path.basename(full_path))
            
            subprocess.Popen(full_path)
            self.root.destroy()
        else:
            messagebox.showerror("Error", f"Application not found: {path}", parent=self.root)

class CopyProgressDialog:
    def __init__(self, parent, title="Copying..."):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x100")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure dark theme
        self.dialog.configure(bg="#2e2e2e")
        style = ttk.Style()
        style.configure("Custom.Horizontal.TProgressbar",
                      troughcolor="#2e2e2e",
                      background="#444444",
                      thickness=20)
        
        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.label = tk.Label(
            self.dialog,
            text="Copying files...",
            padx=20,
            pady=10,
            bg="#2e2e2e",
            fg="#ffffff"
        )
        self.label.pack()
        
        self.progress = ttk.Progressbar(
            self.dialog,
            length=200,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(padx=20, pady=10)
        
    def update(self, value, text=None):
        if text:
            self.label.config(text=text)
        self.progress['value'] = value
        self.dialog.update()
        
    def close(self):
        self.dialog.destroy()

def portableAppsTerminal():
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
        error_message = ""
        error_time = time.time()
        
        while True:
            display_menu()
            if number_buffer:
                print(f"\nEntering: {number_buffer}")
            if error_message and time.time() - error_time < 2:
                print(f"\nError: {error_message}")
            
            key = term.inkey()
            
            # Calculate grid navigation parameters
            max_width = max(len(name) for name, _ in portable_apps) + 8
            term_width = term.width
            num_columns = max(1, term_width // max_width)
            num_rows = (len(portable_apps) + num_columns - 1) // num_columns
            
            if key.isdigit():
                number_buffer += key
                error_message = ""
            elif key.name == 'KEY_ENTER':
                if number_buffer:
                    try:
                        num = int(number_buffer)
                        number_buffer = ""
                        if num == 0:
                            break
                        if 1 <= num <= len(portable_apps):
                            app_name, exe_path = portable_apps[num - 1]
                            print(f"\nStarting {app_name}...")
                            subprocess.Popen([exe_path])
                            input("\nPress Enter to continue...")  # Wait for user acknowledgment
                        else:
                            error_message = f"Invalid number: {num}"
                            error_time = time.time()
                    except ValueError:
                        error_message = "Invalid number"
                        error_time = time.time()
                else:
                    if 0 <= current_option < len(portable_apps):
                        app_name, exe_path = portable_apps[current_option]
                        print(f"\nStarting {app_name}...")
                        subprocess.Popen([exe_path])
                        input("\nPress Enter to continue...")  # Wait for user acknowledgment
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
            elif key == 'q' or key.name == 'KEY_ESCAPE':
                break
            elif key.name == 'KEY_BACKSPACE':
                if number_buffer:
                    number_buffer = number_buffer[:-1]


