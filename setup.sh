#!/bin/bash
# Further clean up should make them set at proper places and time (Rui Zhang)

export HH_COMBINATION_FW_MODE="overwrite" #"skip_exist";
echo $HH_COMBINATION_FW_MODE
unset hh_combination_fw_path
export hh_combination_fw_path="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Setup workspaceCombiner
# Copied from workspaceCombiner/setup.sh (Rui Zhang)
cd submodules/workspaceCombiner
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase # use your path
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
if [[ $1 == '98' ]]; then
    echo 'setup LCG_98python3'
    lsetup "views LCG_98python3 x86_64-centos7-gcc8-opt"
elif [[ $1 == '100' ]]; then
    echo 'setup LCG_100'
    lsetup "views LCG_100 x86_64-centos7-gcc8-opt"
elif [[ $1 == '101' ]] || [[ -z $1 ]]; then
    echo 'setup LCG_101'
    lsetup "views LCG_101 x86_64-centos7-gcc8-opt"
else
    echo 'Specify a relase number for LCG, default LCG_101'
    echo 'source setup.sh [98|100|101]'
    return
fi
# More memory
ulimit -S -s unlimited

# Greet the user
if [ $_DIRCOMB ]; then
    echo _DIRCOMB is already defined, use a clean shell
    return 0
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

# Copy from workspaceCombiner/setup.sh done


# Setup RooFitExtensions
cd submodules/RooFitExtensions
if [[ -f build/setup.sh ]]; then
    echo "submodules/RooFitExtensions/build/setup.sh"
    source build/setup.sh
fi
cd ${hh_combination_fw_path}

PYTHONPATH=$PYTHONPATH:${hh_combination_fw_path}/python_modules/

WORKSPACECOMBINER_PATH=${hh_combination_fw_path}/submodules/workspaceCombiner/
export WORKSPACECOMBINER_PATH

#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ROOSTATPATH/lib
ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:${hh_combination_fw_path}/submodules/RooFitExtensions
export LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH

export PATH=${hh_combination_fw_path}/bin:$PATH


# setup quickstats
export PATH=${hh_combination_fw_path}/submodules/quickstats/bin:$PATH
export PYTHONPATH=${hh_combination_fw_path}/submodules/quickstats:$PYTHONPATH
