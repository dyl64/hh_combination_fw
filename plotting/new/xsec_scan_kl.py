#!/usr/bin/env python
# Rui Zhang 11.2021
# rui.zhang@cern.ch

from argparse import ArgumentParser
from datetime import datetime
from os import makedirs, path
import json
import pandas as pd
from quickstats.plots import Likelihood1DPlot

def main(args):
    hypo = f'kl{args.kl}'
    input_paths = {
        'bbyy': path.join(args.input_folder, "likelihood/", hypo, "bbyy_klambda.json"),
        'bbtautau': path.join(args.input_folder, "likelihood/", hypo, "bbtautau_klambda.json"),
        'combined': path.join(args.input_folder, "likelihood/", hypo, "combined_klambda.json"),
    }
    data = {}
    for channel in input_paths:
        data[channel] = json.load(open(input_paths[channel]))
    dfs = {}
    for channel in data:
        dfs[channel] = pd.DataFrame(data[channel]).dropna()
    
    styles_map = {
        'bbyy': {"color": "#9A0EEA", "marker": "o"},
        'bbtautau': {"color": "#008F00", "marker": "o"},
        'combined': {"color": "k", "marker": "o"}
    }
    label_map = {
        'bbyy': r"$\mathrm{b\bar{b}\gamma\gamma}$",
        'bbtautau': r"$\mathrm{b\bar{b}\tau^+\tau^-}$",
        'combined': r"Combined",
    }
    styles = {
        'legend':{
    
            'loc': (0.2, 0.5)
        }
    }
    analysis_label_options = {
        'x': 0.2,
        'y': 0.95,
        'energy': '14 TeV',
        'lumi': r'3000 fb$^{-1}$',
        'extra_text': 'HH non-resonant projection',
        'fontsize': 30
    }
    plotter = Likelihood1DPlot(dfs, label_map=label_map, styles_map=styles_map, 
                               styles=styles,
                               analysis_label_options=analysis_label_options)

    plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ymax=12, xmin=-2, xmax=10, draw_sigma_line=True)

    outfolder = f"{args.input_folder}/figures/"
    makedirs(path.dirname(outfolder), exist_ok=True)
    plt.savefig(f"{outfolder}/{args.output_name}_poi{args.kl}.pdf", bbox_inches="tight")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mSave\033[0m'.rjust(40, ' '), f"{outfolder}/{args.output_name}.pdf")

if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mPlot combined plots.\033[0m")
    parser.add_argument('-i', '--input_folder', default='../../../output/v3000invfb_20211106_Local/param/', required=False, help='input folder')
    parser.add_argument('-o', '--output_name', default='likelihood_param_kl', required=False, help='output filename')
    parser.add_argument('-kl', '--kl', default=1, choices = [0, 1], type=int, required=False, help='S+B or B hypothesis')

    args = parser.parse_args()
    main(args)
