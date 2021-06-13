How to run p-value

An example command:
submodules/RooStatTools/bin/runSigCalc ../output/v140invfb_20210531_obs2/rescaled/spin0/bbbb/1000_with_Asimov_POI_0_NP_fit.root  pvalue combWS ModelConfig combData > pvalue/bbbb_1000.log &


# Plotting
This is a new plotting code to eventually replace `submodules/hh_plot`

## Setup
No ROOT is required.
It runs with the LCG setup along with the hh_combination_fw with a caveat of old version of matplotlib==3.1.0.
As such, `sans-serif` font doesn't work properly.
To run with a newer version (e.g. 3.4.0), run with the conda env:
```
cd plotting/xsection
bash setup_conda.sh
```

## Plot combination
- Non-resonant