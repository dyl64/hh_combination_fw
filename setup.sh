#!/usr/bin/env bash

# Further clean up should make them set at proper places and time (Rui Zhang)

export HH_COMBINATION_FW_MODE="overwrite" #"skip_exist";
echo $HH_COMBINATION_FW_MODE

# check if inside SWAN setup
if [[ -z "${SWAN_HOME}" ]] && [[ -z "${USER_ENV_SCRIPT}" ]]; then
    if [ "$#" -ge 1 ];
    then
        EnvironmentName=$1
    else
        EnvironmentName="102b"
    fi
    
    SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
      DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
      SOURCE="$(readlink "$SOURCE")"
      [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done

    export hh_combination_fw_path="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

    # Copied from workspaceCombiner/setup.sh (Rui Zhang)
    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase # use your path
    source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
    if [[ "$EnvironmentName" == '98' ]]; then
        echo 'setup LCG_98python3'
        lsetup "views LCG_98python3 x86_64-centos7-gcc8-opt"
    elif [[ "$EnvironmentName" == "100" ]]; then
        echo 'setup LCG_100'
        lsetup "views LCG_100 x86_64-centos7-gcc8-opt"
    elif [[ "$EnvironmentName" == "101" ]]; then
        echo 'setup LCG_101, ROOT 6.24/06'
        lsetup "views LCG_101 x86_64-centos7-gcc8-opt"
    elif [[ "$EnvironmentName" == "102" ]]; then
        echo 'setup LCG_102, ROOT 6.26/04'
        lsetup "views LCG_102 x86_64-centos7-gcc11-opt"
    elif [[ "$EnvironmentName" == "102b" ]]; then
        echo 'setup LCG_102b, ROOT 6.26/08'
        kernel_info=$(uname -a)
        if [[ $kernel_info =~ el7 ]] && [[ $kernel_info =~ x86_64 ]]; then
            lsetup "views LCG_102b x86_64-centos7-gcc11-opt"
        elif [[ $kernel_info =~ el9 ]] && [[ $kernel_info =~ x86_64 ]]; then
            lsetup "views LCG_102b x86_64-centos9-gcc11-opt"
        else
            echo "Please define the LCG version for your system in setup.sh"
            echo "Your kernel_info is: $kernel_info"
            echo "If this is running on gitlab-CI runner, centos7 will be setup"
            lsetup "views LCG_102b x86_64-centos7-gcc11-opt"
        fi
    elif [[ "$EnvironmentName" == "103" ]]; then
        echo 'setup LCG_103, ROOT 6.28/00'
        lsetup "views LCG_103 x86_64-centos7-gcc11-opt"
    elif [[ "$EnvironmentName" == "104c" ]]; then
        echo 'setup LCG_104c, ROOT 6.28/10'
        lsetup "views LCG_104c_ATLAS_2 x86_64-centos7-gcc11-opt"
        lsetup cmake
    else
        echo 'Specify a relase number for LCG, default LCG_102b'
        echo 'source setup.sh [98|100|101|102|102b|103|104c]'
        return
    fi
    
else
  EnvironmentName="swan"
  export hh_combination_fw_path=$(dirname "$USER_ENV_SCRIPT")
fi

# More memory
ulimit -S -s unlimited

# Greet the user
if [ $_DIRCOMB ]; then
    echo _DIRCOMB is already defined, use a clean shell
    return 0
fi

export _DIRCOMB=$hh_combination_fw_path

# The Makefiles depend only on the root-config script to use ROOT,
# so make sure that is available
if [[ `which root-config` == "" ]]; then
    echo "Error: ROOT environment doesn't seem to be configured!"
fi

# TODO: remove dependence on workspaceCombiner
# speficy the SFRAME base directory, i.e. the directory in which this file lives

WORKSPACECOMBINER_PATH=${hh_combination_fw_path}/submodules/workspaceCombiner/
export WORKSPACECOMBINER_PATH
# Modify to describe your directory structure. Default is to use the a structure where
# all directories are below the SFrame base directory specified above
export _BIN_PATH=${WORKSPACECOMBINER_PATH}/build
export _LIB_PATH=${WORKSPACECOMBINER_PATH}/build

if [[ `root-config --platform` == "macosx" ]]; then
    export DYLD_LIBRARY_PATH=${_LIB_PATH}:${DYLD_LIBRARY_PATH}
else
    export LD_LIBRARY_PATH=${_LIB_PATH}:${LD_LIBRARY_PATH}
fi

export PATH=${_BIN_PATH}:${PATH}
cd ${hh_combination_fw_path}

# Setup RooFitExtensions
cd ${hh_combination_fw_path}/submodules/RooFitExtensions

if [[ -f build/setup.sh ]]; then
    echo "submodules/RooFitExtensions/build/setup.sh"
    source build/setup.sh
fi

export ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:${hh_combination_fw_path}/submodules/RooFitExtensions

# setup hh combination fw
export PYTHONPATH=$PYTHONPATH:${hh_combination_fw_path}
export PATH=${hh_combination_fw_path}/bin:$PATH

# setup quickstats
export PATH=${hh_combination_fw_path}/submodules/quickstats/bin:$PATH
export PYTHONPATH=${hh_combination_fw_path}/submodules/quickstats:$PYTHONPATH

cd ${hh_combination_fw_path}

# jupyter notebook --port 8933 > jupyter.log 2>&1 &

unset EnvironmentName
