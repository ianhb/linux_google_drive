import os

# Absolute path of the Google Drive root directory
import time

ROOT_DIR = os.environ["HOME"] + os.path.sep + "google_drive"

def mkdir_if_nexists(path):
    """
    Creates a folder if it doesn't exist
    Args:
        path (): path of the folder to create
    """
    if not os.path.exists(path):
        os.mkdir(path)
        print("Created directory %s" % path)


def absolute_path(path):
    """
    Creates the absolute path of a file within the drive
    Args:
        path (): the relative path of the file

    Returns: the absolute path of the file

    """
    return ROOT_DIR + os.path.sep + path


def datetime_from_string(datetime_string):
    lmt = time.strptime(datetime_string[:-5], "%Y-%m-%dT%H:%M:%S")
    cloud_edit_time = time.mktime(lmt)
    return cloud_edit_time


# Absolute path of the linux_google_drive configurations folder
CONFIG_DIR = absolute_path(".config")
# Absolute path of the pickled directory of the last sync
TREE_FILE = os.path.join(CONFIG_DIR, ".drivetree")
