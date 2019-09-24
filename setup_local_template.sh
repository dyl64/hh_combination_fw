#!/usr/bin/env bash
    
# - Set the path to `workspaceCombiner` package here (you need to build it before)
# - See: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner
if [[ -z ${WORKSPACECOMBINER_SET} ]]; then
    export WORKSPACECOMBINER_SET=0
    export WORKSPACECOMBINER_PATH="PATH_TO_WSCOMBINER"
    echo "WORKSPACECOMBINER_SET is false, setting workspaceCombiner."
    echo "WORKSPACECOMBINER_PATH: ${WORKSPACECOMBINER_PATH}"
    WORKSPACECOMBINER_SETUP_SCRIPT=${WORKSPACECOMBINER_PATH}/setup.sh
    source_if_exists ${WORKSPACECOMBINER_SETUP_SCRIPT}
    export WORKSPACECOMBINER_LIB="${WORKSPACECOMBINER_PATH}/lib/"
    export LD_LIBRARY_PATH=${WORKSPACECOMBINER_LIB}:${LD_LIBRARY_PATH}
fi

# - Source HSG7, ROOT 6 version from cvmfs
if [[ -z ${ROOT_SET} ]]; then
    echo "ROOT not set up yet, sourcing ${ROOT}"
    export ROOT_SET=0
    setupATLAS
    lsetup "root 6.04.16-HiggsComb-x86_64-slc6-gcc49-opt"
fi