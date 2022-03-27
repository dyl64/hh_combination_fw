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
    source setup_H_HH_comb.sh
fi

printf "${GREEN}\n
==================================================
| Compiling 1/2) submodules/RooFitExtensions  ...
==================================================${NC}\n"
cd submodules/RooFitExtensions
if [ -d "submodules/RooFitExtensions/build" ] ; then
    rm -r submodules/RooFitExtensions/build
fi
mkdir -p build && cd build && rm -fr * && cmake .. && make -j8 && cd ..
source build/setup.sh
cd ${hh_combination_fw_path}

printf "${GREEN}\n
==============================================
| Compiling 2/2) submodules/quickstats ...
==============================================${NC}\n"
quickstats compile

