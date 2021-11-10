# individual
HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbtautau -r nonres -o ../output/v3000invfb_20211106_Local/indiv --minimizer_options configs/minimizer_fixXSunc.json --config configs/regularization_proj_v10.yaml --file_format "<mass[F]>_kl_<kl[P]>"
HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbyy -r nonres -o ../output/v3000invfb_20211106_Local/indiv --minimizer_options configs/minimizer_fixXSunc.json --config configs/regularization_proj_v10.yaml --file_format "<mass[F]>_kl_<kl[P]>"

HHComb combine_ws -i ../output/v3000invfb_20211106_Local/indiv/ -c bbyy,bbtautau -r nonres --minimizer_options configs/minimizer_fixXSunc.json --file_format "<mass[F]>_kl_<kl[P]>" --scheme configs/np_map_kl_v10.json


# param
## for XS
HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbyy,bbtautau -r nonres -o ../output/v3000invfb_20211106_Local/param/ --minimizer_options configs/minimizer.json --config configs/regularization_kl.yaml --no-cache --file_format "<mass[F]>_kl" --param klambda=-2_8_0.2

HHComb combine_ws -i ../output/v3000invfb_20211106_Local/param/ -r nonres -c bbyy,bbtautau --minimizer_options configs/minimizer_fixXSunc.json --scheme configs/np_map_kl_v10.json --file_format "<mass[F]>_kl" --param klambda=-2_8_0.2


## for LH
HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbyy,bbtautau -r nonres -o ../output/v3000invfb_20211106_Local/param/ --minimizer_options configs/minimizer.json --config configs/regularization_kl.yaml --no-cache --file_format "<mass[F]>_kl" --param klambda=1 --skip-limit

HHComb combine_ws -i ../output/v3000invfb_20211106_Local/param/ -r nonres -c bbtautau,bbyy --minimizer_options configs/minimizer.json --config configs/regularization_kl.yaml --scheme configs/np_map_kl_v10.json --skip-limit --no-cache --file_format "<mass[F]>_kl" --param klambda=1


HHComb kl_likelihood -i ../output/v3000invfb_20211106_Local/param/  -c bbyy,bbtautau --min -2 --max 10 --step 0.1 --no-cache









##==========
#HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -r nonres -c bbyy,bbtautau -o outputs -p klambda=1 --skip-limit --file_format "<mass[F]>_kl" --config configs/regularization_kl.yaml
#
#HHComb combine_ws -i outputs/ -r nonres -c bbyy,bbtautau -s configs/np_map_kl_v10.json --config configs/regularization_kl.yaml --skip-limit --file_format "<mass[F]>_kl" -p klambda=1 --skip-limit
#
#quickstats generate_standard_asimov -t -2 -p klambda -d combData -i outputs/combined/nonres/A-bbtautau_bbyy-fullcorr/0_kl.root -o 0_kl_asimov.root --fix xsec_br=1,klambda=1 --snapshot nominalNuis
#
#quickstats likelihood_scan -i 0_kl_asimov.root --min -2.0 --max 2.0 --step 1.0 -d asimovData_1_NP_Nominal --parallel -1 --print_level -1 -p klambda -o combined_klambda --no-cache --outdir outputs/likelihood/ --fix xsec_br=1
##==========











## NR
HHComb pvalue -i ../output/v3000invfb_20211106_CI/NR/rescaled/nonres/bbyy/0.root  -e -1

# plotting
python combine_plot.py -i ../../../output/v3000invfb_20211106_CI/NR/ -sf 1
python plot_kl.py -i ../../../output/v3000invfb_20211106_Local/indiv/ --config project3000 --rescale 0.032776
python plot_kl.py -i ../../../output/v3000invfb_20211106_Local/param/ --config project3000 --rescale 1



python plotting/likelihood/likelihood_plotting.py -a nonres -i ../output/v3000invfb_20211106_Local/param/likelihood/ -c combined_klambda.json -t bbtautau_klambda.json -y bbyy_klambda.json -o ../output/v3000invfb_20211106_Local/param/figures/ --threshold 12

