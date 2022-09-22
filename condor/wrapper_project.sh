#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
source setup.sh 102

command=`echo $1 | sed "s/____/ /g"`
command=`echo $command |sed 's@${hh_combination_fw_path}@/afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw@g'`

echo $command
$command
unset command
