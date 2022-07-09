#!/bin/bash
# This is not to compile hh_combination_fw
# But a wrapper to compile submodules (Rui Zhang)

GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [[ ! -v hh_combination_fw_path ]]; then
    printf "${GREEN}\n
==================================
| Sourcing   source setup.sh  ...
==================================${NC}\n"
    source setup.sh
fi

printf "${GREEN}\n
==================================================
| Compiling 1/3) submodules/RooFitExtensions  ...
==================================================${NC}\n"
cd ${hh_combination_fw_path}
if [ -d "submodules/RooFitExtensions/build" ] ; then
    rm -fr submodules/RooFitExtensions/build
fi
cd submodules/RooFitExtensions
mkdir -p build && cd build && rm -fr * && cmake .. && make -j8 && cd ..
source build/setup.sh
cd ${hh_combination_fw_path}

printf "${GREEN}\n
==================================================
| Compiling 2/3) submodules/workspaceCombiner ...
==================================================${NC}\n"
cd ${hh_combination_fw_path}
if [ -d "submodules/workspaceCombiner/build" ] ; then
    rm -fr submodules/workspaceCombiner/build
fi
if [ -d "submodules/workspaceCombiner/lib" ] ; then
    rm -fr submodules/workspaceCombiner/lib/*
fi
cd submodules/workspaceCombiner
mkdir -p build && cd build && rm -fr * && cmake .. && make -j8 && cd ..
cd ${hh_combination_fw_path}

printf "${GREEN}\n
==============================================
| Compiling 3/3) submodules/quickstats ...
==============================================${NC}\n"
quickstats compile

