
if [[ $RUNNER_OS !=  "Linux" ]]; then
    export BASHRC=.bash_profile
else
    export BASHRC=.bashrc
fi

if [[ $RUNNER_OS !=  "macOS" ]]; then
    export CONDA_ENV_ROOT=$CONDA
else
    export CONDA_ENV_ROOT=/Users/runner/.conda
fi

if [[ $RUNNER_OS !=  "Windows" ]]; then
    export CONDA_SCRIPT=bin
else
    export CONDA_SCRIPT=Scripts
fi
