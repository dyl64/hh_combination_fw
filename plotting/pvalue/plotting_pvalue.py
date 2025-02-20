#!/usr/bin/env python
# Rui Zhang 6.2020
# rui.zhang@cern.ch

import sys
import os
import numpy as np
from argparse import ArgumentParser
from pdb import set_trace
import json
from math import exp, sqrt, isclose
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from glob import glob
from matplotlib import rcParams
rcParams['axes.linewidth'] = 1.5
#rcParams['font.sans-serif'] = "Arial"
#rcParams['font.family'] = "sans-serif"
#rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

def get_masses_and_pvalues(files, value='pvalue'):
    data = {}
    for f in files:
        try:
            data[f.split('/')[-1].split('_')[0]] = json.load(open(f))[value]
        except:
            print('problem in', f)

    X = np.array(list(data.keys()), dtype=float)
    Y = np.array(list(data.values()))
    null_index = (Y == None)
    X = X[~null_index]
    Y = Y[~null_index]
    indices = np.argsort(X)
    x = X[indices]
    y = Y[indices]
    return x, y

def up_crossing(input_paths, channel, ref_sig = 1):
    x, sig = get_masses_and_pvalues(input_paths[channel], value='significance')
    sig2 = sig[1:]
    sig1 = sig[:-1]
    crossings = (sig1<ref_sig) & (ref_sig<sig2)
    N_crossings = crossings.sum()
    X_crossings = x[:-1][crossings]
    print(channel, N_crossings, 'times down crossings, at', X_crossings)
    return dict(zip(x, sig)), N_crossings, X_crossings

def global_significance(local_sig, N_crossings, ref_sig = 1):
    import ROOT
    # reference: https://cds.cern.ch/record/1375842/files/ATL-PHYS-PUB-2011-011.pdf
    # CMS: https://cds.cern.ch/record/1406347/files/HIG-11-032-pas.pdf
    # p (global) = p0 (local) + N*exp( - (q0 - q_ref)/2.)
    # q0: test-statistics for local max significance, q0=Z0*Z0 asymptotically
    # q_ref: reference point, eg. 1sigma := ref_sig*ref_sig
    # N: up-crossing points at reference point q_ref (down corssing if looking at p-value plot)
    q0 = pow(local_sig, 2)
    plocal = ROOT.RooStats.SignificanceToPValue(local_sig);
    pglobal = (N_crossings) * exp(-(q0 - ref_sig*ref_sig) / 2.) + plocal;
    pglobal_error = sqrt(N_crossings) * exp(-(q0 - ref_sig*ref_sig) / 2.);

    sigglobal = ROOT.RooStats.PValueToSignificance(pglobal);
    sigglobal_error_up = sigglobal - ROOT.RooStats.PValueToSignificance(pglobal+pglobal_error);
    sigglobal_error_dn = ROOT.RooStats.PValueToSignificance(pglobal-pglobal_error) - sigglobal;
    print(f'''
Local p-value: {plocal}, significance: {local_sig}, N_crossings: {N_crossings}.
Global p-value: {pglobal} +/- {pglobal_error}, significance: {sigglobal} + {sigglobal_error_up} - {sigglobal_error_dn}.
    ''')
    return {'local_p': plocal, 'local_sig': local_sig, 'n_crossings': str(N_crossings), 'global_p': pglobal, 'global_p_err': pglobal_error, 'global_sig': sigglobal, 'global_sig_up': sigglobal_error_up, 'global_sig_dn': sigglobal_error_dn}

def get_global_pvalue(input_paths, save_as=None):
    global_results = {}
    global_config = {
        'bbbb': [1100],
        'bbtautau': [1000],
        'bbyy': [],
        'combined': [1000, 1100]
        }
    for channel in input_paths:
        x, y = get_masses_and_pvalues(input_paths[channel])
        masses = global_config[channel]
        for mass in masses:
            for ref_sig in [0, 1, 2]:
                local_sigs, N_crossings, X_crossings = up_crossing(input_paths, channel, ref_sig = ref_sig)
                print('='*10, 'Global mass range:', x[0], '--', x[-1], 'point', mass, '='*10)
                global_results['_'.join([channel, str(mass), str(ref_sig)])] = global_significance(local_sigs[mass], N_crossings, ref_sig = ref_sig)

    for mass in [1100]:
        for i in [0, 1, 2]:
            print('\SI{'+str(mass)+'}{\GeV}',
            '&',f'{{{i}}}',
            '&',global_results[f'combined_{mass}_{i}']['local_sig'],
            '&',global_results[f'combined_{mass}_{i}']['local_p'],
            '&',global_results[f'combined_{mass}_{i}']['n_crossings'],
            '&', global_results[f'combined_{mass}_{i}']['global_sig'],
            '&',global_results[f'combined_{mass}_{i}']['global_sig_up'],
            '&', global_results[f'combined_{mass}_{i}']['global_sig_dn'],
            '&',global_results[f'combined_{mass}_{i}']['global_p'],
            r'\\')

    if save_as is not None:
        with open(save_as, "w") as outfile:
            json.dump(global_results, outfile, indent = 2)
        print('Save to', save_as)

# With help from https://github.com/rateixei/PyATLASstyle/blob/master/PyATLASstyle.py
def drawATLASlabel(fig, ax, lumi = r'27.5$-$139', internal=True, reg_text=None, xmin=0.05, ymax=0.85,
                   fontsize_title=30, fontsize_label=15, line_spacing=1.2):
    '''
    Draws ATLAS label + other descriptive text

    Parameters
    ----------
    yr : str
        Year to use for lumi label (all is an option)
    internal : bool
        Whether to put internal label - doesn't work yet, to be fixed!
    xmin : float
        Min x location of ATLAS text
    ymax : float
        Max y location of ATLAS text
    fontsize_title : int
        ATLAS title font size
    fontsize_label : int
        Label text font size
    line_spacing : float
        Spacing between title and label text
    '''
    c = 'k'

    box0 = ax.text(xmin, ymax, 'ATLAS', transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='left',
            fontsize=fontsize_title, fontweight='bold', style='italic', c=c)
    box0_ext_tr = ax.transAxes.inverted().transform(box0.get_window_extent(renderer=fig.canvas.get_renderer()))

    ax.text(max(box0_ext_tr[1][0], 0.23), ymax, 'Preliminary' if args.p else 'Internal', transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='left',
            fontsize=fontsize_title, c=c)

    if xmin < 0.2:
        lumi_label = '$\\sqrt{\\mathrm{s}} = $13 TeV, %s fb$^{-1}$' % (lumi)
    else:
        lumi_label = '$\\sqrt{\\mathrm{s}} = $13 TeV'
        lumi_label += '\n'
        lumi_label += '%s fb$^{-1}$' % (lumi)


    full_label = lumi_label + '\n'+ reg_text

    label_ypos = ymax-(box0_ext_tr[1][1]-box0_ext_tr[0][1])*(len(full_label.split("\n"))*line_spacing)
    ax.text(xmin, label_ypos, full_label,
            transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='left',
            fontsize=fontsize_label, c=c)

def plot_local_pvalue(input_paths, color_maps=None, label_maps=None,
                         figsize=(9, 7), 
                         xlabel=r"$\mathrm{m}_\mathrm{X}$ [GeV]",
                         ylabel=r"Local $p_{0}$-value",
                         save_as=None):
    plt.clf()
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    if label_maps is None:
        label_maps = {channel:channel for channel in input_paths}
        
    for i, p in enumerate([0.5, 1.58655253931457074e-01, 2.27501319481792086e-02, 1.34989803163009588e-03, 0.000032]):
        plt.axhline(y=p, color='gray', linestyle='--')
        ax.text(210, p, f'{i} $\sigma$', color='gray', ha='left', va='bottom', fontsize=20)
    for channel in input_paths:
        x, y = get_masses_and_pvalues(input_paths[channel])
        color = color_maps[channel]
        label = label_maps[channel]
        ax.plot(x, y, marker='o', color=color, label=label, linewidth=3 if channel == 'combined' else 2, markersize = 6 if channel == 'combined' else 4, alpha=0.8)


    textlable = 'Spin-0'

    drawATLASlabel(fig, ax, lumi = r'126 '+u'\u2212'+' 139', internal=(False if args.p else True), reg_text=textlable, xmin=0.05, ymax=0.25, fontsize_title=24, fontsize_label=20, line_spacing=1.1)

    plt.xlabel(xlabel, fontsize=20, loc='right')
    plt.ylabel(ylabel, fontsize=20, loc='top')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(2e-5, 1.5)
    plt.legend(fontsize=19, loc='lower right', bbox_to_anchor=(0.98, 0.02), frameon=False)
    
    majorticks = [200, 300, 500, 1000, 2000, 3000, 5000]
    ax.set_xticks(majorticks)
    ax.set_xticklabels(majorticks)
    minorticks = list(np.arange(200, 300, 20)) + list(np.arange(200, 2000, 100)) + list(np.arange(2000, 3000, 500)) + list(np.arange(3000, 5000, 1000))
    ax.set_xticks(minorticks, minor=True)
    ax.set_xticklabels([], minor=True)
    ax.tick_params(axis="y", which="major", direction='in', right=True,length=10, width=1.5, labelsize=20)
    ax.tick_params(axis="y", which="minor", direction='in', right=True,length=6, width=1, labelsize=20)    
    ax.tick_params(axis="x", which="major", direction='in', top=True,length=10, width=1.5, labelsize=20)
    ax.tick_params(axis="x", which="minor", direction='in', top=True,length=6, width=1, labelsize=20)
    
    if save_as is not None:
        plt.savefig(save_as, format='pdf')
        print('Save to', save_as)
    return plt

def main(args):
    input = args.input + '/' + args.analysis
    # input_paths = {
    #     'bbbb': glob(f'{input}/bbbb/*pvalue*.json'),
    #     'bbtautau': glob(f'{input}/bbtautau/*pvalue*.json'),
    #     'bbyy': glob(f'{input}/bbyy/*pvalue*.json'),
    #     'combined': glob(f'{input}/combined/*pvalue*.json'),
    # }
    input_paths = {
        'bbbb': glob(f'{input}/bbbb/cache/*.json'),
        'bbtautau': glob(f'{input}/bbtautau/cache/*.json'),
        'bbyy': glob(f'{input}/bbyy/cache/*.json'),
        'combined': glob(f'{input}/combined/A-*-fullcorr/cache/*.json'),
    }

    if args.analysis != 'spin0':
        input_paths.pop('bbbb')
        print('significance:')
        for channel in input_paths:
            _, pvalue = get_masses_and_pvalues(input_paths[channel], 'significance')
            print(channel, pvalue[0])
        return

    color_maps = \
    {
        'combined': 'k',
        'bbbb': 'b',
        'bbtautau': '#008F00', # 'bbtautau:green',
        'bbyy': '#9A0EEA', # 'bbtautau:purple',
    }
    
    label_maps = \
    {
        'bbbb': r'$\mathrm{b\bar{b}b\bar{b}}$',
        'bbtautau': r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$',
        'bbyy': r'$\mathrm{b\bar{b}\gamma\gamma}$',
        'combined': 'Combined',
    }
    
    plot_local_pvalue(input_paths, color_maps, label_maps, 
                         save_as=f"{args.output}/{args.analysis}_local_pvalue{'_p' if args.p else ''}.pdf")

    get_global_pvalue(input_paths, save_as=f"{args.output}/{args.analysis}_global_pvalue.json")


if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mPlot pvalue.\033[0m")
    parser.add_argument('-a', '--analysis', type=str, choices=['nonres_mu', 'nonres_xsec', 'nonres', 'spin0'], default=None, required=True, help='Analysis type')
    parser.add_argument('-i', '--input', type=str, default=None, required=True, help='Path to JSON')
    parser.add_argument('-o', '--output', type=str, default='.', required=False, help='Output path')
    parser.add_argument('-p', action='store_true', default=False, required=False, help='')

    args = parser.parse_args()
    main(args)
