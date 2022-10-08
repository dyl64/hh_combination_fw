# lumi = 1000, syst = stat_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1000ifb/stat_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/stat_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1000, syst = theo_exp_baseline, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1000ifb/theo_exp_baseline -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/theo_exp_baseline/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1000, syst = theo_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1000ifb/theo_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/theo_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 1000, syst = run2_syst, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1000ifb/run2_syst -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/run2_syst/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = stat_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1500ifb/stat_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/stat_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = theo_exp_baseline, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1500ifb/theo_exp_baseline -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/theo_exp_baseline/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = theo_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1500ifb/theo_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/theo_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = run2_syst, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi1500ifb/run2_syst -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/run2_syst/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = stat_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2000ifb/stat_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/stat_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = theo_exp_baseline, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2000ifb/theo_exp_baseline -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/theo_exp_baseline/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = theo_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2000ifb/theo_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/theo_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = run2_syst, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2000ifb/run2_syst -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/run2_syst/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = stat_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2500ifb/stat_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/stat_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = theo_exp_baseline, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2500ifb/theo_exp_baseline -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/theo_exp_baseline/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = theo_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2500ifb/theo_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/theo_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = run2_syst, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi2500ifb/run2_syst -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/run2_syst/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = stat_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/stat_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/stat_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = stat_only, task_scenario = kl_individual

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/stat_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/stat_only/kl_individual -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = stat_only, task_scenario = kl_parameterised

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/stat_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/stat_only/kl_parameterised -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --do-likelihood --do-pvalue

# lumi = 3000, syst = theo_exp_baseline, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/theo_exp_baseline -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_exp_baseline/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = theo_exp_baseline, task_scenario = kl_individual

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/theo_exp_baseline -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_exp_baseline/kl_individual -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty_no_kl_unc.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = theo_exp_baseline, task_scenario = kl_parameterised

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/theo_exp_baseline -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_exp_baseline/kl_parameterised -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty_no_kl_unc.json --do-limit --do-likelihood --do-pvalue

# lumi = 3000, syst = theo_only, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/theo_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_only/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = theo_only, task_scenario = kl_individual

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/theo_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_only/kl_individual -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = theo_only, task_scenario = kl_parameterised

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/theo_only -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_only/kl_parameterised -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --do-likelihood --do-pvalue

# lumi = 3000, syst = run2_syst, task_scenario = SM

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/run2_syst -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/run2_syst/SM -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = run2_syst, task_scenario = kl_individual

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/run2_syst -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/run2_syst/kl_individual -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = run2_syst, task_scenario = kl_parameterised

HHComb process_channels -i /afs/cern.ch/work/z/zhangr/HHcomb/hh_combination_fw/hh_combination_fw/FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/run2_syst -o ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/run2_syst/kl_parameterised -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --do-likelihood --do-pvalue

# lumi = 1000, syst = stat_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/stat_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1000, syst = theo_exp_baseline, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/theo_exp_baseline/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1000, syst = theo_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/theo_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 1000, syst = run2_syst, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1000ifb/run2_syst/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = stat_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/stat_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = theo_exp_baseline, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/theo_exp_baseline/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = theo_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/theo_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 1500, syst = run2_syst, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi1500ifb/run2_syst/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = stat_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/stat_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = theo_exp_baseline, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/theo_exp_baseline/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = theo_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/theo_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2000, syst = run2_syst, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2000ifb/run2_syst/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = stat_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/stat_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = theo_exp_baseline, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/theo_exp_baseline/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = theo_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/theo_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 2500, syst = run2_syst, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi2500ifb/run2_syst/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = stat_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/stat_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = stat_only, task_scenario = kl_individual

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/stat_only/kl_individual -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = stat_only, task_scenario = kl_parameterised

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/stat_only/kl_parameterised -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_stat_only.json --do-limit --do-likelihood --skip-pvalue

# lumi = 3000, syst = theo_exp_baseline, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_exp_baseline/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_no_kl_unc.json --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = theo_exp_baseline, task_scenario = kl_individual

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_exp_baseline/kl_individual -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty_no_kl_unc.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = theo_exp_baseline, task_scenario = kl_parameterised

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_exp_baseline/kl_parameterised -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty_no_kl_unc.json --do-limit --do-likelihood --skip-pvalue

# lumi = 3000, syst = theo_only, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_only/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = theo_only, task_scenario = kl_individual

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_only/kl_individual -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = theo_only, task_scenario = kl_parameterised

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/theo_only/kl_parameterised -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --do-likelihood --skip-pvalue

# lumi = 3000, syst = run2_syst, task_scenario = SM

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/run2_syst/SM -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --do-limit --skip-likelihood --do-pvalue

# lumi = 3000, syst = run2_syst, task_scenario = kl_individual

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/run2_syst/kl_individual -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl_<klambda[P]>" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_sm.yaml --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --skip-likelihood --skip-pvalue

# lumi = 3000, syst = run2_syst, task_scenario = kl_parameterised

HHComb combine_ws -i ${hh_combination_fw_path}/tutorials/projection2022/output/20220919_proj_all/lumi3000ifb/run2_syst/kl_parameterised -s ${hh_combination_fw_path}/configs/correlation_schemes/projection2022/nonres_kl_v14.json -c bbyy,bbtautau,bbbb -r nonres --file_expr "<mass[F]>_kl" --config ${hh_combination_fw_path}/configs/task_options/projection2022/proj_nonres_kl.yaml --param_expr "klambda=-2_8_0.1" --minimizer_options ${hh_combination_fw_path}/configs/minimizer_options/projection2021/projection_fix_xs_uncertainty.json --do-limit --do-likelihood --skip-pvalue

