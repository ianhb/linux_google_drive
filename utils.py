import os

ROOT_DIR = os.environ["HOME"] + os.path.sep + "google_drive"


def mkdir_if_nexists(path):
    """
    Creates a folder if it doesn't exist
    Args:
        path (): path of the folder to create
    """
    if not os.path.exists(path):
        os.mkdir(path)
        print("Created dir %s" % path)


def absolute_path(path):
    """
    Creates the absolute path of a file within the drive
    Args:
        path (): the relative path of the file

    Returns: the absolute path of the file

    """
    return ROOT_DIR + os.path.sep + path
