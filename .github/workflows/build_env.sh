echo "exporting a new path ======================="
export PATH="$MINICONDA_PATH:$MINICONDA_SUB_PATH:$PATH"
echo "init conda ================================="
conda init bash
echo "~/$BASHRC =================================="
. ~/$BASHRC
echo "hash -r ===================================="
hash -r
echo "============================================"
echo "CONDA_PYTHON = $CONDA_PYTHON ==============="
echo "============================================"
echo "checking python version ===================="
python --version
echo "conda config --yes ========================="
conda config --set always_yes yes --set changeps1 no;
echo "conda info -a =============================="
conda info -a
echo "create test-environment ===================="
conda env create -n test-environment -f ./tests/environment.${CONDA_PYTHON}.yml
echo "activate test-environment =================="
source activate test-environment
conda list
