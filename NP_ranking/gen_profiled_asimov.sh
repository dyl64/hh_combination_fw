quickstats generate_asimov -i ../../../FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbyy/0.root --poi xsec_br --poi_val 1.0 --poi_profile 1.0 --conditional_mle --globs_np_matching -o ../../../FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbyy/cond_1_asimov_1.root --asimov_name cond_1_asimov_1

HHComb best_fit -i ../../../FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbyy/cond_1_asimov_1.root -s conditionalGlobs_1.0 -d cond_1_asimov_1
