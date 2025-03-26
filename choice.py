import os
from pynput import keyboard, mouse

# Track the number of times 'Esc' is pressed
esc_press_count = 0



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
