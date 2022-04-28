import copy
import os
import urllib.parse as up
from typing import Dict

import bs4

import recursively_convert_units as rsc
import find_in_notebook_files as nbf


def main():
    for full_path in rsc.iter_ipynb():
        proc_file(full_path)


def proc_file(full_path:str):
    notebook = nbf.NotebookFile(full_path)
    cells = list(notebook.gen_cells())

    first_cell = cells[0]
    union_cell = copy.deepcopy(first_cell)
    union_cell.update(get_colab_button_cell(full_path))

    b_write = False

    if first_cell == union_cell:
        # already has the correct button
        pass
    elif has_button_img(first_cell):
        b_write = True
        notebook.overwrite_cell(0, get_colab_button_cell(full_path))
    else:
        b_write = True
        notebook.insert_cell(0, get_colab_button_cell(full_path))

    notebook.validate()

    if b_write:
        notebook.write(full_path)


def is_markdown(cell:Dict) -> bool:
    return "markdown" == cell["cell_type"]


def metadata_correct(cell:Dict) -> bool:
    metadata = cell.get("metadata", {})

    first = ("view-in-github" == metadata.get("id"))
    second = ("text" == metadata.get("colab_type"))

    return (first and second)


def has_button_img(cell:Dict) -> bool:
    result = False

    if is_markdown(cell):
        soup = bs4.BeautifulSoup(cell["source"], features="lxml")
        if soup.img is not None:
            result = soup.img["src"] in get_button_img_tag()

    return result


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


def get_button_img_tag() -> str:
    return '''<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>'''


def get_colab_button_cell(full_path:str, github_id:str="kangwonlee", repo:str="momisp") -> Dict:
    result = {
        "cell_type": "markdown",
        "metadata": {
            "id": "view-in-github",
            "colab_type" : "text",
        },
        "source": (
            f'''<a href="{get_colab_link(full_path, github_id, repo)}" target="_parent">'''
            + get_button_img_tag() +
            '''</a>'''
        ),
    }
    return result


if "__main__" == __name__:
    main()
