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
| Compiling 1/4) submodules/RooFitExtensions  ...
==================================================${NC}\n"
cd submodules/RooFitExtensions
if [ -d "submodules/RooFitExtensions/build" ] ; then
    rm -r submodules/RooFitExtensions/build
fi
mkdir -p build && cd build && rm -fr * && cmake .. && make -j8 && cd ..
source build/setup.sh
cd ${hh_combination_fw_path}


printf "${GREEN}\n
==================================================
| Compiling 2/4) submodules/workspaceCombiner ...
==================================================${NC}\n"
cd submodules/workspaceCombiner
if [ -d "submodules/workspaceCombiner/build" ] ; then
    rm -r submodules/workspaceCombiner/build
fi
mkdir -p build && cd build && rm -fr * && cmake .. && make -j8 && cd ..
cd ${hh_combination_fw_path}


printf "${GREEN}\n
==============================================
| Compiling 3/4) submodules/RooStatTools  ...
==============================================${NC}\n"
cd submodules/RooStatTools
make clean && make
cd ${hh_combination_fw_path}

printf "${GREEN}\n
==============================================
| Compiling 4/4) submodules/DiagnosticTools ...
==============================================${NC}\n"
cd submodules/DiagnosticTools
if [ -d "submodules/DiagnosticTools/build" ] ; then
    rm -r submodules/DiagnosticTools/build
fi
mkdir -p build; cd build; cmake ../; make -j4
cd ${hh_combination_fw_path}







