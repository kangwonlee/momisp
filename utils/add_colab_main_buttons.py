import os
import urllib.parse as up
from typing import Dict


import recursively_convert_units as rsc
import find_in_notebook_files as nbf


def main():
    for full_path in rsc.iter_ipynb():
        proc_file(full_path)


def proc_file(full_path:str):
    notebook = nbf.NotebookFile(full_path)
    cells = list(notebook.gen_cells())


def is_markdown(cell:Dict) -> bool:
    return "markdown" == cell["cell_type"]


def metadata_correct(cell:Dict) -> bool:
    metadata = cell.get("metadata", {})

    first = ("view-in-github" == metadata.get("id"))
    second = ("text" == metadata.get("colab_type"))

    return (first and second)


def get_proj_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def get_rel_path(full_path:str) -> str:
    return os.path.relpath(full_path, get_proj_root())


def get_colab_link(full_path:str, github_id:str="kangwonlee", repo:str="momisp") -> str:
    rel_path = get_rel_path(full_path)
    rel_path_list = rel_path.split(os.sep)
    result = up.urlunparse(
        (
            "https",
            "colab.research.google.com",
            '/'.join(
                ["github", github_id, repo, "blob", "main"] + rel_path_list,
            ),
            None,
            None,
            None,
        )
    )
    return result


def get_colab_button_cell(full_path:str, github_id:str="kangwonlee", repo:str="momisp") -> Dict:
    result = {
        "cell_type": "markdown",
        "metadata": {
            "id": "view-in-github",
            "colab_type" : "text",
        },
        "source": (
            f'''<a href="{get_colab_link(full_path, github_id, repo)}" target="_parent">'''
            '''<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>'''
            '''</a>'''
        ),
    }
    return result


if "__main__" == __name__:
    main()
