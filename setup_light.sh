#!/usr/bin/env bash

### -- Save the path of the hh combination framework as an environment variable
hh_combination_fw_path=$(pwd)
export hh_combination_fw_path

### -- Add the hh_combination_fw python modules to PYTHONPATH
hh_combination_fw_pkgs="${hh_combination_fw_path}/python_modules"
echo "Prepending ${hh_combination_fw_pkgs} to PYTHONPATH."
export PYTHONPATH=${hh_combination_fw_pkgs}:$PYTHONPATH
