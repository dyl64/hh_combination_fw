#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw
export HH_COMBINATION_FW_MODE="skip_exist";

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
source setup.sh

job=$1

echo $job
if [[ $job == "process_channels" ]]; then
    input=$2
    channel=$3
    sigtype=$4
    output=$5
    regversion=$6
    mass=$7
    command="HHComb $job -i $input -c $channel -r $sigtype -o $output --config configs/regularization_${sigtype}_${regversion}.yaml --mass ${mass} --unblind"
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
$command
unset command job
