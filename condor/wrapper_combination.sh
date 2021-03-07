#!/bin/bash

cd /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/

## setupATLAS
export ALRB_localConfigDir="/etc/hepix/sh/GROUP/zp/alrb";
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh;

source setup.sh

command="python scripts/pipeline/processChannels.py ../input ../output signal=$1 channel=$2 job_batch_start=$3 job_batch_stop=$4"

echo $command
$command
cd -
