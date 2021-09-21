input_path=/eos/atlas/unpledged/group-wisc/users/zhangr/HHcomb/output/v140invfb_20210915_CI
for input in ${input_path}/output_mu_unblind/rescaled/nonres/bbyy/ \
             ${input_path}/output_mu_unblind/rescaled/nonres/bbtautau/ \
             ${input_path}/output_mu_unblind/combined/nonres/A-bbtautau_bbyy-fullcorr/ ;
do
    quickstats generate_standard_asimov -i ${input}/0.root -o ${input}/standard_asimov2_0.root --poi xsec_br --poi_scale 0.032776 --asimov_types 2
    HHComb best_fit -i ${input}/asimov2_0.root -s asimovData_muhat_NP_Profile -d asimovData_muhat_NP_Profile
    #HHComb pvalue -i ${input}/standard_asimov2_0.root -d asimovData_muhat_NP_Profile  -s asimovData_muhat_NP_Profile
done
unset input_path
