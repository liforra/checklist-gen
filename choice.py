import platform, subprocess, os




# get user input, as an integer. 1 will open Device Manager, 2 will open the Windows Update Page in Settings, 3 will download "https://liforra.de/keyboardtest.exe" and run it
def get_user_input():
    while True:
        try:
            choice = int(input("Enter 1 to open Device Manager, 2 to open Windows Update, 3 to download and run keyboard test: "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
def open_device_manager():
    # Open Device Manager
    if platform.system() == "Windows":
        subprocess.run(["devmgmt.msc"])
    else:
        print("This function is only available on Windows.")
def open_windows_update():
    # Open Windows Update settings
    if platform.system() == "Windows":
        subprocess.run(["ms-settings:windowsupdate-action"])
    else:
        print("This function is only available on Windows.")
def download_and_run_keyboard_test():
    # Download and run the keyboard test
    url = "https://liforra.de/keyboardtest.exe"
    file_name = "keyboardtest.exe"
    
    try:
        # Download the file
        subprocess.run(["powershell", "-Command", f"(New-Object System.Net.WebClient).DownloadFile('{url}', '{file_name}')"])
        
        # Run the downloaded file
        subprocess.run([file_name])
        
        # Optionally, delete the file after running
        os.remove(file_name)
    except Exception as e:
        print(f"Error downloading or running the keyboard test: {e}")
def main():
    choice = get_user_input()
    if choice == 1:
        open_device_manager()
    elif choice == 2:
        open_windows_update()
    elif choice == 3:
        download_and_run_keyboard_test()
