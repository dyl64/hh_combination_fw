#!/usr/bin/env python
# Rui Zhang 11.2021
# rui.zhang@cern.ch

from datetime import datetime
import pandas as pd
import json
from pdb import set_trace
import matplotlib.pyplot as plt
from quickstats.plots import UpperLimit1DPlot
from argparse import ArgumentParser
from os import makedirs, path

class DataReader(object):
    def __init__(self, args):
        infolder = args.input_folder
        self.json_files_main = {
            'combined': f'{infolder}/limits/nonres/combined/A-bbtautau_bbyy-fullcorr/0.json',
            'bbyy': f'{infolder}/limits/nonres/bbyy/mass_0.json',
            'bbtautau': f'{infolder}/limits/nonres/bbtautau/mass_0.json',
        }
        if args.all:
            self.json_files_main.update({
                'combined': f'{infolder}/limits/nonres/combined/A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-fullcorr/0.json',
                'combined3': f'{infolder}/limits/nonres/combined/A-bbbb_bbll_bbtautau-fullcorr/0.json',
                'combined5ll': f'{infolder}/limits/nonres/combined//A-bbbb_bbtautau_bbVV_bbyy_WWWW-fullcorr/0.json',
                'combined5VV': f'{infolder}/limits/nonres/combined/A-bbbb_bbll_bbtautau-fullcorr/0.json',
                'combined5WW': f'{infolder}/limits/nonres/combined/A-bbbb_bbll_bbtautau-fullcorr/0.json',
                'bbbb': f'{infolder}/limits/nonres/bbbb/mass_0.json',
                'bbll': f'{infolder}/limits/nonres/bbll/mass_0.json',
                'bbVV': f'{infolder}/limits/nonres/bbVV/mass_0.json',
                'WWWW': f'{infolder}/limits/nonres/WWWW/mass_0.json',
            })
        self.json_files_addition = {
            'combined': f'{infolder}/stat/limits/nonres/combined/A-bbtautau_bbyy-fullcorr/0.json',
            'bbyy': f'{infolder}/stat/limits/nonres/bbyy/0.json',
            'bbtautau': f'{infolder}/stat/limits/nonres/bbtautau/0.json',
        }
        self.name_addition = 'stat'
        self.scale_factor = args.sf

        self.label_map = {
            'bbtautau': r'$\mathrm{b\bar{b}\tau^+\tau^-}$',
            'bbyy': r'$\mathrm{b\bar{b}\gamma\gamma}$',
            'bbll': r'$\mathrm{b\bar{b}ll}$',
            'bbVV': r'$\mathrm{b\bar{b}VV}$',
            'WWWW': r'Multilepton',
            'combined': r'Combined',
            'combined3': r'Top 3 combined',
            'combined5ll': r'N - bbll',
            'combined5VV': r'N - bbVV',
            'combined5WW': r'N - ML',
        }
        
        self.analysis_label_options = {'fontsize':30, 'energy': '13 TeV', 
                                  'lumi': '139 fb$^{-1}$',
                                  'extra_text': r'$\sigma_{ggF+VBF}^{SM}=32.78$ fb'}
        
        self.labels = {
            '2sigma': r'Comb. exp. limit $\pm 2\sigma$',
            '1sigma': r'Comb. exp. limit $\pm 1\sigma$',
            'expected': r'Expected limit',
            'observed': r'Observed limit',
        }
        self.styles = {
            'axis':{
                'tick_bothsides': False,
                'major_length': 12,
                },
        }
        self.stat = args.stat

    def extract_df_from_json(self):
        data_dict = {}
        for chan, json_file in self.json_files_main.items():
            data_dict[chan] = json.load(open(json_file))
        if self.stat:
            for chan in data_dict:
                data_dict[chan][self.name_addition] = json.load(open(self.json_files_addition[chan]))['0']
        df = pd.DataFrame(data_dict) * self.scale_factor
        return df

    
def main(args):
    dr = DataReader(args)
    df = dr.extract_df_from_json()
    plotter = UpperLimit1DPlot(df, dr.label_map, line_below=["bbyy"], labels=dr.labels, analysis_label_options=dr.analysis_label_options, styles=dr.styles)
    ax = plotter.draw(logx=False, xlabel=r"95% CL upper limit on signal strength", draw_observed=False, draw_stat=args.stat)
    ax.set_xlim([0, None])
    outfolder = f"{args.input_folder}/figures/"
    makedirs(path.dirname(outfolder), exist_ok=True)
    plt.savefig(f"{outfolder}/{args.output_name}.pdf", bbox_inches="tight")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mSave\033[0m'.rjust(40, ' '), f"{outfolder}/{args.output_name}.pdf")

if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mPlot combined plots.\033[0m")
    parser.add_argument('-i', '--input_folder', default='../../../output/v3000invfb_20211106_CI/', required=False, help='input folder')
    parser.add_argument('-o', '--output_name', default='upperlimit_xsec_nonres_fullcorr_mu', required=False, help='output filename')
    parser.add_argument('-sf', '--sf', default=1000/32.776, type=float, required=False, help='reverse of scale factor applied in regularisation.yaml')
    parser.add_argument('-stat', '--stat', action='store_true', default=False, help='Switch on stat only results')
    parser.add_argument('-a', '--all', action='store_true', default=False, help='Run all 6 channels')

    args = parser.parse_args()
    main(args)
