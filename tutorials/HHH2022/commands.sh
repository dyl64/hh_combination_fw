#!/bin/bash

# presetup
function presetup() {
    timestamp=$1
    workspace_dir=${hh_combination_fw_path} # work directory (including scripts, config files, correlation schemes...)

    output_name="output_HHH_${timestamp}" # output directory name
    output_dir="${hh_combination_fw_path}/${output_name}" # the output directory
    data_dir="${hh_combination_fw_path}/FullRun2Workspaces/original/HHH2022/$timestamp/" # the data directory
    run_channel='bbyy,bbtautau,bbbb' # how many channels to combine

    # skip_individual="--skip-chan"
    skip_individual="--include-chan" # if to run individual results in likelihood scan
    
    combine="--combine" # if to run combined results in likelihood scan
    do_limit="--skip-limit" # don't calculate limit (default: --do-limit)
    if [[ ${timestamp} == *'noSgHparam'* ]]; then
        config_file="configs/task_options/HHH2022/nonres_kl_kt_xsection.yaml" # different POI list than likelihood version
    else
        config_file="configs/task_options/HHH2022/nonres_kl_kt_likelihood.yaml" # configuration file
    fi
    correlation_scheme="configs/correlation_schemes/HHH2022/nonres_kl_v11.json"
    minimizer_crosssection_scan="configs/minimizer_options/fix_xs_uncertainty.json" # fix theory cross section uncertainties for cross section scan
    minimizer_likelihood_scan="configs/minimizer_options/default.json" # include theory cross section uncertainties for likelihood scan
    poi="klambda" # no use but leave it here
    kl_kt_scan_range="klambda=-15_20_0.2,kt=0.6_1.6_0.1" # scan range for two pois
    kl_scan_range="klambda=-15_20_0.2" # scan range for kl only
    #fix_param="klambda=1,kt=1" # fix_parameter for generating asimov data
    other_poi="klambda=1,kt=1,kF=1,kH=1,kW=1,kV=1,kZ=1,kb=1,ktau=1" # fix other variables that were POI but missed in combined WS
    fix_auxiliary="--fix \"<auxiliary>\"" # fix hidden variables that were POI but missed in combined WS
    fix_theory="--fix \"THEO_XS_fixmu_*=0,alpha_THEO_XS_PDFalphas_VBFSMHH*=0,alpha_THEO_XS_PDFalphas_ggFSMHH*=0,alpha_THEO_XS_SCALEMTop_ggFSMHH*=0,THEO_XS_COMBINED_HH_ggF*=0,THEO_XS_PDFalphas_HH_VBF*=0,THEO_XS_PDFalphas_HH_ggF*=0,THEO_XS_SCALE_HH_VBF*=0\""
}

##### setup #####


# prepare individual workspace file
function CombineWorkspace() {
    presetup $1
    echo HHComb process_channels -i "${data_dir}" -o "${output_dir}" -c ${run_channel} -r nonres --file_expr '"'"<mass[F]>_kl"'"' --config ${workspace_dir}/${config_file} "${do_limit}" --experimental #--param_expr "${kl_kt_scan_range}" --unblind --minimizer_options "${workspace_dir}/${minimizer_crosssection_scan}"
    echo HHComb combine_ws -i "${output_dir}" -s ${workspace_dir}/${correlation_scheme} -c ${run_channel} -r nonres --file_expr '"'"<mass[F]>_kl"'"' --config ${workspace_dir}/${config_file}  "${do_limit}" --unblind --experimental
    echo
    if [[ $1 != *'noSgHparam'* ]]; then
        GenAsimov
    fi
}


# run likelihood scan on pois (kt, klambda, kV, k2V ...)
function RunXSScan() {
    presetup 20220415_noSgHparam
    #echo HHComb kl_likelihood -c "${run_channel}" --param_expr  "${kl_kt_scan_range}" --fix "${fix_param}" -i "${output_dir}" -p "${poi}" --config ${workspace_dir}/${config_file} --no-cache "${combine}" --hypothesis_type "${scan_type}" "${skip_individual}"
    ch=$1

    #declare -A dataset
    #dataset=( ["bbyy"]="combData" ["combined"]="combData"  ["bbtautau"]="obsData" ["bbbb"]="obsData" )  # -d "${dataset[${ch}]}" 
    if [[ ${ch} == 'combined' ]]; then
        input_file="${output_dir}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl.root"
    else
        input_file="${output_dir}/rescaled/nonres/${ch}/0_kl.root"
    fi
    echo quickstats limit_scan -i ${input_file} --outdir ${output_dir}/xsection_scan/${ch} --param_expr '"'${kl_scan_range}'"'  -p xsec_br --unblind ${fix_theory}
    echo
}

function GenCondorXS() {
    presetup 20220415_noSgHparam
    for i in bbyy combined bbtautau bbbb ; do
        for j in `seq -6 0.2 12`; do
            echo Arguments = $i klambda=$j
            echo Queue 1
        done
    done
}

function GenCondorLH() {
    presetup 20220415_noSgHparam
    #for d in obs prefit postfit1 postfit2; do
    for d in obs prefit postfit2; do
        for i in combined bbbb bbtautau bbyy ; do
            for j in `seq -15 5 15`; do
                echo source ../../condor/wrapper_HHH_llhd.sh $i 2D_kl_kt klambda=${j}_$((j+5))_0.2,kt=0.6_1.6_0.1 $d
                echo source ../../condor/wrapper_HHH_llhd.sh $i 1D_kt_profiled klambda=${j}_$((j+5))_0.2,kt=_0_ $d
                echo source ../../condor/wrapper_HHH_llhd.sh $i 1D_kt_nominal klambda=${j}_$((j+5))_0.2 $d
                break

                echo Arguments = $i 2D_kl_kt klambda=${j}_$((j+5))_0.2,kt=0.6_1.6_0.1 $d
                echo Queue 1
                echo Arguments = $i 1D_kt_profiled klambda=${j}_$((j+5))_0.2,kt $d
                echo Queue 1
                echo Arguments = $i 1D_kt_nominal klambda=${j}_$((j+5))_0.2 $d
                echo Queue 1
            done
        done
    done

}

function GenAsimov() {
    presetup 20220415
    for ch in bbyy combined bbtautau bbbb ; do
        if [[ ${ch} == 'combined' ]]; then
            input_file="${output_dir}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr/0_kl.root"
        else
            input_file="${output_dir}/rescaled/nonres/${ch}/0_kl.root"
        fi
        type=1,2,-2
        echo quickstats generate_standard_asimov -i ${input_file} -o ${input_file//0_kl.root/0_kl_asimov.root} --asimov_types ${type} --asimov_snapshots asimovtype_1_mu1_mu1,asimovtype_2_muprof_mu1,asimovtype_n2_prefit_mu1 --asimov_names combData_asimovtype_1_mu1_mu1,combData_asimovtype_2_muprof_mu1,combData_asimovtype_n2_prefit_mu1 -p xsec_br
        echo quickstats likelihood_fit --retry 2 -i ${input_file} --save_ws ${input_file//0_kl.root/0_kl_fitted.root} --save_snapshot muhatSnapshot_kl_kt --profile "klambda,kt"
        echo quickstats likelihood_fit --retry 2 -i ${input_file//0_kl.root/0_kl_fitted.root} --save_ws ${input_file//0_kl.root/0_kl_fitted.root} --save_snapshot muhatSnapshot_kl --profile "klambda"
    done
}

function RunLHScan() {
    presetup 20220415
    ch=$1
    obs=$2

    #declare -A dataset
    #dataset=( ["bbyy"]="combData" ["combined"]="combData"  ["bbtautau"]="obsData" ["bbbb"]="obsData" )
    if [[ ${ch} == 'combined' ]]; then
        input_path="${output_dir}/combined/nonres/A-bbbb_bbtautau_bbyy-fullcorr"
    else
        input_path="${output_dir}/rescaled/nonres/${ch}"
    fi
    if [[ ${obs} == *'obs'* ]]; then
        snapshot_kl_kt="--snapshot muhatSnapshot_kl_kt --uncond_snapshot muhatSnapshot_kl_kt"
        snapshot_kl="--snapshot muhatSnapshot_kl --uncond_snapshot muhatSnapshot_kl"
        input_file=${input_path}/0_kl_fitted.root
        echo quickstats likelihood_scan --retry 2 -i ${input_file} --outdir ${output_dir}/likelihood_scan/${obs}/${ch}/2D_kl_kt --param_expr '"'${kl_kt_scan_range}'"' ${snapshot_kl_kt}
        echo quickstats likelihood_scan --retry 2 -i ${input_file} --outdir ${output_dir}/likelihood_scan/${obs}/${ch}/1D_kt_profiled --param_expr '"'${kl_scan_range},kt'"' --profile '"'kt=_0_'"' ${snapshot_kl_kt}
        echo quickstats likelihood_scan --retry 2 -i ${input_file} --outdir ${output_dir}/likelihood_scan/${obs}/${ch}/1D_kt_nominal --param_expr '"'${kl_scan_range}'"' ${snapshot_kl}
    else
        if [[ ${obs} == *'prefit'* ]]; then
            snapshot="-s asimovtype_n2_prefit_mu1 -d combData_asimovtype_n2_prefit_mu1"
            input_file=${input_path}/0_kl_asimov.root
        elif [[ ${obs} == *'postfit1'* ]]; then
            snapshot="-s asimovtype_1_mu1_mu1 -d combData_asimovtype_1_mu1_mu1"
            input_file=${input_path}/0_kl_asimov.root
        elif [[ ${obs} == *'postfit2'* ]]; then
            snapshot="-s asimovtype_2_muprof_mu1 -d combData_asimovtype_2_muprof_mu1"
            input_file=${input_path}/0_kl_asimov.root
        else
            snapshot=""
            input_file=""
        fi
        echo quickstats likelihood_scan --retry 2 -i ${input_file} --outdir ${output_dir}/likelihood_scan/${obs}/${ch}/2D_kl_kt --param_expr '"'${kl_kt_scan_range}'"' ${snapshot}
        echo quickstats likelihood_scan --retry 2 -i ${input_file} --outdir ${output_dir}/likelihood_scan/${obs}/${ch}/1D_kt_profiled --param_expr '"'${kl_scan_range},kt'"' --profile '"'kt=_0_'"' ${snapshot}
        echo quickstats likelihood_scan --retry 2 -i ${input_file} --outdir ${output_dir}/likelihood_scan/${obs}/${ch}/1D_kt_nominal --param_expr '"'${kl_scan_range}'"' ${snapshot}
    fi
    echo
}

#echo -e "##############\n## Combine workspace ###\n###########\n"
#CombineWorkspace 20220415_noSgHparam
#CombineWorkspace 20220415
#echo -e "##############\n## Cross section scan ###\n###########\n"
#for i in bbyy combined bbtautau bbbb ; do
#    RunXSScan $i
#done
#GenCondorXS

#echo -e "##############\n## Likelihood scan ###\n###########\n"
for i in bbyy combined bbtautau bbbb ; do
    RunLHScan $i obs
    RunLHScan $i prefit
##    RunLHScan $i postfit1
    RunLHScan $i postfit2
done
#GenCondorLH
