for input in ../../../FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbyy/ \
            ../../../FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbtautau/ \
            ../../../FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/combined/nonres/A-bbtautau_bbyy-fullcorr/ ;
do
    quickstats generate_asimov -i ${input}/0.root --poi xsec_br --poi_val 0.032776  --poi_profile 0.032776 --conditional_mle --globs_np_matching -o ${input}/cond_1_asimov_1.0.root --asimov_name cond_1_asimov_1
    HHComb best_fit -i ${input}/cond_1_asimov_1.0.root -s conditionalGlobs_0.032776 -d cond_1_asimov_1
done
