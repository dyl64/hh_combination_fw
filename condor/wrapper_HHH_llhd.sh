#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

if [[ -z $hh_combination_fw_path ]]; then
    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
    source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
    source setup.sh 101
fi

ch=$1
out=$2
param=$3
obs=$4

output_base="/afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/output_HHH_20220415"
if [[ ${ch} == 'combined' ]]; then
    input_file="${output_base}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl_fitted.root"
else
    input_file="${output_base}/rescaled/nonres/${ch}/0_kl_fitted.root"
fi

if [[ ${obs} == *'obs'* ]]; then
    snapshot="--snapshot muhatSnapshot --uncond_snapshot muhatSnapshot"
elif [[ ${obs} == *'prefit'* ]]; then
    snapshot="-s asimovtype_n2_prefit_mu1 -d combData_asimovtype_n2_prefit_mu1"
    input_file=${input_file//0_kl_fitted.root/0_kl_asimov.root}
else
    snapshot="-s asimovtype_2_muprof_mu1 -d combData_asimovtype_2_muprof_mu1"
    input_file=${input_file//0_kl_fitted.root/0_kl_asimov.root}
fi
output_dir="${output_base}/likelihood_scan/${obs}/${ch}/${out}"


command="quickstats likelihood_scan --retry 2 -i ${input_file} --outdir ${output_dir} --param_expr ${param} ${snapshot}"
echo $command
$command

cd -
unset command
