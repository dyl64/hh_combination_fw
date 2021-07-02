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
import pdb
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
rcParams['axes.linewidth'] = 1.5
rcParams['font.sans-serif'] = "Arial"
rcParams['font.family'] = "sans-serif"
rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

columns = ['xsec_m2s_NP_profiled', 'xsec_m1s_NP_profiled', 'xsec_p1s_NP_profiled', 'xsec_p2s_NP_profiled', 'xsec_exp_NP_profiled', 'xsec_obs_NP_profiled'] # don't change order

def polish_ax(args, ax, fontsize):
    # Set frequency of ticks
    ax.tick_params(direction='out', length=6, width=1.5, colors='k', which='major')
    ax.tick_params(direction='out', length=4, width=1, colors='k', which='minor')

    # Add space between ticklabel and axis
    ax.tick_params(axis='x', which='major', pad=10)

    # Style of ticks
    ax.tick_params(which='both', top='on', right='on', left='off', direction='in', labelsize=fontsize)


# With help from https://github.com/rateixei/PyATLASstyle/blob/master/PyATLASstyle.py
def drawATLASlabel(fig, ax, internal=True, reg_text=None, xmin=0.05, ymax=0.85,
                   fontsize_title=23, fontsize_label=14, line_spacing=1.2):
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

    box1 = ax.text(box0_ext_tr[1][0], ymax, "  ",
                   verticalalignment='bottom', transform=ax.transAxes,
                   fontsize=fontsize_title, c=c)
    box1_ext_tr = ax.transAxes.inverted().transform(box1.get_window_extent(renderer=fig.canvas.get_renderer()))

    ax.text(box1_ext_tr[1][0], ymax, 'Internal', transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='left',
            fontsize=fontsize_title, c=c)

    lumi_label = '$\\sqrt{s} = $13 TeV, %s fb$^{-1}$' % (r'126$-$139')


    full_label = lumi_label + '\n'+ reg_text

    label_ypos = ymax-(box0_ext_tr[1][1]-box0_ext_tr[0][1])*(len(full_label.split("\n"))*line_spacing)
    ax.text(xmin, label_ypos, full_label,
            transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='left',
            fontsize=fontsize_label, c=c)


def save_plot(args):
    input_folder = (args.dat_list[0]).split('limits')
    out_path = input_folder[0] + 'figures' if len(input_folder) > 1 else 'figures'
    if not path.exists(f'{out_path}'):
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mCreating new folder\033[0m'.rjust(40, ' '), out_path)
        makedirs(f'{out_path}')

    new_method = 'json' if args.dat_list[0].endswith('json') else 'dat'
    file_name = f'{out_path}/upperlimit_xsec_{args.resonant_type}_{new_method}_{"obs" if args.unblind else "exp"}.pdf'
    plt.savefig(file_name)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mSave file\033[0m'.rjust(40, ' '), file_name)


def rescale(df, columns, SM_HH_xsec = 31.05 / 1000, absolute=False):
    for c in columns:
        df[c] = df[c] / SM_HH_xsec
    if not absolute:
        df['xsec_m2s_NP_profiled'] = df['xsec_exp_NP_profiled'] - df['xsec_m2s_NP_profiled']
        df['xsec_m1s_NP_profiled'] = df['xsec_exp_NP_profiled'] - df['xsec_m1s_NP_profiled']
        df['xsec_p2s_NP_profiled'] = df['xsec_exp_NP_profiled'] + df['xsec_p2s_NP_profiled']
        df['xsec_p1s_NP_profiled'] = df['xsec_exp_NP_profiled'] + df['xsec_p1s_NP_profiled']
    return df

def plot_spin0(args):
    args.resonant_type = 'spin0'
    ind_list = sorted(args.dat_list)
    com_list = args.com_list
    new_method = True if args.dat_list[0].endswith('json') else False

    scenario_map = {
        f'{args.resonant_type}-bbbb.dat': (r'$\mathrm{b\bar{b}b\bar{b}}$', 'b'),
        f'{args.resonant_type}-bbtautau.dat': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$', 'purple'),
        f'{args.resonant_type}-bbyy.dat': (r'$\mathrm{b\bar{b}\gamma\gamma}$', 'r'),
        f'{args.resonant_type}-bbll.dat': (r'$\mathrm{b\bar{b}ll}$', 'darkcryan'),
        f'{args.resonant_type}-bbVV.dat': (r'$\mathrm{b\bar{b}VV}$', 'darkorange'),
        f'{args.resonant_type}-WWWW.dat': (r'$\mathrm{Multilepton}$', 'orangered'),
        f'{args.resonant_type}-combined-A-bbtautau_bbyy-nocorr.dat': (r'$b\bar{b}\tau^{+}\tau^{-} + b\bar{b}\gamma\gamma$', 'black'),
        f'{args.resonant_type}-combined-A-bbbb_bbtautau_bbyy-nocorr.dat': ('Top 3 combined', 'black'),
        f'{args.resonant_type}-combined-A-bbbb_bbll_bbtautau_bbyy-nocorr.dat': ('Top 3' + r'$\mathrm{b\bar{b}ll}$', 'black'),
        f'{args.resonant_type}-combined-A-bbbb_bbtautau_bbVV_bbyy-nocorr.dat': ('Top 3' + r'$\mathrm{b\bar{b}VV}$', 'black'),
        f'{args.resonant_type}-combined-A-bbbb_bbtautau_bbyy_WWWW-nocorr.dat': ('Top 3 + Multilepton', 'black'),
        f'{args.resonant_type}-combined-A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr.dat': (r'Top 4 + Multilepton', 'black'),
        f'{args.resonant_type}-combined-A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-nocorr.dat': ('All 6 combined', 'black'),

        f'bbbb': (r'$\mathrm{b\bar{b}b\bar{b}}$', 'b'),
        f'bbtautau': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$', 'purple'),
        f'bbyy': (r'$\mathrm{b\bar{b}\gamma\gamma}$', 'r'),
        f'bbll': (r'$\mathrm{b\bar{b}ll}$', 'darkcryan'),
        f'bbVV': (r'$\mathrm{b\bar{b}VV}$', 'darkorange'),
        f'WWWW': (r'$\mathrm{Multilepton}$', 'orangered'),
        f'A-bbtautau_bbyy-nocorr': (r'$b\bar{b}\tau^{+}\tau^{-} + b\bar{b}\gamma\gamma$', 'black'),
        f'A-bbbb_bbtautau_bbyy-nocorr': ('Top 3 combined', 'black'),
        f'A-bbbb_bbll_bbtautau_bbyy-nocorr': ('Top 3 + $b\bar{b}ll$', 'black'),
        f'A-bbbb_bbtautau_bbVV_bbyy-nocorr': ('Top 3 + $b\bar{b}VV$', 'black'),
        f'A-bbbb_bbtautau_bbyy_WWWW-nocorr': ('Top 3 + Multilepton', 'black'),
        f'A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr': (r'Top 4 + Multilepton', 'black'),
        f'A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-nocorr': ('All 6 combined', 'black'),
    }

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
        ind_files = [i.iloc[0]['channel'] for i in ind_dfs]

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
            ind_dfs[-1] = rescale(ind_dfs[-1], columns, 1).sort_values(by = 'parameter', ascending = True)

        for dat in com_list + ind_list:
            file_name = path.basename(dat)
            com_dfs.append(pd.read_table(dat, sep=' '))
            com_dfs[-1] = rescale(com_dfs[-1], columns, 1).sort_values(by = 'parameter', ascending = True)
            com_dfs[-1]['filename'] = file_name
            com_dfs[-1]['channels'] = file_name.split('.')[-2].split('-')[-2].replace('_', ', ') if 'bb' in file_name.split('.')[-2].split('-')[-2] else file_name.split('.')[-2].split('-')[-1].replace('_', ', ')

    com_df_all = pd.concat(com_dfs)
    com_df_new = pd.DataFrame(columns=com_df_all.columns)

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
    print(com_df_new[columns[-2:] + ['parameter', 'filename', 'channels']])


    fontsize = 18
    textlable = 'Spin-0'

    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    # Set axis ranges
    ax.set_ylim([0.0005, 40])
    ax.set_xlim([230, 6000])

    # Plot individual
    for df, file_name in zip(ind_dfs, ind_files):
        ax.plot( 'parameter', 'xsec_exp_NP_profiled', data=df, color=scenario_map[file_name][1], linestyle='dashed', linewidth=2, zorder = 1.1, alpha=0.8, label = scenario_map[file_name][0] + ' (Exp.)')
        ax.plot( 'parameter', 'xsec_obs_NP_profiled', data=df, color=scenario_map[file_name][1], linestyle='solid',  linewidth=2, zorder = 1.1, alpha=0.8, label = scenario_map[file_name][0] + ' (Remove.)')
        maxmass = max(df['parameter'])

        # Draw a vertical dash line to show where the channel stops
        if maxmass < 6000:
            def get_fraction(v):
                a, b = ax.get_ylim()
                a, b, v = np.log(a), np.log(b), np.log(v)
                return (v-a) / (b-a)
            ax.axvline(x=maxmass, ymin=0, ymax=get_fraction(df[df['parameter'] == maxmass][['xsec_exp_NP_profiled', 'xsec_obs_NP_profiled']].values.max()), color=scenario_map[file_name][1], ls = '--', lw=0.5, zorder = 1)
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


    # Plot combined
    # Plot bands
    ax.plot( 'parameter', 'xsec_exp_NP_profiled', data=com_df_new, color='k', linestyle='dashed', linewidth=2, zorder = 1.5, alpha=0.8, label = 'Expected')
    if args.unblind:
        ax.plot( 'parameter', 'xsec_obs_NP_profiled', data=com_df_new, color='k', linestyle='solid', linewidth=2, zorder = 1.5, alpha=0.8, label = 'Observed')
    ax.fill_between(com_df_new['parameter'], com_df_new[columns[0]], com_df_new[columns[3]], facecolor = 'yellow', label = r'$\mathrm{Expected \pm 2 \sigma}$')
    ax.fill_between(com_df_new['parameter'], com_df_new[columns[1]], com_df_new[columns[2]], facecolor = 'lime', label = r'$\mathrm{Expected \pm 1 \sigma}$')

    if args.debug:
        for x,y in zip(com_df_new['parameter'].tolist(), com_df_new['xsec_obs_NP_profiled'].tolist()):
            if x not in [1100]: continue
            ax.axhline(y=y)
            label = "{:.2f} %".format(y*100)
            plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') 

    ax.set_yscale('log')

    # Set log scale
    if args.logx:
        ax.set_xscale('log')
        # Set frequency
        majorticks = [200, 300, 500, 1000, 2000, 3000, 5000]
        ax.set_xticks(majorticks)
        ax.set_xticklabels(majorticks)
        minorticks = list(np.arange(200, 300, 20)) + list(np.arange(200, 2000, 100)) + list(np.arange(2000, 5000, 1000))
        ax.set_xticks(minorticks, minor=True)
        ax.set_xticklabels([], minor=True)
    else:
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    polish_ax(args, ax, fontsize)

    # y-axis title
    ylabel = r'$\sigma$ ($\mathrm{pp} \rightarrow \mathrm{X} \rightarrow \mathrm{HH}$) [pb]'
    ax.set_ylabel(ylabel, horizontalalignment='left', x=1.0, fontsize=fontsize)

    # x-axis title
    xlabel = r'$\mathrm{m}_\mathrm{X}$ [GeV]'
    ax.set_xlabel(xlabel, horizontalalignment='right', x=1.0, fontsize=fontsize)


    plot_common(args, fig, ax, textlable, fontsize, fontsize-3)
    save_plot(args)


def plot_nonres(args):
    args.resonant_type = 'nonres'
    dat_list = args.dat_list
    new_method = True if dat_list[0].endswith('json') else False

    scenario_map = {
        f'{args.resonant_type}-bbbb.dat': (r'$\mathrm{b\bar{b}b\bar{b}}$', 1),
        f'{args.resonant_type}-bbtautau.dat': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$', 2),
        f'{args.resonant_type}-bbyy.dat': (r'$\mathrm{b\bar{b}\gamma\gamma}$', 3),
        f'{args.resonant_type}-bbll.dat': (r'$\mathrm{b\bar{b}ll}$', 4),
        f'{args.resonant_type}-bbVV.dat': (r'$\mathrm{b\bar{b}VV}$', 5),
        f'{args.resonant_type}-WWWW.dat': (r'$\mathrm{Multilepton}$', 6),
        f'{args.resonant_type}-combined-A-bbtautau_bbyy-nocorr.dat': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-} + b\bar{b}\gamma\gamma}$', 11),
        f'{args.resonant_type}-combined-A-bbbb_bbtautau_bbyy-nocorr.dat': ('Top 3 combined', 12),
        f'{args.resonant_type}-combined-A-bbbb_bbll_bbtautau_bbyy-nocorr.dat': ('Top 3 + '+r'$\mathrm{b\bar{b}ll}$', 13),
        f'{args.resonant_type}-combined-A-bbbb_bbtautau_bbVV_bbyy-nocorr.dat': ('Top 3 + '+r'$\mathrm{b\bar{b}VV}$', 14),
        f'{args.resonant_type}-combined-A-bbbb_bbtautau_bbyy_WWWW-nocorr.dat': ('Top 3 + Multilepton', 15),
        f'{args.resonant_type}-combined-A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr.dat': ('Top 4 + Multilepton', 16),
        f'{args.resonant_type}-combined-A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-nocorr.dat': ('All 6 combined', 21),
        
        f'bbbb': (r'$\mathrm{b\bar{b}b\bar{b}}$', 1),
        f'bbtautau': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$', 2),
        f'bbyy': (r'$\mathrm{b\bar{b}\gamma\gamma}$', 3),
        f'bbll': (r'$\mathrm{b\bar{b}ll}$', 4),
        f'bbVV': (r'$\mathrm{b\bar{b}VV}$', 5),
        f'WWWW': (r'$\mathrm{Multilepton}$', 6),
        f'A-bbtautau_bbyy-nocorr': (r'$\mathrm{b\bar{b}\tau^{+}\tau^{-} + b\bar{b}\gamma\gamma}$', 11),
        f'A-bbbb_bbtautau_bbyy-nocorr': ('Top 3 combined', 12),
        f'A-bbbb_bbll_bbtautau_bbyy-nocorr': ('Top 3 + '+r'$\mathrm{b\bar{b}ll}$', 13),
        f'A-bbbb_bbtautau_bbVV_bbyy-nocorr': ('Top 3 + '+r'$\mathrm{b\bar{b}VV}$', 14),
        f'A-bbbb_bbtautau_bbyy_WWWW-nocorr': ('Top 3 + Multilepton', 15),
        f'A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr': ('Top 4 + Multilepton', 16),
        f'A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-nocorr': ('All 6 combined', 31),
        f'A-bbbb_bbtautau_bbVV_bbyy_WWWW-nocorr': ('N - '+r'$\mathrm{b\bar{b}ll}$', 21),
        f'A-bbbb_bbll_bbtautau_bbyy_WWWW-nocorr': ('N - '+r'$\mathrm{b\bar{b}VV}$', 22),
        f'A-bbbb_bbll_bbtautau_bbVV_bbyy-nocorr': ('N - '+r'Multilepton', 23),

    }

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

    else:
        for dat in dat_list:
            file_name = dat.split('/')[-1]
            dfs.append(pd.read_table(dat, sep=' '))
            dfs[-1]['order'] = scenario_map[file_name][1]
            # set file name as index
            dfs[-1].set_index([[file_name] * dfs[-1].shape[0]], inplace=True)

        df = pd.concat(dfs)

    df = rescale(df, columns, args.norm / 1000, absolute=new_method).sort_values(by = 'order', ascending = False)
    print(df[columns])

    fig, ax = plt.subplots(1, 1, figsize=(9, 8))

    ax.set_ylim([0, df.shape[0]*1.5])
    ax.set_xlim([1, 1000 if args.logx else 30])
    fontsize = 18

    # Plot bands
    for y, (index, row) in enumerate(df.iterrows()):
        if args.unblind:
            obs = row[columns[5]]
            ax.vlines(obs, y, y+1, colors = 'k', linestyles = 'solid', zorder = 1.1, label = 'Observed' if y==0 else '')
            ax.scatter(obs, y+0.5, s=50, c='k', marker='o', zorder = 1.1)
            ax.text(700, y+0.5, f'{obs:.2f}', horizontalalignment='right', verticalalignment='center', fontsize=fontsize)
        exp = row[columns[4]]
        ax.vlines(exp, y, y+1, colors = 'k', linestyles = 'dotted', zorder = 1.1, label = 'Expected' if y==0 else '')
        ax.fill_betweenx([y,y+1], row[columns[0]], row[columns[3]], facecolor = 'yellow', label = r'$\mathrm{Expected \pm 2 \sigma}$' if y==0 else '')
        ax.fill_betweenx([y,y+1], row[columns[1]], row[columns[2]], facecolor = 'lime', label = r'$\mathrm{Expected \pm 1 \sigma}$' if y==0 else '')
        # Plot text
        ax.text(200, y+0.5, f'{exp:.2f}', horizontalalignment='right', verticalalignment='center', fontsize=fontsize)

    if args.unblind:
        ax.text(700, y+1.5, 'Obs.', horizontalalignment='right', verticalalignment='center', fontsize=fontsize)
    ax.text(200, y+1.5, 'Exp.', horizontalalignment='right', verticalalignment='center', fontsize=fontsize)

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
    xlabel = '95% ' + r'CL upper limit on $\sigma_{\mathrm{%s}}$ ($\mathrm{pp \rightarrow HH}$) normalised to $\mathrm{\sigma_{%s}^{SM}}$' % (process, process)
    ax.set_xlabel(xlabel, horizontalalignment='right', x=1.0, fontsize=fontsize)

    textlable = r'$\mathrm{\sigma_{%s}^{SM}}$ = %.2f fb' % (process, args.norm)

    plot_common(args, fig, ax, textlable, fontsize, fontsize)
    save_plot(args)

def plot_common(args, fig, ax, textlable, fontsize, legendsize):
    # ATLAS cosmetics
    if args.resonant_type == 'nonres':
        drawATLASlabel(fig, ax, internal=True, reg_text=textlable, xmin=0.05, ymax=0.9, fontsize_title=20, fontsize_label=fontsize-1, line_spacing=1.2)
    elif args.resonant_type == 'spin0':
        drawATLASlabel(fig, ax, internal=True, reg_text=textlable, xmin=0.2, ymax=0.9, fontsize_title=20, fontsize_label=fontsize-1, line_spacing=1)

    # Legend
    if args.resonant_type == 'nonres':
        plt.legend(bbox_to_anchor=(1., 1), ncol=1, framealpha=0., prop={'size': legendsize})
    elif args.resonant_type == 'spin0':
        new_handlers, new_labels = [], []
        current_handles, current_labels = plt.gca().get_legend_handles_labels()

        for handler, label in zip(current_handles, current_labels):
            if 'Remove' not in label:
                new_handlers.append(handler)
                new_labels.append(label)
        plt.legend(new_handlers, new_labels, bbox_to_anchor=(1., 1), ncol=1, framealpha=0., prop={'size': legendsize})

    plt.tight_layout()
    plt.plot()


def main(args):
    if args.command == 'nonres':
        plot_nonres(args)
    elif args.command == 'spin0':
        plot_spin0(args)


if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mCreate templates and configuration files for TRExFitter.\033[0m")
    subcommands = parser.add_subparsers(dest='command')

    nonres = subcommands.add_parser('nonres', help='Plot nonres.')
    nonres.add_argument('nonres', nargs='*')
    nonres.add_argument('-l', '--dat_list', nargs='+', type=str, default=['../data-files/nonres-bbtautau.dat', '../data-files/nonres-bbyy.dat', '../data-files/nonres-bbbb.dat', '../data-files/nonres-bbll.dat', '../data-files/nonres-bbVV.dat', '../data-files/nonres-WWWW.dat', '../data-files/nonres-combined-A-bbbb_bbll_bbtautau_bbVV_bbyy_WWWW-nocorr.dat', '../data-files/nonres-combined-A-bbbb_bbtautau_bbyy-nocorr.dat'], required=False, help='')
    nonres.add_argument('--logx', action='store_true', default=False, required=False, help='')
    nonres.add_argument('--norm', type=float, default=31.05, required=False, help='')
    nonres.add_argument('--unblind', action='store_true', default=False, required=False, help='')

    spin0 = subcommands.add_parser('spin0', help='Plot spin0.')
    spin0.add_argument('spin0', nargs='*')
    spin0.add_argument('--dat_list', nargs='+', type=str, default=['../data-files/spin0-bbtautau.dat', '../data-files/spin0-bbyy.dat', '../data-files/spin0-bbbb.dat'], required=False, help='')
    spin0.add_argument('--com_list', nargs='+', type=str, default=['../data-files/spin0-combined-A-bbbb_bbtautau-nocorr.dat', '../data-files/spin0-combined-A-bbtautau_bbyy-nocorr.dat', '../data-files/spin0-combined-A-bbbb_bbtautau_bbyy-nocorr.dat'], required=False, help='')
    spin0.add_argument('--logx', action='store_true', default=False, required=False, help='')
    spin0.add_argument('--unblind', action='store_true', default=False, required=False, help='')
    spin0.add_argument('--debug', action='store_true', default=False, required=False, help='')


    args = parser.parse_args()
    main(args)
