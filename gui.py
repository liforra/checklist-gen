import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import win32gui
import win32con

def hideConsole():
    try:
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    except:
        pass

class DarkModeApp:
    def __init__(self, root):
        from main import menu_options, start_check_threads, threads_complete
        
        self.root = root
        self.root.title("System Tools")
        self.root.geometry("800x600")
        
        # Configure dark theme colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.button_bg = "#444444"
        self.button_active_bg = "#555555"
        self.entry_bg = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure fonts
        self.default_font = tkfont.Font(family="Arial", size=11)
        self.output_font = tkfont.Font(family="Consolas", size=10)
        
        self.root.option_add("*Font", self.default_font)
        
        # Create output area first
        self.output_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(
            self.output_frame,
            bg="#2a2a2a",  # Slightly darker than background
            fg="#cccccc",  # Slightly dimmer text
            height=10,
            state=tk.NORMAL,  # Keep it normal to avoid flashing
            font=self.output_font,
            relief=tk.FLAT,  # Remove border
            padx=10,
            pady=10,
            cursor="arrow"  # Hide text cursor
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Disable text editing while keeping normal state
        self.output_text.bind("<Key>", lambda e: "break")
        
        # Initialize threads without waiting
        start_check_threads()
        
        # Start periodic check for hardware info
        self.check_hardware_info()
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        self.buttons_frame.pack(fill=tk.BOTH)
        
        # Create buttons dynamically from menu_options
        row = 0
        col = 0
        for option_num, option_text in menu_options:
            if not (800 <= option_num <= 999) and option_num != 0:  # Skip hidden options and exit
                btn = tk.Button(
                    self.buttons_frame,
                    text=f"{option_text} ({option_num})",
                    bg=self.button_bg,
                    fg=self.fg_color,
                    activebackground=self.button_active_bg,
                    activeforeground=self.fg_color,
                    padx=10,
                    pady=5,
                    command=lambda num=option_num: self.run_option(num)
                )
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
                col += 1
                if col > 2:  # 3 buttons per row
                    col = 0
                    row += 1
        
        # Configure grid columns to be equal width
        for i in range(3):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Create number input frame
        self.input_frame = tk.Frame(self.root, bg=self.bg_color, padx=20)
        self.input_frame.pack(fill=tk.X)
        
        # Add number input field
        self.number_label = tk.Label(
            self.input_frame,
            text="Enter option number:",
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.number_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.number_entry = tk.Entry(
            self.input_frame,
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color
        )
        self.number_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.number_entry.bind('<Return>', lambda e: self.go_button_clicked())
        
        self.go_button = tk.Button(
            self.input_frame,
            text="Go",
            bg=self.button_bg,
            fg=self.fg_color,
            activebackground=self.button_active_bg,
            activeforeground=self.fg_color,
            command=self.go_button_clicked
        )
        self.go_button.pack(side=tk.LEFT)
    
    def check_hardware_info(self):
        from main import get_thread_status, cpu, cpu_freq, gpu, battery_health, product, serial
        from main import ram_amount, ram_freq, ram_type, ram_slots, ram_stick_type, drive_size, drive_type
        from main import windows_ed, windows_ver, activation, last_update, users, bitlocker_status, domain_info
        
        info = "Hardware Information:\n"
        
        # Hardware info (Thread 1)
        if cpu:
            info += f"Product: {product or 'Not ready'}; Serial Nr: {serial or 'Not ready'}\n"
            info += f"CPU: {cpu or 'Not ready'}; Battery Health: {battery_health or 'Not ready'}%\n"
            info += f"GPU: {gpu or 'Not ready'}\n"
        
        # Memory info (Thread 2)
        if ram_amount:
            info += f"RAM: {ram_amount or 'Not ready'} GB; {ram_freq or 'Not ready'} MHz; {ram_type or 'Not ready'};\n"
            info += f"Slots: {ram_slots or 'Not ready'}; RAM-Type: {ram_stick_type or 'Not ready'}\n"
            info += f"Main Drive: {drive_size or 'Not ready'} GB; {drive_type or 'Not ready'}\n"
        
        # System info (Thread 3)
        if windows_ed:
            info += f"OS: {windows_ed or 'Not ready'}; Version: {windows_ver or 'Not ready'};\n"
            info += f"Activation: {activation or 'Not ready'}\n"
            info += f"Last Update: {last_update or 'Not ready'}\n"
            info += f"Users: {users or 'Not ready'}\n"
            info += f"Bitlocker: {bitlocker_status or 'Not ready'}\n"
            info += f"Domain: {domain_info or 'Not ready'}\n"
        
        if not (cpu or ram_amount or windows_ed):
            info += "Gathering system information...\n"
            
        self.update_output(info)
        
        if not get_thread_status():
            self.root.after(1000, self.check_hardware_info)  # Check again in 1 second
    
    def go_button_clicked(self):
        try:
            option_num = int(self.number_entry.get())
            self.run_option(option_num)
        except ValueError:
            self.update_output("Please enter a valid number")
    
    def run_option(self, option_num):
        from main import run
        if option_num in [5, 7]:  # Raw input test options
            RawInputWindow()
        else:
            self.update_output(f"Running option {option_num}...")
            run(option_num)
    
    def update_output(self, message):
        current_text = self.output_text.get("1.0", tk.END).strip()
        new_text = message.strip()
        if current_text != new_text:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, message)

class RawInputWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Raw Input Test")
        self.root.geometry("600x400")
        
        self.output_text = tk.Text(
            self.root,
            bg="#333333",
            fg="#ffffff",
            font=("Consolas", 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.setup_listeners()
        
    def setup_listeners(self):
        from pynput import keyboard, mouse
        
        def on_key_press(key):
            try:
                self.log(f"Key pressed: {key.char}")
            except AttributeError:
                self.log(f"Special key pressed: {key}")
                
        def on_key_release(key):
            self.log(f"Key released: {key}")
            
        def on_click(x, y, button, pressed):
            state = "pressed" if pressed else "released"
            self.log(f"Mouse {state} at ({x}, {y}) with {button}")
            
        def on_scroll(x, y, dx, dy):
            self.log(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")
            
        self.keyboard_listener = keyboard.Listener(
            on_press=on_key_press,
            on_release=on_key_release
        )
        self.mouse_listener = mouse.Listener(
            on_click=on_click,
            on_scroll=on_scroll
        )
        
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        
    def on_close(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        self.root.destroy()

def main():
    hideConsole()
    root = tk.Tk()
    app = DarkModeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
