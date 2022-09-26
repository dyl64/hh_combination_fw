#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

if [[ -z $hh_combination_fw_path ]]; then
    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
    source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
    source setup.sh 101
fi

command=$1
command=${command//____/ }
command=${command//^/}

echo $command
$command
unset command
cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/condor
