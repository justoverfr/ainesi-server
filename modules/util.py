import json
import datetime
import os


def open_file(filepath):
    """
    Open a file and return its content.

    Args:
        filepath (str): Path of the file

    Returns:
        str: Content of the file
    """
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(file_name, content=None, folder_path='', create_folder=True):
    """
    Save a file with the given content.

    Args:
        file_name (str): The name of the file to save.
        content (str, optional): The content of the file to save.
        folder_path (str, optional): The path of the folder in which to save the file.
        create_folder (bool, optional): Whether to create the folder if it does not exist.
    """
    if (create_folder and not os.path.exists(folder_path)):
        os.makedirs(folder_path)

    file_full_path = os.path.join(folder_path, file_name)

    with open(file_full_path, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def load_json(filepath):
    """
    Load a json file and return its content.

    Args:
        filepath (str): Path of the file

    Returns:
        dict: Content of the file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)
    except Exception as oops:
        return None


def save_json(file_name, data=None, folder_path='', create_folder=True):
    """
    Save a json file with the given data.

    Args:
        file_name (str): The name of the file to save.
        data (dict, optional): The data to save in the json file.
        folder_path (str, optional): The path of the folder in which to save the file.
        create_folder (bool, optional): Whether to create the folder if it does not exist.
    """
    if create_folder and not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_full_path = os.path.join(folder_path, file_name)

    with open(file_full_path, 'w') as file:
        json.dump(data, file, indent=4)

    return file_full_path


def get_time_string(unix_time):
    """
    Convert Unix timestamp to datetime string.

    Args:
        unix_time (int): Unix timestamp

    Returns:
        str: date in the following format: Monday, January 01, 2000 at 12:00AM UTC
    """
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")
