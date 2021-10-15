#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

#export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
#source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
#source setup.sh
export PATH=/afs/cern.ch/work/c/chlcheng/public/local/conda/miniconda/envs/ml-base/bin:$PATH

job=$1
input=$2
dataset=$3
scan_min=$4
scan_max=$5
steps=15
n_toys=50
batchsize=50
seed=$6
output=$7
poi_min=$8
poi_max=$9
command="quickstats $job -i $input -d $dataset --scan_min $scan_min --scan_max $scan_max --steps $steps --n_toys $n_toys --batchsize $batchsize --seed $seed -o /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/output/$output --poi_min ${poi_min} --poi_max ${poi_max}"

echo $command
$command
unset command job
