echo "activate test-environment =================="
source $CONDA/$CONDA_SCRIPT/activate test-environment
$CONDA/$CONDA_SCRIPT/conda list

if [[ $RUNNER_OS !=  "macOS" ]]; then
    CONDA_ENV_ROOT=$CONDA
else
    CONDA_ENV_ROOT=/Users/runner/.conda
fi

$CONDA_ENV_ROOT/envs/test-environment/$CONDA_SCRIPT/py.test --numprocesses=auto tests/
