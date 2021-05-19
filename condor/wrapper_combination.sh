#!/bin/bash

cd /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/MR/hh_combination_fw/
export HH_COMBINATION_FW_MODE="skip_exist";

## setupATLAS
#export ALRB_localConfigDir="/etc/hepix/sh/GROUP/zp/alrb";
#export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
#echo source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh;
#source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh;
source setup.sh

job=$1

echo $job
if [[ $job == "process_channels" ]]; then
    input=$2
    sigtype=$3
    channel=$4
    output=$5
    regversion=$6
    mass=$7
    command="HHComb $job -i $input -r $sigtype -c $channel -o $output --config configs/regularization_${sigtype}_${regversion}.yaml --mass ${mass}"
elif [[ $job == "combine_ws" ]]; then
    input=$2
    sigtype=$3
    channel=$4
    output=$5
    scheme=$6
    mass=$7
    command="HHComb $job -i $input -c $combine_channels"
else
    echo "command not found": $job
fi


echo $command
#$command
unset command job
