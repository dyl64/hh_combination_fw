#!/bin/bash

job=$1
input=$2
combData=$3
scan_min=$4
scan_max=$5
steps=15
n_toys=200
batchsize=50
seed=$6
output=$7
poi_min=$8
poi_max=$9
extras="--tolerance=0.1 --snapshot=nominalNuis --offset"


#export PATH=/afs/cern.ch/work/c/chlcheng/public/local/conda/miniconda/envs/ml-base/bin:$PATH
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
#lsetup "views LCG_98python3 x86_64-centos7-gcc8-opt"
source /cvmfs/sft.cern.ch/lcg/views/LCG_98python3/x86_64-centos7-gcc8-opt/setup.sh
which python
python -V

# setup quickstats in sandbox
export sandbox=/tmp/zhangr/quickstats
echo sandbox is ${sandbox}
rm -fr ${sandbox}
mkdir -p ${sandbox}
cd ${sandbox}
git clone /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/submodules/quickstats/
export PATH=${sandbox}/quickstats/bin:$PATH
export PYTHONPATH=${sandbox}/quickstats:$PYTHONPATH
which quickstats
quickstats compile
pip install click --target .

command="quickstats $job -i $input -d $combData --scan_min $scan_min --scan_max $scan_max --steps $steps --n_toys $n_toys --batchsize $batchsize --seed $seed -o /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/output/$output --poi_min ${poi_min} --poi_max ${poi_max} ${extras}"

echo $command
$command
unset command job

# cleanup sandbox
rm -fr ${sandbox}
