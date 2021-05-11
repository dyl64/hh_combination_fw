#!/bin/bash
# Some hacky settings in order to run RooStatTool
# Further clean up should make them set at proper places and time (Rui Zhang)

# set up environmental paths
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done

DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

export hh_combination_fw_path=${DIR}

# Setup workspaceCombiner
# Copied from workspaceCombiner/setup.sh (Rui Zhang)
cd $DIR/submodules/workspaceCombiner

# More memory
ulimit -S -s unlimited

# Greet the user
if [ $_DIRCOMB ]; then
    echo _DIRCOMB is already defined, use a clean shell
    return 1
fi

# speficy the SFRAME base directory, i.e. the directory in which this file lives
export _DIRCOMB=${DIR}

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
cd $DIR/submodules/RooFitExtensions
if [[ -f build/setup.sh ]]; then
    echo "submodules/RooFitExtensions/build/setup.sh"
    source build/setup.sh
fi
cd ${hh_combination_fw_path}

export PYTHONPATH=$PYTHONPATH:${hh_combination_fw_path}/python_modules/:${hh_combination_fw_path}/submodules/RooStatTools/python_modules/
export ROOSTATPATH=${hh_combination_fw_path}/submodules/RooStatTools

export WORKSPACECOMBINER_PATH=${hh_combination_fw_path}/submodules/workspaceCombiner/

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ROOSTATPATH/lib
export ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:${hh_combination_fw_path}/submodules/RooStatTools/inc/
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/sft.cern.ch/lcg/views/LCG_98/x86_64-centos7-gcc8-opt/lib
