#!/bin/bash

# input arg:
#       0: combine workspace
#       1: run likelihood scan
run_type=$1

# presetup
function presetup() {
    workspace_dir=${hh_combination_fw_path} # work directory (including scripts, config files, correlation schemes...)

    output_name="output_HHH2" # output directory name
    output_dir="${hh_combination_fw_path}/${output_name}" # the output directory
    data_dir="${hh_combination_fw_path}/FullRun2Workspaces/original/HHH2022/20220415/" # the data directory
    run_channel='bbyy,bbtautau,bbbb' # how many channels to combine

    # skip_individual="--skip-chan"
    skip_individual="--include-chan" # if to run individual results in likelihood scan
    
    combine="--combine" # if to run combined results in likelihood scan
    do_limit="--skip-limit" # don't calculate limit (default: --do-limit)
    config_file="configs/task_options/HHH2022/nonres_kl_kt_likelihood.yaml" # configuration file
    correlation_scheme="configs/correlation_schemes/HHH2022/nonres_kl_v11.json"
    minimizer_crosssection_scan="configs/minimizer_options/fix_xs_uncertainty.json" # fix theory cross section uncertainties for cross section scan
    minimizer_likelihood_scan="configs/minimizer_options/default.json" # include theory cross section uncertainties for likelihood scan
    poi="klambda" # no use but leave it here
    kl_kt_scan_range="klambda=-6_12_0.2,kt=0.8_1.4_0.05" # scan range for two pois
    kl_scan_range="klambda=-6_12_0.2" # scan range for kl only
    #fix_param="klambda=1,kt=1" # fix_parameter for generating asimov data
    other_poi="klambda=1,kt=1,kF=1,kH=1,kW=1,kV=1,kZ=1,kb=1,ktau=1" # fix other variables that were POI but missed in combined WS
    fix_auxiliary="--fix \"<auxiliary>\"" # fix hidden variables that were POI but missed in combined WS
}

##### setup #####
presetup


# prepare individual workspace file (regulating and skimming)
function CombineWorkspace() {
    echo HHComb process_channels -i "${data_dir}" -o "${output_dir}" -c ${run_channel} -r nonres --file_expr '"'"<mass[F]>_kl"'"' --config ${workspace_dir}/${config_file} "${do_limit}" --experimental #--param_expr "${kl_kt_scan_range}" --unblind --minimizer_options "${workspace_dir}/${minimizer_crosssection_scan}"
    echo HHComb combine_ws -i "${output_dir}" -s ${workspace_dir}/${correlation_scheme} -c ${run_channel} -r nonres --file_expr '"'"<mass[F]>_kl"'"' --config ${workspace_dir}/${config_file}  "${do_limit}" --unblind --experimental
    echo
}


# run likelihood scan on pois (kt, klambda, kV, k2V ...)
function RunXSScan() {
    #scan_type=$1
    #echo "-- Running scan for type ${scan_type}"
    #echo HHComb kl_likelihood -c "${run_channel}" --param_expr  "${kl_kt_scan_range}" --fix "${fix_param}" -i "${output_dir}" -p "${poi}" --config ${workspace_dir}/${config_file} --no-cache "${combine}" --hypothesis_type "${scan_type}" "${skip_individual}"
    ch=$1

    #declare -A dataset
    #dataset=( ["bbyy"]="combData" ["combined"]="combData"  ["bbtautau"]="obsData" ["bbbb"]="obsData" )  # -d "${dataset[${ch}]}" 
    if [[ ${ch} == 'combined' ]]; then
        input_file="${output_dir}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl.root"
    else
        input_file="${output_dir}/rescaled/nonres/${ch}/0_kl.root"
    fi
    echo quickstats limit_scan -i ${input_file} --outdir ${output_dir}/xsection_scan/${ch} --param_expr '"'${kl_scan_range}'"'  -p xsec_br --unblind ${fix_auxiliary}
    echo
}

function GenCondor() {
    for i in bbyy combined bbtautau bbbb ; do
        for j in `seq -6 0.2 12`; do
            echo Arguments = $i klambda=$j
            echo Queue 1
        done
    done
}

function RunLHScan() {
    ch=$1

    #declare -A dataset
    #dataset=( ["bbyy"]="combData" ["combined"]="combData"  ["bbtautau"]="obsData" ["bbbb"]="obsData" )
    if [[ ${ch} == 'combined' ]]; then
        input_file="${output_dir}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl.root"
    else
        input_file="${output_dir}/rescaled/nonres/${ch}/0_kl.root"
    fi
    echo quickstats likelihood_scan -i ${input_file} --outdir ${output_dir}/likelihood_scan/${ch}/2D_kl_kt --param_expr '"'${kl_kt_scan_range}'"'   ${fix_auxiliary}
    echo quickstats likelihood_scan -i ${input_file} --outdir ${output_dir}/likelihood_scan/${ch}/1D_kt_profiled --param_expr '"'${kl_scan_range}'"' --profile kt ${fix_auxiliary}
    echo quickstats likelihood_scan -i ${input_file} --outdir ${output_dir}/likelihood_scan/${ch}/1D_kt_nominal --param_expr '"'${kl_scan_range}'"'  ${fix_auxiliary}
    echo

}

#echo -e "##############\n## Combine workspace ###\n###########\n"
#CombineWorkspace
#echo -e "##############\n## Cross section scan ###\n###########\n"
#for i in bbyy combined bbtautau bbbb ; do
#    RunXSScan $i
#done
#GenCondor

echo -e "##############\n## Likelihood scan ###\n###########\n"
for i in bbyy combined bbtautau bbbb ; do
    RunLHScan $i
done
