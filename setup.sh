#!/bin/bash
# Some hacky settings in order to run RooStatTool
# Further clean up should make them set at proper places and time (Rui Zhang)

export HH_COMBINATION_FW_MODE="overwrite" #"skip_exist";
echo $HH_COMBINATION_FW_MODE
unset hh_combination_fw_path
export hh_combination_fw_path="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Setup workspaceCombiner
# Copied from workspaceCombiner/setup.sh (Rui Zhang)
cd submodules/workspaceCombiner
setupATLAS
#lsetup "views LCG_97_ATLAS_1 x86_64-centos7-gcc8-opt"
lsetup "views LCG_98python3 x86_64-centos7-gcc8-opt"

# More memory
ulimit -S -s unlimited

# Greet the user
if [ $_DIRCOMB ]; then
    echo _DIRCOMB is already defined, use a clean shell
    return 1
fi

# speficy the SFRAME base directory, i.e. the directory in which this file lives
export _DIRCOMB=${PWD}

# Modify to describe your directory structure. Default is to use the a structure where
# all directories are below the SFrame base directory specified above
export _BIN_PATH=${_DIRCOMB}/bin
export _LIB_PATH=${_DIRCOMB}/lib

# The Makefiles depend only on the root-config script to use ROOT,
# so make sure that is available
if [[ `which root-config` == "" ]]; then
    echo "Error: ROOT environment doesn't seem to be configured!"
fi

if [[ `root-config --platform` == "macosx" ]]; then
    export DYLD_LIBRARY_PATH=${_LIB_PATH}:${DYLD_LIBRARY_PATH}
else
    export LD_LIBRARY_PATH=${_LIB_PATH}:${LD_LIBRARY_PATH}
fi
export PATH=${_BIN_PATH}:${PATH}
cd ${hh_combination_fw_path}



# Setup RooFitExtensions
cd submodules/RooFitExtensions
if [[ -f build/setup.sh ]]; then
    echo "submodules/RooFitExtensions/build/setup.sh"
    source build/setup.sh
fi
cd ${hh_combination_fw_path}

PYTHONPATH=$PYTHONPATH:${hh_combination_fw_path}/python_modules/:${hh_combination_fw_path}/submodules/RooStatTools/python_modules/
ROOSTATPATH=${hh_combination_fw_path}/submodules/RooStatTools
export ROOSTATPATH

WORKSPACECOMBINER_PATH=${hh_combination_fw_path}/submodules/workspaceCombiner/
export WORKSPACECOMBINER_PATH

LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ROOSTATPATH/lib
ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:${hh_combination_fw_path}/submodules/RooStatTools/inc/:${hh_combination_fw_path}/submodules/RooFitExtensions
export ROOT_INCLUDE_PATH
