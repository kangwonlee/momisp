# ref : Francesco Mosconi, Travis + Anaconda + Jupyter, https://github.com/ghego/travis_anaconda_jupyter


import os
import subprocess
import tempfile


def check_kernel_spec():
    # https://jupyter-client.readthedocs.io/en/latest/api/kernelspec.html
    import jupyter_client.kernelspec as jk
    kernel_spec_manager = jk.KernelSpecManager()

    print(kernel_spec_manager.get_all_specs())


def get_tempfile_name(ext='.ipynb'):
    # https://stackoverflow.com/questions/26541416/generate-temporary-file-names-without-creating-actual-file-in-python
    return next(tempfile._get_candidate_names()) + ext


def _exec_notebook(path_filename):
    # http://nbconvert.readthedocs.io/en/latest/execute_api.html
    # ijstokes et al, Command line execution of a jupyter notebook fails in default Anaconda 4.1, https://github.com/Anaconda-Platform/nb_conda_kernels/issues/34
    fout_name = get_tempfile_name()
    args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
            "--ExecutePreprocessor.timeout=1000",
            "--ExecutePreprocessor.kernel_name=python",
            "--output", fout_name, path_filename]
    subprocess.check_call(args)

    path, _ = os.path.split(path_filename)

    if os.path.exists(os.path.join(path, fout_name)):
        os.remove(os.path.join(path, fout_name))


folder_list = (
    'Ch02_Strain', 'Ch03_Torsion', 'Ch04_SFD.BMD', 'Ch05_Stress.in.Beams', 'Ch06_Deflection', 'Ch07_Stat.Indet',
    'Ch08_Stress_Due.To_Combined.Loads', 'Ch10_Column', 'Ch12_SpecialTopic',
)


def test02():
    path = os.path.join(os.pardir, folder_list[0])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test03():
    path = os.path.join(os.pardir, folder_list[1])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test04():
    path = os.path.join(os.pardir, folder_list[2])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test05():
    path = os.path.join(os.pardir, folder_list[3])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test06():
    path = os.path.join(os.pardir, folder_list[4])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test07():
    path = os.path.join(os.pardir, folder_list[5])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test08():
    path = os.path.join(os.pardir, folder_list[6])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test10():
    path = os.path.join(os.pardir, folder_list[7])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))


def test12():
    path = os.path.join(os.pardir, folder_list[8])
    ext = 'ipynb'

    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for filename in filenames:
                if os.path.splitext(filename)[-1].endswith(ext):
                    print('test() : %s %s' % (root, filename))
                    _exec_notebook(os.path.join(root, filename))
