#!/usr/bin/env python
# Rui Zhang 6.2021
# rui.zhang@cern.ch

from datetime import datetime
from pdb import set_trace
import json
import pandas as pd
from quickstats.plots import UpperLimit2DPlot
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from os import makedirs, path

def xs_ggF(kl):
    return (70.3874-50.4111*kl+11.0595*kl**2) #XS in fb

def xs_VBF(kl):
    return (4.581-4.245*kl+1.359*kl**2) 

def xs_HH(kl, s=13):
    if s == 13:
        return xs_ggF(kl) + xs_VBF(kl)
    elif s == 14:
        return (xs_ggF(kl) + xs_VBF(kl)) * 1.18

class DataReader(object):
    def __init__(self, args):
        infolder = args.input_folder
        path_map = {
            'bbtautau': 'bbtautau',
            'bbyy': 'bbyy',
            'combined': 'combined/A-bbtautau_bbyy-fullcorr',
        }
        label_map = {
            'bbtautau': r'$\mathrm{b\bar{b}\tau^+\tau^-}$',
            'bbyy': r'$\mathrm{b\bar{b}\gamma\gamma}$',
            'combined': r'Combined',
        }
        scale_factor = 1000/32.776
        self.df_param = pd.DataFrame(json.load(open(f"{infolder}/param/limits/nonres/{path_map[args.chan]}/limits.json"))).set_index(['klambda'])
        self.df_indiv = pd.DataFrame(json.load(open(f"{infolder}/indiv/limits/nonres/{path_map[args.chan]}/limits.json"))).set_index(['kl']) * scale_factor
        
        self.atlas_label_options={
                    'x': 0.05,
                    'y': 0.97,
                    'status': 'int', 
                    'energy' : '14 TeV', 
                    'lumi' : "4000 fb$^{-1}$", 
                    'extra_text' : label_map[args.chan],
                    'fontsize': 25
                    }
        self.styles = {
                'figsize': (8, 6),
                'axis':{
                    'tick_bothsides': True,
                    'major_length': 12,
                    },
                'legend':{
                    'loc': (0.05, 0.41),
                    'fontsize': 18,
                    'frameon': False
                    }
                }
        
        self.labels = {
                '2sigma': 'Exp. $\pm 2\sigma$ (param)',
                '1sigma': 'Exp. $\pm 1\sigma$ (param)',
                'expected': 'Exp. (param)',
                'observed': 'Obs. (param)'
                }
        
        self.labels_sec = {
                '2sigma': 'Exp. $\pm 2\sigma$ (indiv)',
                '1sigma': 'Exp. $\pm 1\sigma$ (indiv)',
                'expected': 'Exp. (indiv)',
                'observed': 'Obs. (indiv)'
                }

def main(args):
    dr = DataReader(args)
    kl = dr.df_param.index.astype(float).values
    xsec = xs_HH(kl, args.energy)
    plotter = UpperLimit2DPlot(dr.df_param, dr.df_indiv, labels=dr.labels, labels_sec=dr.labels_sec, analysis_label_options=dr.atlas_label_options, styles=dr.styles, scale_factor = xsec)
    plotter.config['primary_alpha'] = 0.7
    plotter.config['secondary_alpha'] = 0.7
    plotter.config['primary_hatch'] = None
    ax = plotter.draw(ylim=[0, 160], xlabel=r'$\kappa_\lambda$', ylabel=r'$\sigma_{ggF+VBF}$ [fb]', xlim=(-3, 9), draw_observed=False)
    
    outfile = f"{args.input_folder}/figures/{args.output_name}_{args.chan}.pdf"
    makedirs(path.dirname(outfile), exist_ok=True)
    plt.savefig(outfile, bbox_inches="tight")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mSave\033[0m'.rjust(40, ' '), outfile)


if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mPlot combined plots.\033[0m")
    parser.add_argument('-i', '--input_folder', default='../../../output/v3000invfb_20211106_Local/', required=False, help='input folder')
    parser.add_argument('-o', '--output_name', default='compare_indv_param', required=False, help='output filename')
    parser.add_argument('-c', '--chan', default='combined', choices=['combined', 'bbyy', 'bbtautau'], required=False, help='channel to plot')
    parser.add_argument('-s', '--energy', default=14, choices=[13, 14, 13.6], required=False, help='collision energy')

    args = parser.parse_args()
    main(args)
