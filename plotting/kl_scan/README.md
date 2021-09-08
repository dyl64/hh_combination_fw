## Overview 
This script plots the kappa lambda scans for the HH combination. It can plot each channel individually, and can also layer all channels on top of eachother in a combined plot. 

## To run 

In this directory run the following setup script:
```
. setup.py 
```

This will set up an LCG 100 environment and install the atlas matplot lib style, atlas_mpl_style. 

Next run: 
```
python plot_kl.py
```
This will make the plots of the $\kappa_\lambda$ scan found in the paper. 

## To make changes
If you would like to plot a new set of limits from the individual workspaces, scroll to the bottom of plot_kl.py to "__main__" and change the input glob string. The input glob string is set up as follows: /eos/user/j/jpearkes/hh_combination_outputs/individual/alkaid_aug_27/bbyy_new/*[!y].json". If you are using Alkaid's inputs, the string "alkaid" must be in the glob string somewhere, to tell the script to parse files with his naming convention. The "[!y]" portion makes sure to ignore all *_summary.json files which are not needed for this tool. 

json files must be named according to nXpX, e.g. kl = -0.5 -> kln0p5.json, kl = 1.0 -> kl1p5.json, or 0_kl_n0p5.json if using "alkaid" in the input glob string. 

The code expects input json files in the following format:
```
{
  "0": 0.17627053780337487,
  "2": 0.3912660039668158,
  "1": 0.26065791138829253,
  "-1": 0.1270126830771918,
  "-2": 0.09460894205543723,
  "obs": 0.13204760044221495,
  "inj": 0
}
```

Output plots will be saved directly in this directory.

## Contact
If you have questions about this script, please direct them to me: jannicke.pearkes@cern.ch

