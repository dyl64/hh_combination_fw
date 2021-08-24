#!/usr/bin/env python
# Rui Zhang / Alkaid Cheng 8.2021
# rui.zhang@cern.ch
# chi.lung.cheng@cern.ch

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from pdb import set_trace

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

DEFAULT_COLOR_WHEELS = ['k', 'r', 'b', 'g', 'c']

def get_xy(path, threshold):
    data = {k:v for k,v in json.load(open(path)).items() if abs(v) < threshold}
    X = np.array(list(data.keys()), dtype=float)
    Y = np.array(list(data.values()))
    indices = np.argsort(X)
    x = X[indices]
    y = Y[indices]
    return x, y

def plot_likelihood_scan(input_paths, color_maps=None, label_maps=None,
                         threshold=5., figsize=(12, 8), 
                         text='',
                         xlabel=r"$\kappa_\lambda$",
                         ylabel=r"-2ln($\Lambda$)",
                         save_as=None):
    plt.clf()
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    if color_maps is None:
        color_wheel = DEFAULT_COLOR_WHEELS.copy()
        color_wheel.reverse()
        color_maps = {}
        for channel in input_paths:
            color_maps[channel] = color_wheel.pop()
    if label_maps is None:
        label_maps = {channel:channel for channel in input_paths}
        
    channel_data = {}
    for channel in input_paths:
        x, y = get_xy(input_paths[channel], threshold=threshold)
        color = color_maps[channel]
        label = label_maps[channel]
        ax.plot(x, y, color=color, label=label, linewidth=2)
    ax.text(0.125, 1.02, text, ha='left', va='top', transform=ax.transAxes, fontsize=20)
    plt.axhline(y=1, color='gray', linestyle='--')
    plt.axhline(y=4, color='gray', linestyle='--')
    plt.xlabel(xlabel, fontsize=20, loc='right')
    plt.ylim(0, threshold)
    plt.ylabel(ylabel, fontsize=20, loc='top')
    plt.legend(fontsize=15, loc='upper right', bbox_to_anchor=(0.95, 0.4))
    
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(axis="y", which="major", direction='in', right=True,length=8, labelsize=15)
    ax.tick_params(axis="y", which="minor", direction='in', right=True,length=4, labelsize=15)    
    ax.tick_params(axis="x", which="major", direction='in', top=True,length=8, labelsize=15)
    ax.tick_params(axis="x", which="minor", direction='in', top=True,length=4, labelsize=15)
    
    if save_as is not None:
        plt.savefig(save_as)
        print('Save to', save_as)
    return plt

def main(args):

    input_paths = \
    {
        'combined': args.input + '/' + args.combined,
        'bbtautau': args.input + '/' + args.bbtt,
        'bbyy': args.input + '/' + args.bbyy,
    }
    if args.bbbb:
        input_paths['bbbb'] = args.input + '/' + args.bbbb

    color_maps = \
    {
        'combined': 'k',
        'bbtautau': '#9A0EEA',
        'bbyy': 'r',
        'bbbb': 'b',
    }
    
    label_maps = \
    {
        'combined': 'Combined',
        'bbtautau': r'$bb\tau\tau$',
        'bbyy': r'$bb\gamma\gamma$',
        'bbbb': r'$bbbb$',
    }
    
    text = \
    """
    $\mathbf{ATLAS}$ Internal
    $\sqrt{s} = $ 13 TeV, 139 fb$^{-1}$
    """ + f"""Spin-0 {args.mass} GeV
    """ if args.analysis == 'spin0' else """
    $\mathbf{ATLAS}$ Internal
    $\sqrt{s} = $ 13 TeV, 139 fb$^{-1}$
    Non resonant
    """
    
    plot_likelihood_scan(input_paths, color_maps, label_maps, threshold=5, text=text,
                         xlabel=r"$\sigma_{ggF+VBF}(pp\rightarrow HH)$ [fb]",
                         save_as=f"{args.output}/{args.analysis}_{args.mass}.pdf")

if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mPlot likelihood.\033[0m")
    parser.add_argument('-a', '--analysis', type=str, choices=['nonres', 'spin0'], default=None, required=True, help='Analysis type')
    parser.add_argument('-i', '--input', type=str, default=None, required=False, help='Path to JSON')
    parser.add_argument('-c', '--combined', type=str, default=None, required=True, help='Filename of combined')
    parser.add_argument('-t', '--bbtt', type=str, default=None, required=False, help='Filename of bbtautau')
    parser.add_argument('-y', '--bbyy', type=str, default=None, required=False, help='Filename of bbyy')
    parser.add_argument('-b', '--bbbb', type=str, default=None, required=False, help='Filename of bbbb')
    parser.add_argument('-m', '--mass', type=int, default=0, required=False, help='Mass for spin-0')
    parser.add_argument('-o', '--output', type=str, default='.', required=False, help='Output path')

    args = parser.parse_args()
    if args.analysis == 'nonres' and args.bbbb is not None:
        assert(0), f'{args.analysis} does not support bbbb'
    if args.analysis == 'spin0' and args.mass == 0:
        assert(0), f'--mass required in {args.analysis}'

    main(args)
