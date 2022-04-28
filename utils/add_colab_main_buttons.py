import recursively_convert_units as rsc
import find_in_notebook_files as nbf


def main():
    for full_path in rsc.iter_ipynb():
        proc_file(full_path)


def proc_file(full_path:str):
    notebook = nbf.NotebookFile(full_path)
    cells = list(notebook.gen_cells())


if "__main__" == __name__:
    main()
