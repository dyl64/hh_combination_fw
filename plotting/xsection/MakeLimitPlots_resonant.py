#!/usr/bin/env python
# Rui Zhang 6.2020
# rui.zhang@cern.ch

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

base_path = '../../../output/v140invfb_20210531_obs2/limits/data-files/'

scenario_map = {
    'bbbb': 'spin0-bbbb.dat',
    'bbtautau': 'spin0-bbtautau.dat',
    'bbyy': 'spin0-bbyy.dat',
    'combined': 'spin0-combined-A-bbbb_bbtautau_bbyy-nocorr.dat'
}


unblind = True

data = {}
masses = {}
columns = {}
for scenario in scenario_map:
    data_1 = open(os.path.join(base_path, scenario_map[scenario])).readlines()
    data_2 = [i.strip().split() for i in data_1[1:]]
    data_3 = {i[0]:i[1:] for i in data_2}
    columns[scenario] = data_1[0].split()[1:]
    data_final = {float(k):{kk:vv for kk,vv in zip(columns[scenario], v)} for k,v in data_3.items()}
    masses[scenario] = sorted(list(data_final.keys()))
    data[scenario] = data_final


pois = {
    'xsec_NP_profiled': ('xsec', 'profiled'),
    'xsec_NP_nominal': ('xsec', 'nominal'),
    'mu_NP_profiled': ('mu', 'profiled'),
    'mu_NP_nominal': ('mu', 'nominal'),
}


signature = {
    'exp': 'expected',
    'obs': 'observed',
    'm2s': '-2sigma',
    'm1s': '-1sigma',
    'p1s': '+1sigma',
    'p2s': '+2sigma'
}
def extract_limits(source, poi, np_type):
    limits = {}
    buf = '{}_{{}}_NP_{}'.format(poi, np_type)
    for point in source:
        limits[point] = {}
        for sig in signature:
            limits[point][signature[sig]] = float(source[point][buf.format(sig)])
        limits[point]['-1sigma'] = limits[point]['expected'] - limits[point]['-1sigma']
        limits[point]['-2sigma'] = limits[point]['expected'] - limits[point]['-2sigma']
        limits[point]['+1sigma'] = limits[point]['expected'] + limits[point]['+1sigma']
        limits[point]['+2sigma'] = limits[point]['expected'] + limits[point]['+2sigma']
    return limits


df = {}
limit_bands = {}
for poi in pois:
    df[poi] = {}
    for scenario in scenario_map:
        limits = extract_limits(data[scenario], pois[poi][0], pois[poi][1])
        df[poi][scenario] = pd.DataFrame(limits).transpose()
for poi in df:
    limit_bands[poi] = {}
    for scenario in df[poi]:
        limit_bands[poi][scenario] = {index: df[poi][scenario][index].values for index in df[poi][scenario]}


def plot_limit_band(limits, x, major='combined', name='limit_bands', ylimits=(5e-4, 10), ratio_ylimit=(0.9, 100), out_dir='plots'):

    color_map = {
        'bbbb': 'b--',
        'bbtautau': 'm--',
        'bbyy': 'r--',
        'combined': 'k-'
    }
    
    leg = {
        'bbbb'  : r'$b\bar{b}b\bar{b}$ (exp.)',
        'bbtautau': r'$b\bar{b}\tau^+\tau^-$ (exp.)',
        'bbyy': r'$b\bar{b}\gamma\gamma$ (exp.)',
        'combined': r'Combined (exp.)',
        '1sigma_band': r'Comb. $\pm 1\sigma$ (exp.)',
        '2sigma_band': r'Comb. $\pm 2\sigma$ (exp.)'
    }

    # define figure sizes
    plt.clf()
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    
    for scenario in limits:
        # define axis label
        label= leg[scenario]
        ax.semilogy(x[scenario], limits[scenario]['expected'], color_map[scenario],label=label, linewidth=3)
        if unblind:
            ax.semilogy(x[scenario], limits[scenario]['observed'], color_map[scenario],label=label, linewidth=3)
    # Here the +- 1, 2 sigma bands will be from the "major" expected limit
    ax.fill_between(x[major], np.array(limits[major]['-2sigma']), np.array(limits[major]['+2sigma']),
                    facecolor = 'yellow', label=leg['1sigma_band'])
    ax.fill_between(x[major], np.array(limits[major]['-1sigma']), np.array(limits[major]['+1sigma']),
                    facecolor = 'lime',  label=leg['2sigma_band'])
    
    # set y-limit for limit plots
    ax.set_ylim(*ylimits)
    
    # more axis decoration
    ax.set_ylabel(r'95% upper limit on $\sigma(X\rightarrow HH)$ [pb]', fontsize=20, loc='top')
    ax.set_xlabel(r'$m_S$[GeV]', fontsize=20, loc='right')
    stdText = r'$\mathbf{ATLAS}$ Internal'+'\n'
    stdText += r'$\sqrt{s} = $ 13 TeV, 139 fb$^{-1}$'+'\n'
    stdText += r'spin 0'

    ax.legend(loc='upper right', fontsize=20, bbox_to_anchor=(1.40, 1.02))
    ax.text(0.525,.955,stdText,ha='left',va='top',transform=ax.transAxes, fontsize=20)
    
    # format axis ticks
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(axis="y", which="major", direction='in', right=True,length=8, labelsize=15)
    ax.tick_params(axis="y", which="minor", direction='in', right=True,length=4, labelsize=15)    
    ax.tick_params(axis="x", which="major", direction='in', top=True,length=8, labelsize=15)
    ax.tick_params(axis="x", which="minor", direction='in', top=True,length=4, labelsize=15) 
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out_path = os.path.join(out_dir, name)
    # save plots
    # plt.savefig('{}.pdf'.format(out_path),dpi=300, bbox_inches = "tight")
    plt.savefig('{}.pdf'.format(out_path), bbox_inches = "tight")
    return plt

plot_limit_band(limit_bands['xsec_NP_profiled'], masses, name='limit_bands_xsec_NP_profiled')


plot_limit_band(limit_bands['xsec_NP_profiled'], masses, name='limit_bands_xsec_NP_nominal')