which py.test
if [[ "RUNNER_OS" !=  "macOS" ]]; then
    CONDA_ENV_ROOT=$CONDA
else
    CONDA_ENV_ROOT=/Users/runner/.conda
fi
echo $CONDA_ENV_ROOT/envs/test-environment/$CONDA_SCRIPT/py.test
$CONDA_ENV_ROOT/envs/test-environment/$CONDA_SCRIPT/py.test --numprocesses=auto tests/
