#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
source setup.sh

job=$1
input=$2
dataset=$3
poi=$4
output=$5
command="quickstats $job -i $input -d $dataset -x $poi -o $output --parallel -1 --cache --batch_mode --exclude \"xi*,nbkg*,BKG*,ATLAS_norm*,gamma_*,NORM_*\""

echo $command
$command
unset command job
