import os
import json
import shutil
from glob import glob
from pathlib import Path
from datetime import datetime

def get_timestamp() -> str:
    """
    Returns the current timestamp as a string.

    Returns:
    str: The current timestamp as a string of the integer number of seconds since the Unix epoch.
    """
    return str(int(datetime.now().timestamp()))

def make_path(extension: str) -> str:
    """
    Constructs an absolute path from a given relative extension.

    Parameters:
    extension (str): The relative path or extension to append to the project root path.

    Returns:
    str: The absolute path of the specified extension within the project directory.
    """
    project_path = Path(Path(__file__).resolve().parent)
    return str(project_path / extension)

def load_config() -> dict:
    """
    Loads the configuration settings from a JSON file.

    Returns:
    dict: The dictionary containing configuration settings from the 'config.json' file.
    """
    with open(make_path(extension="config.json"), "r") as f:
        dct = json.load(f)
    return dct

def delete_folder(extension: str) -> None:
    """
    Deletes a folder and all of its contents based on the given path extension.

    Parameters:
    extension (str): The relative path of the folder to be deleted.
    """
    folder_path = make_path(extension=extension)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        
def make_folder(extension: str) -> None:
    """
    Creates a folder at the given path extension if it does not already exist.

    Parameters:
    extension (str): The relative path of the folder to create.
    """
    folder_path = make_path(extension=extension)
    os.makedirs(folder_path, exist_ok=True)

def get_local_database_path() -> str:
    """
    Retrieves the absolute path to the local database folder.

    Returns:
    str: The absolute path to the 'database' folder.
    """
    return make_path("database")        
        
def get_path_list(extension: str, datatype: str) -> list:
    """
    Returns a list of file paths in the specified folder with the given file extension.

    Parameters:
    extension (str): The relative path to the folder.
    datatype (str): The file extension/type to search for (e.g., 'json', 'txt').

    Returns:
    list: A list of file paths matching the specified file type.
    """
    return glob(os.path.join(make_path(extension=extension), f"*.{datatype}"))

def clear_database() -> None:
    """
    Deletes all subfolders in the local database folder except for the two most recent subfolders.
    Assumes subfolders are named as timestamps to determine recency.
    """
    folder_path = get_local_database_path()
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    subfolders.sort()

    if len(subfolders) > 2:
        folders_to_remove = subfolders[:-2]

        for folder in folders_to_remove:
            folder_path_to_remove = os.path.join(folder_path, folder)
            shutil.rmtree(folder_path_to_remove)

def save_list_as_txt(file_path: str, data: list) -> None:
    """
    Saves a list of strings as a text file, with each string on a new line.

    Parameters:
    file_path (str): The path where the text file will be saved.
    data (list): The list of strings to save to the file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item}\n")
            
def read_txt_as_list_of_strings(file_path: str) -> list:
    """
    Reads a text file line by line and returns its contents as a list of strings.

    Parameters:
    file_path (str): The path to the text file.

    Returns:
    list: A list where each element is a line from the text file (with newline characters stripped).
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    lines = [line.strip() for line in lines]
    
    return lines

def add_key_to_json(file_path: str, new_key: str, new_value) -> None:
    """
    Reads a JSON file, adds a new key-value pair, and writes the modified JSON back to the file.

    Parameters:
    file_path (str): The path to the JSON file.
    new_key (str): The key to add to the JSON object.
    new_value: The value associated with the new key.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    data[new_key] = new_value
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_most_recent_subfolders() -> dict:
    """
    Finds the most recent subfolders in the local database folder and returns a dictionary of subfolder names and their absolute paths.

    Returns:
    dict: A dictionary where the keys are subfolder names and the values are their absolute paths.
    """
    folder_path = get_local_database_path()
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    subfolders.sort(reverse=True)
    folder_path = os.path.join(folder_path, subfolders[0])
    subfolders = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    return {path.split("/")[-1]: path for path in subfolders}
