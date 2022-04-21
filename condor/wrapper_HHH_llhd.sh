#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
source setup.sh 101

ch=$1
out=$2
param=$3
profile=$4
if [[ ${profile} == 'profile' ]]; then
    profile="--profile kt"
else
    profile=""
fi

output_base="/afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/output_HHH3"
if [[ ${ch} == 'combined' ]]; then
    input_file="${output_base}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl.root"
else
    input_file="${output_base}/rescaled/nonres/${ch}/0_kl.root"
fi

output_dir="${output_base}/likelihood_scan/${ch}/${out}"
command="quickstats likelihood_scan -i ${input_file} --outdir ${output_dir} --param_expr ${param} ${profile}"

echo $command
$command
unset command
