import os
from pynput import keyboard, mouse

# Track the number of times 'Esc' is pressed
esc_press_count = 0

def raw_input_test():
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


def run_CrystalDiskMark():
    # Iterate through all drives (Windows-specific)
    for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_path = f"{drive}:\\"
        crystal_disk_path = os.path.join(drive_path, "PortableApps", "CrystalDiskMarkPortable", "CrystalDiskMarkPortable.exe")
        if os.path.exists(crystal_disk_path):
            print(f"Found CrystalDiskMark at {crystal_disk_path}. Launching...")
            os.startfile(crystal_disk_path)  # Launch the executable
            return
    print("CrystalDiskMarkPortable.exe not found on any drive.")


def check_number(number):
    match number:
        case 1:
            # Open Device Manager in Windows
            os.system("start devmgmt.msc")
        case 2:
            # Open Windows Update Page in Settings
            os.system("start ms-settings:windowsupdate")
        case 3:
            # Download and run the keyboard test program
            os.system("start https://liforra.de/keyboardtest.exe")
        case 4:
            # Run Battery Report
            os.system("start cmd /c powercfg /batteryreport")
        case 5:
            # Run Raw Input Test
            raw_input_test()
        case 6:
            # CrystalDiskMark
            run_CrystalDiskMark()
        case 100:
            #Run Massgrave Activation Scripts
            os.system("powershell -c \"irm https://get.activated.win | iex\"")
        case _:
            print(f"{number} hat leider noch keine Funktion. Bitte eine andere Zahl eingeben.")

while True:
    userinput = input("Bitte eine Zahl eingeben (1 = Geräte-Manager, 2 = Windows Update, 3 = Tastaturtest, 4 = Akku Report, 5 = Raw Input Test, 6 = CrystalDiskMark, q = quit)\n")
    userinput = userinput.strip()  # Remove leading/trailing whitespace
    try:
        number = int(userinput)
        check_number(number)
    except ValueError:
        if userinput == "q" or userinput == "Q":
            print("Exiting the program.")
            exit()
        else:
            print("Invalid input. Please enter a number or 'q' to quit.")
            continue



# get user input, as an integer. 1 will open Device Manager, 2 will open the Windows Update Page in Settings, 3 will download "https://liforra.de/keyboardtest.exe" and run it
