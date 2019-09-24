# - Note:
# - When sourcing this script the current working directory should be the root directory of the toolbox

hh_combination_fw_path=$(pwd)

### --- Export environment variables --- ###

# - Matplotlib styles directory
export ENV_MATPLOTLIB_STYLES_DIR=${hh_combination_fw_path}/python/matplotlib/styles/

# - Jupyter setup scripts
export ENV_JUPYTER_SETUPS_DIR=${hh_combination_fw_path}/python/jupyter/setups/

hh_combination_fw_pkgs="${hh_combination_fw_path}/python_modules"
UtilTools_pkgs="${hh_combination_fw_path}/submodules/UtilTools/python_modules"
export PYTHONPATH=${hh_combination_fw_pkgs}:$PYTHONPATH
export PYTHONPATH=${UtilTools_pkgs}:$PYTHONPATH
