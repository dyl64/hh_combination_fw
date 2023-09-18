#!/usr/bin/env bash
# This is not to compile hh_combination_fw
# But a wrapper to compile submodules (Rui Zhang)

GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [[ -z "${hh_combination_fw_path-}" ]]; then
    printf "${GREEN}\n
==================================
| Sourcing   source setup.sh  ...
==================================${NC}\n"
    if [[ -z $1 ]]; then
        source setup.sh
    else
        source setup.sh $1
    fi
fi

printf "${GREEN}\n
==================================================
| Compiling 1/2) submodules/RooFitExtensions  ...
==================================================${NC}\n"
cd ${hh_combination_fw_path}
if [ -d "submodules/RooFitExtensions/build" ] ; then
    rm -fr submodules/RooFitExtensions/build
fi
cd submodules/RooFitExtensions
rm -fr build && mkdir -p build && cd build && cmake .. && make -j8 && cd ..
source build/setup.sh
cd ${hh_combination_fw_path}

printf "${GREEN}\n
==============================================
| Compiling 2/2) submodules/quickstats ...
==============================================${NC}\n"
quickstats compile
rm -fr ${hh_combination_fw_path}/submodules/quickstats/quickstats/macros/CMSSWCore_HHComb
quickstats add_macro -i ${hh_combination_fw_path}/macros/CMSSWCore_HHComb
quickstats compile -m CMSSWCore_HHComb
