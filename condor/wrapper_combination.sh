#!/bin/bash

cd /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/

## setupATLAS
export ALRB_localConfigDir="/etc/hepix/sh/GROUP/zp/alrb";
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh;

source setup.sh

job=$1
if [[ $job == "pipeline" ]]; then
    command="python scripts/pipeline/processChannels.py ../input ../output signal=$2 channel=$3 job_batch_start=$4 job_batch_stop=$5"
elif [[ $job == "combine" ]]; then
    command="python scripts/combination/auto/combine_ws.py nonres=$2"
fi

echo $command
$command
cd -
