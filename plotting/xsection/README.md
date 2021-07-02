How to run p-value

An example command:
submodules/RooStatTools/bin/runSigCalc ../output/v140invfb_20210531_obs2/rescaled/spin0/bbbb/1000_with_Asimov_POI_0_NP_fit.root  pvalue combWS ModelConfig combData > pvalue/bbbb_1000.log &


# Plotting
This is a new plotting code to eventually replace `submodules/hh_plot`

## Setup
No ROOT is required.
It runs with the LCG setup along with the hh_combination_fw with a caveat of old version of matplotlib==3.1.0.
As such, `sans-serif` font doesn't work properly.
To run with a newer version (e.g. 3.4.2), run with the conda env:
```
source /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/anaconda3/setup.sh
```

## Plot combination
- Non-resonant
```
python plotting/xsection/combination_plotting.py nonres --logx -l ../output/v140invfb_20210531_obs/limits/data-files/nonres-bb*dat
python plotting/xsection/combination_plotting.py nonres --logx -l ../output/v140invfb_20210531_obs/limits/root-files/nonres/*/0.json
```

- Spin-0
```
python plotting/xsection/combination_plotting.py spin0 --logx --dat_list ../output/v140invfb_20210531_obs/limits/data-files/spin0-bb* --com_list ../output/v140invfb_20210531_obs/limits/data-files/spin0-combined-A-bb*dat

python plotting/xsection/combination_plotting.py spin0 --logx --dat_list ../output/v140invfb_20210531_obs/limits/root-files/spin0/bb*/*[0-9].json --com_list ../output/v140invfb_20210531_obs/limits/root-files/spin0/combined/A-*-nocorr/*[0-9].json
```

## Plot summary plot for EPS 2021
Relevant results are stored in `plotting/xsection/summary_plot_2021/*.csv`.
They are collected by hand from hepdata.
No frequent update is expected.
- Spin-0
```
python plotting/xsection/combination_plotting.py spin0  --logx  --dat_list ../v140invfb_20210613_obs/limits/root-files/spin0/bbbb/*[0-9].json --com_list ../v140invfb_20210613_obs/limits/root-files/spin0/combined/A-*-nocorr/*[0-9].json --unblind

python plotting/xsection/combination_plotting.py spin0  --logx  --unblind --summary_json plotting/xsection/summary_plot_2021/summary.json --relative --no-error
```

- Non-resonant
```
python plotting/xsection/combination_plotting.py nonres --logx -l ../v140invfb_20210613_obs/limits/root-files/nonres/*/*/0.json ../v140invfb_20210613_obs/limits/root-files/nonres/*/0.json

python plotting/xsection/combination_plotting.py nonres --logx --csv plotting/xsection/summary_plot_2021/upperlimit_xsec_nonres_json_obs.csv --unblind
```
