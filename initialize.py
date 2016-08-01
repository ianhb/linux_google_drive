import cPickle

from folder import Folder
from utils import mkdir_if_nexists, ROOT_DIR, TREE_FILE, CONFIG_DIR


def make_root_dir(service):
    """
    Creates a drive root folder and downloads the contents of a user's drive to the root folder
    Args:
        service (): the Drive Service to connect to Drive with
    """
    mkdir_if_nexists(ROOT_DIR)
    mkdir_if_nexists(CONFIG_DIR)
    root = Folder('root', 'root', ROOT_DIR, None, service=service)

    with open(TREE_FILE, 'w') as tree_file:
        cPickle.dump(root, tree_file)
