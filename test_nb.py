# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter


import os
import subprocess
import tempfile


def _exec_notebook(path):
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=1000",
                "--output", fout.name, path]
        subprocess.check_call(args)


def test():
    _exec_notebook(os.path.join('Ch04', 'ex04.001.SFD.BMD.numerical.arrows.ipynb'))
