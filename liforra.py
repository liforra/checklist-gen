import os

def find_dir(directory_name):
    """
    Searches for a directory in the root of all available drives and outputs the drives that contain it.

    Args:
        directory_name (str): The name of the directory to search for.

    Returns:
        list: A list of drives that contain the specified directory.
    """
    drives_with_directory = []
    
    # Get all available drives (Windows-specific)
    drives = [f"{chr(drive)}:\\" for drive in range(65, 91) if os.path.exists(f"{chr(drive)}:\\")]
    
    for drive in drives:
        directory_path = os.path.join(drive, directory_name)
        if os.path.isdir(directory_path):
            drives_with_directory.append(drive)
    
    return drives_with_directory