#!/bin/bash

cd /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/

## setupATLAS
#export ALRB_localConfigDir="/etc/hepix/sh/GROUP/zp/alrb";
#export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
#echo source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh;
#source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh;
source setup.sh

job=$1
echo $job
if [[ $job == "pipeline" ]]; then
    command="python scripts/pipeline/processChannels.py ../input ../output signal=$2 channel=$3 job_batch_start=$4 job_batch_stop=$5"
elif [[ $job == "combine" ]]; then
    if [[ "$#" -eq 3 ]]; then
        command="python scripts/combination/auto/combine_ws.py $2=$3"
    elif [[ "$#" -eq 5 ]]; then
        command="python scripts/combination/auto/combine_ws.py $2=$3 $4=$5"
    else
        echo "command number not pass": $#
    fi
else
    echo "command not found": $job
fi


echo $command
$command
unset command job
