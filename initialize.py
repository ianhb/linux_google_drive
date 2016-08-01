from folder import Folder
from utils import mkdir_if_nexists, ROOT_DIR


def make_root_dir(service):
    """
    Creates a drive root folder and downloads the contents of a user's drive to the root folder
    Args:
        service (): the Drive Service to connect to Drive with
    """
    mkdir_if_nexists(ROOT_DIR)
    root = Folder('root', 'root', ROOT_DIR, None, service=service)

    for child in root.get_children():
        child.get(service)
