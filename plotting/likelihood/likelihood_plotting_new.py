#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import atlas_mpl_style as ampl
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.lines as lines

ampl.use_atlas_style()

plt.rcParams['figure.dpi'] = 100

#channel = 'lephad'
#channel = 'hadhad'
channel = 'tautau'


##############################################################################
# Read json file
def loadJSON(path):
    with open(path,'r') as f:
         nll = json.load(f)
    # Put in dataframe
    df = pd.DataFrame(nll)
    #print(df)
    # rename columns so that I don't have to change the code below, mu and qmu are the ones needed.
    df = df.rename(columns={"mu": "kl", "nll": "other", "qmu": "nll"})
    # drop first row
    df = df.iloc[1: , :]
    #print(df['kl'],df['nll'])
    return df

def intersections(df,npoints,channel):
    x,y = df['kl'],df['nll'] #
    if channel != 'lephad':
       fx = np.linspace(-2,10,num=npoints)
    else:
       fx = np.linspace(-4,12,num=npoints)
    fy = np.interp(fx, x, y)

    onesigma = np.linspace(1,1,num=npoints)
    twosigma = np.linspace(4,4,num=npoints)

    idx_onesigma = np.argwhere(np.diff(np.sign(fy - onesigma))).flatten()
    idx_twosigma = np.argwhere(np.diff(np.sign(fy - twosigma))).flatten()
    return fx[idx_onesigma],fx[idx_twosigma]
###############################################################################

statOnly_path = '../../../output/v3000invfb_20211106_Local/param/likelihood/bbyy_klambda.json'
baseline_path = '../../../output/v3000invfb_20211106_Local/param/likelihood/bbtautau_klambda.json'
halfTheo_path = '../../../output/v3000invfb_20211106_Local/param/likelihood/combined_klambda.json'
#noMCstat_path = '../llh_scans_newcommit/likelihood_scan_'+channel+'_run2SysNoMCstat/klambda.json'
#run2sys_path  = '../llh_scans_newcommit/likelihood_scan_'+channel+'_run2Sys/klambda.json'

##load data in dataframes 
df_statOnly = loadJSON(statOnly_path)
df_baseline = loadJSON(baseline_path)
df_halfTheo = loadJSON(halfTheo_path)
#df_noMCstat = loadJSON(noMCstat_path)
#df_run2sys  = loadJSON(run2sys_path)

npoints=2000

#find intersections at 1sigma and 2sigma
fx_statOnly_sigma1,fx_statOnly_sigma2 = intersections(df_statOnly,npoints,channel)
fx_baseline_sigma1,fx_baseline_sigma2 = intersections(df_baseline,npoints,channel)
fx_halfTheo_sigma1,fx_halfTheo_sigma2 = intersections(df_halfTheo,npoints,channel)
#fx_noMCstat_sigma1,fx_noMCstat_sigma2 = intersections(df_noMCstat,npoints,channel)
#fx_run2sys_sigma1,fx_run2sys_sigma2   = intersections(df_run2sys,npoints,channel)


# Set up figure
fig = plt.figure(figsize=(8, 6))

#df.plot(x="kl",y="nll",legend=None, use_index=True)
#DataList = [df_statOnly,df_baseline,df_halfTheo,df_noMCstat,df_run2sys]
DataList = [df_statOnly,df_baseline,df_halfTheo]
colorList = ["#9A0EEA", '#008F00', "k"]
lstyle = ['o-','o-','o-','o-','o--']

for i in range(len(DataList)):
    plt.plot(DataList[i]['kl'], DataList[i]['nll'], lstyle[i],  c=colorList[i], markersize=4);

ax = plt.gca()
ax.set_ylim(0,12)
if channel != 'lephad':
	ax.set_xlim(-2,10)
else:
	ax.set_xlim(-4,12)

ax.axhline(1, color="grey", linestyle="--")
ax.axhline(4, color="grey", linestyle="--")

ampl.set_ylabel("-2$\Delta$ln(L)",fontsize= 20)
ampl.set_xlabel("$\mathrm{\kappa_\lambda}$", fontsize= 20)

#plt.plot(fx[idx_onesigma], onesigma[idx_onesigma], 'yo')
#plt.plot(fx[idx_twosigma], twosigma[idx_twosigma], 'yo')

border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)

handles,labels = ax.get_legend_handles_labels()

if channel == 'lephad':
   ampl.draw_atlas_label(0.2, 0.95, ax, status = 'int', energy = '14 TeV', lumi = 3000, desc = r"$HH \rightarrow$ $\mathrm{b\bar{b} \tau^{+}_{\mathrm{lep}} \tau^{-}_\mathrm{had}}$")
elif channel == 'hadhad':
   ampl.draw_atlas_label(0.2, 0.95, ax, status = 'int', energy = '14 TeV', lumi = 3000, desc = r"$HH \rightarrow$ $\mathrm{b\bar{b} \tau^{+}_{\mathrm{had}} \tau^{-}_\mathrm{had}}$")
else:
   ampl.draw_atlas_label(0.2, 0.95, ax, status = 'int', energy = '14 TeV', lumi = 3000, desc = r"$HH \rightarrow$ $\mathrm{b\bar{b} \tau^{+}\tau^{-}}$")


#ax.legend(loc='upper right',frameon = False)
plt.axhline(y=1., color='0.8', linestyle='--')
plt.axhline(y=4., color='0.8', linestyle='--')
l1 = ax.legend(handles[0:2]+handles[5:], labels[0:2]+labels[5:], loc=(0.52,0.62),fontsize = 12, frameon = False)
plt.gca().add_artist(l1)

line1 = lines.Line2D([],[],color="#9A0EEA",label=r"$\mathrm{b\bar{b}\gamma\gamma}$")
line2 = lines.Line2D([],[],color='#008F00',label=r"$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$")
line3 = lines.Line2D([],[],color="k",label=r'Combined')
#line4 = lines.Line2D([],[],color="red",label=r'MC stat. unc. neglected')
#line5 = lines.Line2D([],[],color="darkred",label=r'Run-2 syst. unc.',linestyle='--')
handles = [line1, line2, line3]

fig.legend(bbox_to_anchor=(0.45, 0.7), loc='upper center',fontsize = 12 ,handles=handles)
plt.savefig('../../../output/v3000invfb_20211106_Local/param/figures/likelihood_scan.pdf')#, bbox_inches='tight')

print(channel)
print("bbyy: 1 sigma interval: {} , 2 sigma interval: {}".format(fx_statOnly_sigma1,fx_statOnly_sigma2))
print("bbtautau: 1 sigma interval: {} , 2 sigma interval: {}".format(fx_baseline_sigma1,fx_baseline_sigma2))
print("combined: 1 sigma interval: {} , 2 sigma interval: {}".format(fx_halfTheo_sigma1,fx_halfTheo_sigma2))
#print("noMCstat: 1 sigma interval: {} , 2 sigma interval: {}".format(fx_noMCstat_sigma1,fx_noMCstat_sigma2))
#print("run2sys:  1 sigma interval: {} , 2 sigma interval: {}".format(fx_run2sys_sigma1,fx_run2sys_sigma2))

