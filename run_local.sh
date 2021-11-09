# individual
HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbtautau -r nonres -o ../output/v3000invfb_20211106_Local/indiv --minimizer_options configs/minimizer_fixXSunc.json --config configs/regularization_proj_v10.yaml --file_format "<mass[F]>_kl_<kl[P]>"
HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbyy -r nonres -o ../output/v3000invfb_20211106_Local/indiv --minimizer_options configs/minimizer_fixXSunc.json --config configs/regularization_proj_v10.yaml --file_format "<mass[F]>_kl_<kl[P]>"

HHComb combine_ws -i ../output/v3000invfb_20211106_Local/indiv/ -c bbyy,bbtautau -r nonres --minimizer_options configs/minimizer_fixXSunc.json --file_format "<mass[F]>_kl_<kl[P]>" --scheme configs/np_map_kl_v10.json


# param
HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbyy,bbtautau -r nonres -o ../output/v3000invfb_20211106_Local/param/ --minimizer_options configs/minimizer.json --config configs/regularization_kl.yaml --no-cache --file_format "<mass[F]>_kl" --param klambda=1
#HHComb process_channels -i ../../FullRun2Workspaces/original/20211106_mu_all/ -c bbyy,bbtautau -r nonres -o ../output/v3000invfb_20211106_Local/param/ --minimizer_options configs/minimizer.json --config configs/regularization_kl.yaml --no-cache --file_format "<mass[F]>_kl" --param klambda=-2_8_0.2

# for LH
HHComb combine_ws -i ../output/v3000invfb_20211106_Local/param/ -r nonres -c bbtautau,bbyy --minimizer_options configs/minimizer.json --config configs/regularization_kl.yaml --scheme configs/np_map_kl_v10.json --skip-limit --no-cache --file_format "<mass[F]>_kl" --param klambda=1

## for XS
#HHComb combine_ws -i ../output/v3000invfb_20211106_Local/param/ -r nonres -c bbyy,bbtautau --minimizer_options configs/minimizer_fixXSunc.json --scheme configs/np_map_kl_v10.json --file_format "<mass[F]>_kl" --param klambda=-2_8_0.2


# LH scan
HHComb kl_likelihood -i ../output/v3000invfb_20211106_Local/param/  -c bbyy,bbtautau --min -2 --max 10 --step 0.1


## NR
HHComb pvalue -i ../output/v3000invfb_20211106_CI/NR/rescaled/nonres/bbyy/0.root  -e -1
