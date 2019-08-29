. set_os.env.sh

echo "activate test-environment =================="
source $CONDA/$CONDA_SCRIPT/activate test-environment
$CONDA/$CONDA_SCRIPT/conda list

$CONDA_ENV_ROOT/envs/test-environment/$CONDA_SCRIPT/py.test --numprocesses=auto tests/
