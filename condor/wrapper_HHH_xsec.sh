#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

#export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
#source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
#source setup.sh

ch=$1
param=$2
if [[ ${ch} == 'combined' ]]; then
    input_file="/afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/output_HHH/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl.root"
else
    input_file="/afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/output_HHH/rescaled/nonres/${ch}/0_kl.root"
fi

output_dir="/afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/output_HHH/xsection_scan/${ch}"
command="quickstats limit_scan -i ${input_file} --outdir ${output_dir} --param_expr ${param} -p xsec_br --unblind --fix \"<auxiliary>\""

echo $command
$command
unset command
