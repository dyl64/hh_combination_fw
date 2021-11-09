#!/usr/bin/env python
# Rui Zhang 6.2021
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
            'combined': f'{infolder}/NR/limits/nonres/combined/A-bbtautau_bbyy-fullcorr/0.json',
            'bbyy': f'{infolder}/NR/limits/nonres/bbyy/0.json',
            'bbtautau': f'{infolder}/NR/limits/nonres/bbtautau/0.json',
        }
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
            'combined': r'Combined',
        }
        
        self.analysis_label_options = {'fontsize':30, 'energy': '14 TeV', 
                                  'lumi': '3000 fb$^{-1}$',
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

    def extract_df_from_json(self):
        data_dict = {}
        for chan, json_file in self.json_files_main.items():
            data_dict[chan] = json.load(open(json_file))
        for chan in data_dict:
            data_dict[chan][self.name_addition] = json.load(open(self.json_files_addition[chan]))['0']
        df = pd.DataFrame(data_dict) * self.scale_factor
        return df

    
def main(args):
    dr = DataReader(args)
    df = dr.extract_df_from_json()
    plotter = UpperLimit1DPlot(df, dr.label_map, line_below=["bbyy"], labels=dr.labels, analysis_label_options=dr.analysis_label_options, styles=dr.styles)
    ax = plotter.draw(logx=False, xlabel=r"95% CL upper limit on signal strength", draw_observed=False, draw_stat=True)
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

    args = parser.parse_args()
    main(args)
