echo "exporting a new path ======================="
export PATH="$MINICONDA_PATH:$MINICONDA_SUB_PATH:$PATH"
echo "init conda ================================="
$CONDA/$CONDA_SCRIPT/conda init bash
echo "~/$BASHRC =================================="
. ~/$BASHRC
echo "hash -r ===================================="
hash -r
echo "============================================"
echo "CONDA_PYTHON = $CONDA_PYTHON ==============="
echo "============================================"
echo "checking python version ===================="
$CONDA/python --version
echo "conda config --yes ========================="
$CONDA/$CONDA_SCRIPT/conda config --set always_yes yes --set changeps1 no;
echo "conda info -a =============================="
$CONDA/$CONDA_SCRIPT/conda info -a
echo "create test-environment ===================="
$CONDA/$CONDA_SCRIPT/conda env create -n test-environment -f ./tests/environment.${CONDA_PYTHON}.yml
echo "activate test-environment =================="
source activate test-environment
$CONDA/$CONDA_SCRIPT/conda list
