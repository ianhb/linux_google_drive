import os

from folder import Folder


def compare_tree_to_local(root):
    # type: (Folder) -> List[File]
    local_children = os.listdir(root.get_path())
    tree_children = root.get_children()


def compare_tree_to_remote(root):
    tree_children = root.get_children()
