#!/usr/bin/env bash

### -- Save the path of the hh combination framework as an environment variable
hh_combination_fw_path=$(pwd)
export hh_combination_fw_path

source_if_exists()
{
    if [ -f $1 ]
    then
        echo "$1 exists, sourcing..."
        source $1
    else
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "!!! ERROR: $1 not found !!!!"
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		  return 1
    fi
}

source_if_exists $hh_combination_fw_path/setup_local.sh

################################################
### --- Sourcing submodule setup scripts --- ###
################################################

for dir in $hh_combination_fw_path/submodules/*
do
	cd ${dir}
	setup_script="setup.sh"
	if [ -f "${setup_script}" ]
	then
      last_dir=$(basename $dir)
		echo "### --- Submodule ${last_dir}."
		source_if_exists ${setup_script}
	 else
      echo "${setup_script} not found."
	fi
	cd ${hh_combination_fw_path}
done

cd ${hh_combination_fw_path}

### -- Add the hh_combination_fw python modules to PYTHONPATH
hh_combination_fw_pkgs="${hh_combination_fw_path}/python_modules"
echo "Prepending ${hh_combination_fw_pkgs} to PYTHONPATH."
export PYTHONPATH=${hh_combination_fw_pkgs}:$PYTHONPATH
