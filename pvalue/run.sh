for input in /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/combined/nonres/A-bbtautau_bbyy-fullcorr/ \
/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbyy \
/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbtautau; do

    #quickstats generate_standard_asimov -i ${input}/0.root -o ${input}/asimov_0.root --poi xsec_br --poi_scale 0.032776 --asimov_types 1,2,3,4
    #for asimov in asimovData_1_NP_Profile asimovData_0_NP_Profile asimovData_muhat_NP_Profile S_unconstrained_NP_Fit; do
    for asimov in asimovData_1_unconstrained_NP_Profile; do
        HHComb pvalue -i ${input}/asimov_0.root -d  ${asimov} -s ${asimov}
    done
done
