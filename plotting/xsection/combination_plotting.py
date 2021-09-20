#!/usr/bin/env python
# Rui Zhang 6.2021
# rui.zhang@cern.ch

from datetime import datetime
from os import makedirs, path, remove
import sys
from argparse import ArgumentParser
import uproot
import pandas as pd
import numpy as np
import json
from pdb import set_trace
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from color import *
from matplotlib import rcParams
rcParams['axes.linewidth'] = 1.5
rcParams['font.sans-serif'] = "Arial"
rcParams['font.family'] = "sans-serif"
rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

columns = ['xsec_m2s_NP_profiled', 'xsec_m1s_NP_profiled', 'xsec_p1s_NP_profiled', 'xsec_p2s_NP_profiled', 'xsec_exp_NP_profiled', 'xsec_obs_NP_profiled', 'exp_stat', 'obs_stat'] # don't change order

scenario_map = {
    # f'{args.command}-bbbb.dat': (r'$\mathrm{b\bar{b}b\bar{b}}$', 1),
    # f'{args.command}-bbtautau.dat': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$', 2),
    # f'{args.command}-bbyy.dat': (r'$\mathrm{b\bar{b}\gamma\gamma}$', 3),
    # f'{args.command}-bbll.dat': (r'$\mathrm{b\bar{b}ll}$', 4),
    # f'{args.command}-bbVV.dat': (r'$\mathrm{b\bar{b}VV}$', 5),
    # f'{args.command}-WWWW.dat': (r'$\mathrm{Multilepton}$', 6),
    # f'{args.command}-combined-A-bbtautau_bbyy-nocorr.dat': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-} + b\bar{b}\gamma\gamma}$', 11),
    # f'{args.command}-combined-A-bbbb_bbtautau_bbyy-nocorr.dat': ('Top 3 combined', 12),
    # f'{args.command}-combined-A-bbbb_bbll_bbtautau_bbyy-nocorr.dat': ('Top 3 + '+r'$\mathrm{b\bar{b}ll}$', 13),
    # f'{args.command}-combined-A-bbbb_bbtautau_bbVV_bbyy-nocorr.dat': ('Top 3 + '+r'$\mathrm{b\bar{b}VV}$', 14),
    # f'{args.command}-combined-A-bbbb_bbtautau_bbyy_WWWW-nocorr.dat': ('Top 3 + Multilepton', 15),
    # f'{args.command}-combined-A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr.dat': ('Top 4 + Multilepton', 16),
    # f'{args.command}-combined-A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-nocorr.dat': ('All 6 combined', 21),
    
    f'combined': ('Combined', 1, 'black'),
    f'Combined1': ('Combined', 1, 'black'),
    f'Combined2': ('dummy', 1, 'black'),
    f'Combined3': ('dummy', 1, 'black'),
    f'combined36': (r'Combined' + '\n' + r'27.5$-$36.1 fb$^{-1}$', 1, 'black'),
    f'bbbb': (r'$\mathrm{b\bar{b}b\bar{b}}$', 11, 'b'),
    f'bbtautau': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$', 12, '#9A0EEA'),
    f'bbtautau139': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$'+'\n' + r'139 fb$^{-1}$', 12, 'hdbs:starcommandblue'),
    f'bbtautau_resolved': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$ (resolved)', 12, 'hh:medturquoise'),
    f'bbtautau_boosted': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$ (boosted)', 12, 'hh:darkgreen'),
    f'bbtautau_boosted2': ('dummy', 12, 'hh:darkgreen'),
    f'bbtautau_boosted3': ('dummy', 12, 'hh:darkgreen'),
    f'bbyy': (r'$\mathrm{b\bar{b}\gamma\gamma}$', 13, 'hh:darkpink'),
    f'bbyy139': (r'$\mathrm{b\bar{b}\gamma\gamma}$'+'\n' + r'139 fb$^{-1}$', 13, 'r'),
    f'bbll': (r'$\mathrm{b\bar{b}ll}$', 14, 'darkcryan'),
    f'bbVV': (r'$\mathrm{b\bar{b}VV}$', 15, 'darkorange'),
    f'WWWW': (r'$\mathrm{Multilepton}$', 16, 'orangered'),
    f'bbWW': (r'$\mathrm{b\bar{b}WW}$', 17, 'orangered'),
    f'bbWW2l': (r'$\mathrm{b\bar{b}\ell^{+}\nu \ell^{-}\nu}$'+'\n' + r'139 fb$^{-1}$', 17, 'orangered'),
    f'A-bbtautau_bbyy-nocorr': ('Combined', 21, 'black'),
    f'A-bbbb_bbtautau_bbyy-nocorr': ('Top 3 combined', 22, 'black'),
    f'A-bbbb_bbll_bbtautau_bbyy-nocorr': ('Top 3 + '+r'$\mathrm{b\bar{b}ll}$', 23, 'black'),
    f'A-bbbb_bbtautau_bbVV_bbyy-nocorr': ('Top 3 + '+r'$\mathrm{b\bar{b}VV}$', 24, 'black'),
    f'A-bbbb_bbtautau_bbyy_WWWW-nocorr': ('Top 3 + Multilepton', 25, 'black'),
    f'A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr': ('Top 4 + Multilepton', 26, 'black'),
    f'A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-nocorr': ('All 6 combined', 41, 'black'),
    f'A-bbbb_bbtautau_bbVV_bbyy_WWWW-nocorr': ('N - '+r'$\mathrm{b\bar{b}ll}$', 31, 'black'),
    f'A-bbbb_bbll_bbtautau_bbyy_WWWW-nocorr': ('N - '+r'$\mathrm{b\bar{b}VV}$', 32, 'black'),
    f'A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr': ('N - '+r'Multilepton', 33, 'black'),
    #f'A-bbtautau_bbyy-fullcorr': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}'+'\n'+r'+ b\bar{b}\gamma\gamma}$', 21, 'black'),
    f'A-bbtautau_bbyy-fullcorr': ('Combined', 21, 'black'),
    f'A-bbbb_bbtautau_bbyy-fullcorr': ('Top 3 combined', 22, 'black'),
    f'A-bbbb_bbll_bbtautau_bbyy-fullcorr': ('Top 3 + '+r'$\mathrm{b\bar{b}ll}$', 23, 'black'),
    f'A-bbbb_bbtautau_bbVV_bbyy-fullcorr': ('Top 3 + '+r'$\mathrm{b\bar{b}VV}$', 24, 'black'),
    f'A-bbbb_bbtautau_bbyy_WWWW-fullcorr': ('Top 3 + Multilepton', 25, 'black'),
    f'A-bbbb_bbll_bbtautau_bbVV_bbyy-fullcorr': ('Top 4 + Multilepton', 26, 'black'),
    f'A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-fullcorr': ('All 6 combined', 41, 'black'),
    f'A-bbbb_bbtautau_bbVV_bbyy_WWWW-fullcorr': ('N - '+r'$\mathrm{b\bar{b}ll}$', 31, 'black'),
    f'A-bbbb_bbll_bbtautau_bbyy_WWWW-fullcorr': ('N - '+r'$\mathrm{b\bar{b}VV}$', 32, 'black'),
    f'A-bbbb_bbll_bbtautau_bbVV_bbyy-fullcorr': ('N - '+r'Multilepton', 33, 'black'),

}


def polish_ax(args, ax, fontsize):
    # Set frequency of ticks
    ax.tick_params(direction='out', length=10, width=1.5, colors='k', which='major')
    ax.tick_params(direction='out', length=6, width=1, colors='k', which='minor')

    # Add space between ticklabel and axis
    ax.tick_params(axis='x', which='major', pad=10)

    # Style of ticks
    ax.tick_params(which='both', top='on', right='on', left='off', direction='in', labelsize=fontsize)


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

    ax.text(max(box0_ext_tr[1][0], 0.25), ymax, 'Preliminary' if args.p else 'Internal', transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='left',
            fontsize=fontsize_title, c=c)

    if xmin < 0.2:
        lumi_label = '$\\sqrt{s} = $13 TeV, %s fb$^{-1}$' % (lumi)
    else:
        lumi_label = '$\\sqrt{s} = $13 TeV'
        lumi_label += '\n'
        lumi_label += '%s fb$^{-1}$' % (lumi)


    full_label = lumi_label + '\n'+ reg_text

    label_ypos = ymax-(box0_ext_tr[1][1]-box0_ext_tr[0][1])*(len(full_label.split("\n"))*line_spacing)
    ax.text(xmin, label_ypos, full_label,
            transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='left',
            fontsize=fontsize_label, c=c)

def corr_or_not(args):
    fullcorr = 0
    if args.dat_list:
        fullcorr += sum([1 for i in args.dat_list if 'fullcorr' in i])
    if 'com_list' in args:
        fullcorr += sum([1 for i in args.com_list if 'fullcorr' in i])
    return fullcorr

def save_plot(args):
    out_path = get_output_folder(args)
    if not path.exists(f'{out_path}'):
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mCreating new folder\033[0m'.rjust(40, ' '), out_path)
        makedirs(f'{out_path}')

    fullcorr = corr_or_not(args)
    new_method = 'csv' if args.csv_list or args.summary_json else 'json' if args.dat_list and args.dat_list[0].endswith('json') else 'dat'
    file_name = f'{out_path}/upperlimit_xsec_{args.command}_{new_method}_{"obs" if args.unblind else "exp"}_{"fullcorr" if fullcorr else "nocorr"}{"_mu" if args.mu else ""}.pdf'
    plt.savefig(file_name)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mSave file\033[0m'.rjust(40, ' '), file_name)


def get_output_folder(args):
    if args.dat_list:
        input_folder = (args.dat_list[0]).split('limits')
    elif args.csv_list:
        input_folder = (args.csv_list[0]).split('figures') if type(args.csv_list) == list else (args.csv_list).split('figures')
    elif args.summary_json:
        input_folder = (args.summary_json).split('figures')

    out_path = input_folder[0] + 'figures' if len(input_folder) > 1 else path.dirname(input_folder[0])
    return out_path


def rescale(df, columns, SM_HH_xsec = 31.05 / 1000, absolute=False):
    for c in columns:
        if c not in df: continue
        '''
            Results from json is (nonres) xxx fb, corresponding to mu = xxx / (SM_HH_xsec)
        '''
        df[c] = df[c] / SM_HH_xsec
    if not absolute:
        df['xsec_m2s_NP_profiled'] = df['xsec_exp_NP_profiled'] - df['xsec_m2s_NP_profiled']
        df['xsec_m1s_NP_profiled'] = df['xsec_exp_NP_profiled'] - df['xsec_m1s_NP_profiled']
        df['xsec_p2s_NP_profiled'] = df['xsec_exp_NP_profiled'] + df['xsec_p2s_NP_profiled']
        df['xsec_p1s_NP_profiled'] = df['xsec_exp_NP_profiled'] + df['xsec_p1s_NP_profiled']
    return df

def plot_spin0(args):
    ind_list = sorted(args.dat_list)
    com_list = args.com_list
    new_method = True if args.dat_list[0].endswith('json') else False

    ind_dfs = []
    ind_files = []
    com_dfs = []

    if new_method:
        dfs = []
        for dat in ind_list:
            with open(dat) as f:
                dfs.append(pd.DataFrame([json.load(f)]))
            file_name = path.basename(path.dirname(dat))
            dfs[-1]['parameter'] = float(path.basename(dat).split('.json')[0])
            dfs[-1]['channel'] = file_name
            dfs[-1] = dfs[-1].rename(columns={'-2': 'xsec_m2s_NP_profiled', '2': 'xsec_p2s_NP_profiled', '-1': 'xsec_m1s_NP_profiled', '1': 'xsec_p1s_NP_profiled', '0': 'xsec_exp_NP_profiled', 'obs': 'xsec_obs_NP_profiled'}).drop(columns=['inj'])
        
        dfs = pd.concat(dfs)
        ind_dfs = [group.sort_values(by = 'parameter', ascending = True) for _, group in dfs.groupby('channel')]

        for dat in com_list + ind_list:
            with open(dat) as f:
                com_dfs.append(pd.DataFrame([json.load(f)]))
            file_name = path.basename(path.dirname(dat))
            com_dfs[-1]['parameter'] = float(path.basename(dat).split('.json')[0])
            com_dfs[-1]['filename'] = file_name
            com_dfs[-1]['channels'] = file_name.split('-')[-2].replace('_', ', ') if 'A-' in file_name else file_name
            com_dfs[-1] = com_dfs[-1].rename(columns={'-2': 'xsec_m2s_NP_profiled', '2': 'xsec_p2s_NP_profiled', '-1': 'xsec_m1s_NP_profiled', '1': 'xsec_p1s_NP_profiled', '0': 'xsec_exp_NP_profiled', 'obs': 'xsec_obs_NP_profiled'}).drop(columns=['inj'])

    else:
        for dat in ind_list:
            ind_files.append(dat.split('/')[-1])
            ind_dfs.append(pd.read_table(dat, sep=' '))
            ind_dfs[-1] = rescale(ind_dfs[-1], columns, 0.001).sort_values(by = 'parameter', ascending = True)

        for dat in com_list + ind_list:
            file_name = path.basename(dat)
            com_dfs.append(pd.read_table(dat, sep=' '))
            com_dfs[-1] = rescale(com_dfs[-1], columns, 0.001).sort_values(by = 'parameter', ascending = True)
            com_dfs[-1]['filename'] = file_name
            com_dfs[-1]['channels'] = file_name.split('.')[-2].split('-')[-2].replace('_', ', ') if 'bb' in file_name.split('.')[-2].split('-')[-2] else file_name.split('.')[-2].split('-')[-1].replace('_', ', ')

    com_df_all = pd.concat(com_dfs)
    com_df_new = pd.DataFrame(columns=com_df_all.columns)

    if args.alter:
        exclude_masses = [425, 475]
    else:
        exclude_masses = [312.5, 337.5, 375, 425, 475]
    combine_result = {}
    # Construct the final limit frame that takes whatever the best expected limit
    for y, (index, row) in enumerate(com_df_all.iterrows()):
        identifier = row['parameter']
        if identifier in exclude_masses: continue
        identified = com_df_new.loc[com_df_new['parameter'] == identifier]
        # Append mass point if it is a new point or if it has lower expected limit
        if identifier not in set(com_df_new['parameter']):
            combine_result[identifier] = [row['filename']]
            com_df_new = com_df_new.append(row)
        elif row['xsec_exp_NP_profiled'] < identified['xsec_exp_NP_profiled'].values[0]:
            combine_result[identifier] = row['filename']
            com_df_new.loc[com_df_new['parameter'] == identifier, :] = row.values

    com_df_new['parameter'] = pd.to_numeric(com_df_new['parameter'])
    com_df_new = com_df_new.sort_values(by = 'parameter')
    com_df_new = rescale(com_df_new, columns, SM_HH_xsec = 0.001, absolute=True)
    print(com_df_new[columns[-3:-2] + ['parameter', 'filename', 'channels']])

    input_folder = (args.dat_list[0]).split('limits') if args.dat_list else (args.csv_list[0]).split('limits')
    out_path = input_folder[0] + 'figures' if len(input_folder) > 1 else 'figures'
    fullcorr = corr_or_not(args)
    com_df_new.to_csv(f'{out_path}/upperlimit_xsec_{args.command}_{"json" if new_method else "dat"}_{"obs" if args.unblind else "exp"}_{"fullcorr" if fullcorr else "nocorr"}_combined.csv', index=False)

    for df in ind_dfs:
        file_name = df.iloc[0]['channel']
        df.to_csv(f'{out_path}/upperlimit_xsec_{args.command}_{"json" if new_method else "dat"}_{"obs" if args.unblind else "exp"}_{"fullcorr" if fullcorr else "nocorr"}_{file_name}.csv', index=False)
        df = rescale(df, columns, SM_HH_xsec = 0.001, absolute=True)
        
    plot_spin0_from_df(args, ind_dfs+[com_df_new])



def plot_spin0_from_df(args, ind_dfs, reversed = False, references = None):
    com_df_new = ind_dfs.pop(-1)
    com_reference = references.pop(-1) if references else ''

    fontsize = 18
    textlable = 'Spin-0'

    fig, ax = plt.subplots(1, 1, figsize=(8, 7))

    # Set axis ranges
    if args.summary_json:
        ax.set_ylim([0.6, 200000])
        ax.set_xlim([230, 4000])
    else:
        ax.set_ylim([0.5, 20000])
        ax.set_xlim([230, 3500])

    def plot_individual():
        # Plot individual
        for ind_df in ind_dfs:
            reference = references.pop(0) if references else ''
            for file_name, df in ind_df.groupby('channel'):
                label = '' if args.unblind or scenario_map[file_name][0] == 'dummy' else scenario_map[file_name][0] + ' ' + reference
                ax.plot( 'parameter', 'xsec_exp_NP_profiled', data=df, color=scenario_map[file_name][2], linestyle='dashed', linewidth=2, zorder = 1.1, alpha=1, label = label)
                label = '' if scenario_map[file_name][0] == 'dummy' else scenario_map[file_name][0] + ' ' + reference
                ax.plot( 'parameter', 'xsec_obs_NP_profiled', data=df, color=scenario_map[file_name][2], linestyle='solid',  linewidth=2, zorder = 1.1, alpha=1, label = label)
                maxmass = max(df['parameter'])

                # Draw a vertical dash line to show where the channel stops
                if not reversed and maxmass < 6000:
                    def get_fraction(v):
                        a, b = ax.get_ylim()
                        a, b, v = np.log(a), np.log(b), np.log(v)
                        return (v-a) / (b-a)
                    #ax.axvline(x=maxmass, ymin=0, ymax=get_fraction(df[df['parameter'] == maxmass][['xsec_exp_NP_profiled', 'xsec_obs_NP_profiled']].values.max()), color=scenario_map[file_name][2], ls = '--', lw=0.5, zorder = 1)
                if args.debug:
                    print(df)
                    for x,y in zip(df['parameter'].tolist(), df['xsec_obs_NP_profiled'].tolist()):
                        if x not in [1100]: continue
                        ax.axhline(y=y)
                        label = "{:.2f} %".format(y*100)
                        plt.annotate(label, # this is the text
                                (x,y), # these are the coordinates to position the label
                                textcoords="offset points", # how to position the text
                                xytext=(0,10), # distance from text to points (x,y)
                                ha='center')

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mPlotted individual channels\033[0m'.rjust(40, ' '), len(ind_dfs))


    def plot_combined():
        # Plot combined
        # Plot bands
        line, = ax.plot( 'parameter', 'xsec_exp_NP_profiled', data=com_df_new, color='k', linestyle='dashed', linewidth=2, zorder = 1.5, alpha=1, label = '' if args.unblind else 'Combined')
        if args.unblind:
            line, = ax.plot( 'parameter', 'xsec_obs_NP_profiled', data=com_df_new, color='k', linestyle='solid', linewidth=2, zorder = 1.5, alpha=1, label = 'Combined ' + com_reference)
        if not args.no_error:
            ax.fill_between(com_df_new['parameter'], com_df_new[columns[0]], com_df_new[columns[3]], facecolor = 'hh:darkyellow', label = r'Expected $\pm$ 2 $\sigma$')
            ax.fill_between(com_df_new['parameter'], com_df_new[columns[1]], com_df_new[columns[2]], facecolor = 'hh:lightturquoise', label = r'Expected $\pm$ 1 $\sigma$')

        if args.debug:
            for x,y in zip(com_df_new['parameter'].tolist(), com_df_new['xsec_obs_NP_profiled'].tolist()):
                # if x not in [1100]: continue
                # ax.axhline(y=y)
                label = "{:.2f} %".format(y*100)
                plt.annotate(label, # this is the text
                        (x,y), # these are the coordinates to position the label
                        textcoords="offset points", # how to position the text
                        xytext=(0,10), # distance from text to points (x,y)
                        ha='center')

    if reversed:
        plot_combined()
        plot_individual()
    else:
        plot_individual()
        plot_combined()

    ax.set_yscale('log')

    # Set log scale
    if args.logx:
        ax.set_xscale('log')
        # Set frequency
        majorticks = [200, 300, 500, 1000, 2000, 3000, 5000]
        if args.summary_json:
            majorticks.remove(5000)
        else:
            majorticks.remove(5000)
        ax.set_xticks(majorticks)
        ax.set_xticklabels(majorticks)
        minorticks = list(np.arange(200, 300, 20)) + list(np.arange(200, 2000, 100)) + (list(np.arange(2000, 3000, 500)) if args.summary_json else list(np.arange(2000, 3000, 500)))
        ax.set_xticks(minorticks, minor=True)
        ax.set_xticklabels([], minor=True)
    else:
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    polish_ax(args, ax, fontsize)

    # y-axis title
    ylabel = r'$\sigma$ ($\mathrm{pp} \rightarrow \mathrm{X} \rightarrow \mathrm{HH}$) [fb]'
    try:
        ax.set_ylabel(ylabel, loc='top', fontsize=fontsize)
    except:
        ax.set_ylabel(ylabel, horizontalalignment='right', x=1.0, fontsize=fontsize)

    # x-axis title
    xlabel = r'$\mathrm{m}_\mathrm{X}$ [GeV]'
    ax.set_xlabel(xlabel, horizontalalignment='right', x=1.0, fontsize=fontsize)


    plot_common(args, fig, ax, textlable, fontsize, fontsize-5 if args.summary_json else fontsize-3)
    save_plot(args)

def plot_nonres(args):
    args.command = 'nonres'
    dat_list = args.dat_list
    new_method = True if dat_list[0].endswith('json') else False

    dfs = []
    if new_method:
        for dat in dat_list:
            with open(dat) as f:
                dfs.append(pd.DataFrame([json.load(f)]))

            file_name = path.basename(path.dirname(dat))
            dfs[-1]['order'] = scenario_map[file_name][1]
            dfs[-1].set_index([[file_name] * dfs[-1].shape[0]], inplace=True)

        df = pd.concat(dfs)
        df = df.rename(columns={'-2': 'xsec_m2s_NP_profiled', '2': 'xsec_p2s_NP_profiled', '-1': 'xsec_m1s_NP_profiled', '1': 'xsec_p1s_NP_profiled', '0': 'xsec_exp_NP_profiled', 'obs': 'xsec_obs_NP_profiled'}).drop(columns=['inj'])
        if args.stat_list:
            for stat in args.stat_list:
                file_name = path.basename(path.dirname(stat))
                if file_name in df.index:
                    with open(stat) as f:
                        dic = json.load(f)
                        df.at[file_name, 'exp_stat'] = dic['0']
                        df.at[file_name, 'obs_stat'] = dic['obs']
                if file_name.replace('nocorr', 'fullcorr') in df.index:
                    file_name = file_name.replace('nocorr', 'fullcorr') 
                    with open(stat) as f:
                        df.at[file_name, 'exp_stat'] = json.load(f)['0']

    else:
        for dat in dat_list:
            file_name = dat.split('/')[-1]
            dfs.append(pd.read_table(dat, sep=' '))
            dfs[-1]['order'] = scenario_map[file_name][1]
            # set file name as index
            dfs[-1].set_index([[file_name] * dfs[-1].shape[0]], inplace=True)

        df = pd.concat(dfs)

    df = rescale(df, columns, args.norm / 1000, absolute=new_method).sort_values(by = 'order', ascending = False)
    plot_nonres_from_df(args, df)

    out_path = get_output_folder(args)
    fullcorr = corr_or_not(args)
    df.to_csv(f'{out_path}/upperlimit_xsec_{args.command}_{"json" if new_method else "dat"}_{"obs" if args.unblind else "exp"}_{"fullcorr" if fullcorr else "nocorr"}{"_mu" if args.mu else ""}.csv')
    if 'obs_stat' in df:
        print(df[columns])
    elif 'exp_stat' in df:
        print(df[columns][:-1])
    else:
        print(df[columns[:-2]])
    print('Cross section scaled back to', args.norm)
    print(df[['xsec_exp_NP_profiled', 'xsec_obs_NP_profiled']] * args.norm)

def plot_nonres_from_df(args, df):
    fig, ax = plt.subplots(1, 1, figsize=(8, 7))
    df = df.sort_values(by = 'order', ascending = False)

    ax.set_ylim([0, df.shape[0]*1.8])
    if args.summary_json or args.csv_list:
        ax.set_xlim([1.9, 300 if args.logx else 30])
    else:
        ax.set_xlim([1, 130 if args.logx else 30])
        if args.stat_list is None:
            ax.set_xlim([1, 70])
    fontsize = 18

    # Plot bands
    if args.summary_json or args.csv_list:
        obs_text_x, exp_text_x, exp_stat_text_x, ref_text_x = 110, 200, 700, 700
    else:
        obs_text_x, obs_stat_text_x, exp_text_x, exp_stat_text_x, ref_text_x = 16, 28, 50, 87.5, 40
        if args.stat_list is None:
            obs_text_x, exp_text_x = 20, 40
    y_shift = 0.73 if 'ref' in df else 0.5

    df = df.fillna('')
    for y, (index, row) in enumerate(df.iterrows()):
        if args.unblind:
            obs = row[columns[5]]
            ax.vlines(obs, y, y+1, colors = 'k', linestyles = 'solid', zorder = 1.1, label = 'Observed' if y==0 else '')
            ax.scatter(obs, y+0.5, s=50, c='k', marker='o', zorder = 1.1)
            obs_str = f'{obs:.1f}' if index not in ['combined36', 'bbWW2l'] else f'{obs:g}'
            ax.text(obs_text_x, y+y_shift, obs_str, horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
        exp = row[columns[4]]
        ax.vlines(exp, y, y+1, colors = 'k', linestyles = 'dotted', zorder = 1.1, label = 'Expected' if y==0 else '')
        ax.fill_betweenx([y,y+1], row[columns[0]], row[columns[3]], facecolor = 'hh:darkyellow', label = r'Expected $\pm$ 2 $\sigma$' if y==0 else '')
        ax.fill_betweenx([y,y+1], row[columns[1]], row[columns[2]], facecolor = 'hh:lightturquoise', label = r'Expected $\pm$ 1 $\sigma$' if y==0 else '')

        # Plot limit text
        exp_str = f'{exp:.1f}' if index not in ['combined36', 'bbWW2l'] else f'{exp:g}'
        ax.text(exp_text_x, y+y_shift, exp_str, horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
        if 'ref' in df:
            ref = row['ref'].replace('\\n', '\n')
            ax.text(obs_text_x*1.2, y+1.1-y_shift, ref, horizontalalignment='center', verticalalignment='center', fontsize=fontsize-8)
        if 'exp_stat' in df:
            exp_stat_str = row['exp_stat']
            if isinstance(exp_stat_str , (int, float)):
                exp_stat_str = f'({exp_stat_str:.1f})'
            ax.text(exp_stat_text_x, y+1-y_shift, exp_stat_str, horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
        if 'obs_stat' in df:
            obs_stat_str = row['obs_stat']
            if isinstance(obs_stat_str , (int, float)):
                obs_stat_str = f'({obs_stat_str:.1f})'
            ax.text(obs_stat_text_x, y+1-y_shift, obs_stat_str, horizontalalignment='center', verticalalignment='center', fontsize=fontsize)

    if args.unblind:
        ax.text(obs_text_x*1.05, (y + 1)*1.1, 'Obs.', horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
        if 'obs_stat' in df:
            ax.text(obs_stat_text_x, (y + 1)*1.1, '(stat.)', horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
    ax.text(exp_text_x*1.05, (y + 1)*1.1, 'Exp.', horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
    if 'exp_stat' in df:
        ax.text(exp_stat_text_x, (y + 1)*1.1, '(stat.)', horizontalalignment='center', verticalalignment='center', fontsize=fontsize)

    textlable = ''

    # Plot horizontal lines
    ax.axhline(df.shape[0] - df[df['order'] < 10].shape[0], color = 'k', ls = '--', lw=0.5)
    ax.axhline(df.shape[0] - df[df['order'] < 20].shape[0], color = 'k', ls = '--', lw=0.5)

    # Add y tick in middle and process name as ticklabel
    ax.set_yticks(np.arange(df.shape[0])+0.5)
    ax.set_yticklabels([scenario_map[i][0] for i in df.index.to_list()], horizontalalignment='right')
    # Set log scale
    if args.logx:
        ax.set_xscale('symlog')
        # Set frequency
        if args.summary_json or args.csv_list:
            majorticks = [1, 2, 5, 10, 20, 50, 100, 200]
            ax.set_xticks(majorticks)
            ax.set_xticklabels(majorticks)
            ax.xaxis.set_minor_locator(ticker.LogLocator(base=10,subs=np.arange(10)))
        else:
            #majorticks = [2, 5, 10, 20, 50]
            #ax.set_xticks(majorticks)
            #ax.set_xticklabels(majorticks)
            ax.xaxis.set_major_locator(ticker.LogLocator())
            ax.xaxis.set_major_formatter(ticker.LogFormatter())
            ax.xaxis.set_minor_locator(ticker.LogLocator(base=10,subs=np.arange(10)))
    else:
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(20))
    polish_ax(args, ax, fontsize)
    
    # Add legend
    positions = (0.04, 0.8)
    if args.norm == 31.05:
        process = 'ggF'
    elif args.norm == 31.05 + 1.726:
        process = 'ggF+VBF'

    # x-axis title
    xlabel = '95% ' + r'CL upper limit on $\sigma_{\mathrm{%s}}$ ($\mathrm{pp} \rightarrow \mathrm{HH}$)''\n'r'normalised to $\sigma^\mathrm{{SM}}_\mathrm{{%s}}$' % (process, process)
    if args.summary_json or args.csv_list:
        xlabel = '95% ' + r'CL upper limit on $\sigma$ ($\mathrm{pp} \rightarrow \mathrm{HH}$) normalised to $\sigma_{\mathrm{SM}}$'
    if args.mu:
        xlabel = '95% ' + r'CL upper limit on signal strength'
    ax.set_xlabel(xlabel, horizontalalignment='right', x=1.0, fontsize=fontsize)

    if not (args.summary_json or args.csv_list):
        textlable = r'$\mathrm{\sigma_{%s}^{SM}}$ = %.2f fb' % (process, args.norm)
        if corr_or_not(args) == 0:
            textlable += '\nnocorr'

    plot_common(args, fig, ax, textlable, fontsize, fontsize)
    save_plot(args)

def bold_edge(inputs=None):
    import matplotlib.patches as patches
    handles,labels = plt.gca().get_legend_handles_labels() if inputs is None else inputs
    for i, (handle,label) in enumerate(zip(handles,labels)):
        if r'\sigma$' in label:
            border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)
            handles.insert(i, (handle, border_leg))
            handles.pop(i+1)
    ''' Swap 1 and 2 sigma band '''
    handles[-1], handles[-2] = handles[-2], handles[-1]
    labels[-1], labels[-2] = labels[-2], labels[-1]
    return handles,labels


def plot_common(args, fig, ax, textlable, fontsize, legendsize):
    # ATLAS cosmetics
    if args.command == 'nonres':
        drawATLASlabel(fig, ax, lumi = r'27.5$-$139' if (args.summary_json or args.csv_list) else r'139', internal=True, reg_text=textlable, xmin=0.05, ymax=0.9, fontsize_title=24, fontsize_label=fontsize-1, line_spacing=1.1)
    elif args.command == 'spin0':
        drawATLASlabel(fig, ax, lumi = r'27.5$-$139' if (args.summary_json or args.csv_list) else r'126$—$139', internal=True, reg_text=textlable, xmin=0.04 if args.summary_json else 0.2, ymax=0.9, fontsize_title=24, fontsize_label=fontsize-1, line_spacing=0.8)

    # Legend
    if args.command == 'nonres':
        handles,labels = bold_edge()
        plt.legend(handles,labels, bbox_to_anchor=(1., 1), ncol=1, framealpha=0., prop={'size': legendsize})

    elif args.command == 'spin0':
        new_handlers, new_labels = [], []
        current_handles, current_labels = plt.gca().get_legend_handles_labels()
        
        if args.unblind:
            import matplotlib.lines as mlines
            obs_line = mlines.Line2D([], [], color='k', ls = '-', label='Observed')
            exp_line = mlines.Line2D([], [], color='k', ls = '--', label='Expected')
            style_legend = plt.legend(handles=[obs_line, exp_line], bbox_to_anchor=(0.02, 0.15), loc='upper left', ncol=1, framealpha=0., prop={'size': legendsize})
            # Add the legend manually to the current Axes.
            plt.gca().add_artist(style_legend)

        for handler, label in zip(current_handles, current_labels):
            if 'Remove' not in label:
                new_handlers.append(handler)
                new_labels.append(label)
        new_handlers, new_labels = bold_edge((new_handlers, new_labels))
        plt.legend(new_handlers, new_labels, bbox_to_anchor=(0.99, 0.99),  loc='upper right', ncol=1, framealpha=0., prop={'size': legendsize})

    plt.tight_layout()
    plt.plot()


def main(args):
    if args.command == 'nonres':
        if args.csv_list:
            df = pd.read_csv(args.csv_list, index_col=0)
            plot_nonres_from_df(args, df)
        else:
            plot_nonres(args)
    elif args.command == 'spin0':
        if args.csv_list:
            ind_dfs = []
            for csv in args.csv_list:
                if csv.endswith('combined.csv'):
                    com_df_new = pd.read_csv(csv)
                    if args.relative:
                        com_df_new = rescale(com_df_new, columns, SM_HH_xsec = 0.001, absolute=False)
                else:
                    ind_dfs.append(pd.read_csv(csv))
            plot_spin0_from_df(args, ind_dfs + [com_df_new])
        elif args.summary_json:
            with open(args.summary_json) as f:
                summary_spec = json.load(f)
                ind_dfs = []
                references = []
                for k, v in summary_spec.items():
                    if v[0].endswith('combined.csv'):
                        references.append(v[-1])
                        com_df_new = []
                        for csv in v[:-1]:
                            com_df_new.append(pd.read_csv(csv))
                        com_df_new = pd.concat(com_df_new)
                        if args.relative:
                            com_df_new = rescale(com_df_new, columns, SM_HH_xsec = 0.001, absolute=False)
                    else:
                        references.append(v[-1])
                        ind_df = []
                        for csv in v[:-1]:
                            ind_df.append(rescale(pd.read_csv(csv), columns, SM_HH_xsec = 0.001, absolute=False))
                        ind_dfs.append(pd.concat(ind_df))
                plot_spin0_from_df(args, ind_dfs + [com_df_new], reversed = True, references=references)
        else:
            plot_spin0(args)


if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mPlot combined plots.\033[0m")
    subcommands = parser.add_subparsers(dest='command')

    nonres = subcommands.add_parser('nonres', help='Plot nonres.')
    nonres.add_argument('nonres', nargs='*')
    inputs = nonres.add_mutually_exclusive_group(required=True)
    inputs.add_argument('-l', '--dat_list', nargs='+', type=str, default=None, required=False, help='')
    inputs.add_argument('--csv_list', type=str, default=None, required=False, help='')
    inputs.add_argument('--summary_json', type=str, default=None, required=False, help='')
    nonres.add_argument('-s', '--stat_list', nargs='+', type=str, default=None, required=False, help='')
    nonres.add_argument('--logx', action='store_true', default=False, required=False, help='')
    nonres.add_argument('--norm', type=float, default=32.776, required=False, help='')
    nonres.add_argument('--unblind', action='store_true', default=False, required=False, help='')
    nonres.add_argument('-p', action='store_true', default=False, required=False, help='')
    nonres.add_argument('-mu', action='store_true', default=False, required=False, help='Plot limit on signal strength instead of on cross section')

    spin0 = subcommands.add_parser('spin0', help='Plot spin0.')
    spin0.add_argument('spin0', nargs='*')
    inputs = spin0.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--csv_list', nargs='+', type=str, default=None, required=False, help='')
    inputs.add_argument('--dat_list', nargs='+', type=str, default=None, required=False, help='')
    inputs.add_argument('--summary_json', type=str, default=None, required=False, help='')
    spin0.add_argument('--com_list', nargs='+', type=str, default=['../data-files/spin0-combined-A-bbbb_bbtautau-nocorr.dat', '../data-files/spin0-combined-A-bbtautau_bbyy-nocorr.dat', '../data-files/spin0-combined-A-bbbb_bbtautau_bbyy-nocorr.dat'], required=False, help='')
    spin0.add_argument('--logx', action='store_true', default=False, required=False, help='')
    spin0.add_argument('--unblind', action='store_true', default=True, required=False, help='')
    spin0.add_argument('--debug', action='store_true', default=False, required=False, help='')
    spin0.add_argument('--relative', action='store_true', default=False, required=False, help='')
    spin0.add_argument('--no-error', action='store_true', default=False, required=False, help='')
    spin0.add_argument('-p', action='store_true', default=False, required=False, help='')
    spin0.add_argument('-mu', action='store_true', default=False, required=False, help='Plot limit on signal strength instead of on cross section')
    spin0.add_argument('-alter', action='store_true', default=False, required=False, help='Add ')

    args = parser.parse_args()
    main(args)
