#!/bin/bash

cd /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
source setup.sh 101

ch=$1
param=$2
output_base="/afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/output_HHH_20220415_noSgHparam"
if [[ ${ch} == 'combined' ]]; then
    input_file="${output_base}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl.root"
else
    input_file="${output_base}/rescaled/nonres/${ch}/0_kl.root"
fi

output_dir="${output_base}/xsection_scan/${ch}"
command="quickstats limit_scan -i ${input_file} --outdir ${output_dir} --param_expr ${param} -p xsec_br --unblind --fix THEO_XS_fixmu_*=0,alpha_THEO_XS_PDFalphas_VBFSMHH*=0,alpha_THEO_XS_PDFalphas_ggFSMHH*=0,alpha_THEO_XS_SCALEMTop_ggFSMHH*=0,THEO_XS_COMBINED_HH_ggF*=0,THEO_XS_PDFalphas_HH_VBF*=0,THEO_XS_PDFalphas_HH_ggF*=0,THEO_XS_SCALE_HH_VBF*=0"

echo $command
$command
unset command
