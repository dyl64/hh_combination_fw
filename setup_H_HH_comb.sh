#!/bin/bash
# Further clean up should make them set at proper places and time (Rui Zhang)

export HH_COMBINATION_FW_MODE="overwrite" #"skip_exist";
echo $HH_COMBINATION_FW_MODE
unset hh_combination_fw_path
export hh_combination_fw_path="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Setup workspaceCombiner
# Copied from workspaceCombiner/setup.sh (Rui Zhang)
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase # use your path
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
echo 'setup LCG_102'
lsetup "views LCG_102rc1 x86_64-centos7-gcc11-opt"

# More memory
ulimit -S -s unlimited

# Setup RooFitExtensions
cd submodules/RooFitExtensions
if [[ -f build/setup.sh ]]; then
    echo "submodules/RooFitExtensions/build/setup.sh"
    source build/setup.sh
fi
cd ${hh_combination_fw_path}

PYTHONPATH=$PYTHONPATH:${hh_combination_fw_path}/python_modules/

#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ROOSTATPATH/lib
ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:${hh_combination_fw_path}/submodules/RooFitExtensions
export LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH

export PATH=${hh_combination_fw_path}/bin:$PATH


# setup quickstats
export PATH=${hh_combination_fw_path}/submodules/quickstats/bin:$PATH
export PYTHONPATH=${hh_combination_fw_path}/submodules/quickstats:$PYTHONPATH
