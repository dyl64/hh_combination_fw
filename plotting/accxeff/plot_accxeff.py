import numpy as np
import glob
import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.lines as lines
import atlas_mpl_style as ampl
import collections
import json
import pandas as pd
import itertools

ampl.use_atlas_style()


plt.rcParams['figure.dpi'] = 100

df = pd.read_csv("Efficiencies.csv",skiprows=1)

# bbyy -------------------------

# Set up figure
fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(4,1)
ax = fig.add_subplot(gs[:4,0])

plt.plot(df["kl"],df["Signal yields.2"]/(df["Cross section.2"]*float(df["Branching ratio.2"].loc[0])), color = "hh:darkpink",label="High Mass BDT Tight")
plt.plot(df["kl"],df["Signal yields.3"]/(df["Cross section.3"]*float(df["Branching ratio.3"].loc[0])), color = "hh:darkyellow",label="High Mass BDT Loose")
plt.plot(df["kl"],df["Signal yields"]/(df["Cross section"]*float(df["Branching ratio"].loc[0]))      , color = "hh:darkblue",label="Low Mass BDT Tight")
plt.plot(df["kl"],df["Signal yields.1"]/(df["Cross section.1"]*float(df["Branching ratio.1"].loc[0])), color = "#008F00",label="Low Mass BDT Loose")


ampl.draw_atlas_label(0.04, 0.955, ax, status = 'int', energy = '13 TeV', lumi = 139, desc = r"$HH \rightarrow b\bar{b} \gamma \gamma$" )
ampl.set_ylabel('Acceptance x Efficiency [%]', fontsize= 20)    
ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
ax.xaxis.set_ticks(np.arange(-10, 10 + 1, 2))
plt.xlim((-10,10))
plt.ylim((0,14))
plt.legend(fontsize=12)
plt.savefig("bbyy_accxeff.pdf")

# bbtautau ------------------------- 

# Set up figure
fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(4,1)
ax = fig.add_subplot(gs[:4,0])

plt.plot(df["kl"],df["Signal yields.4"]/(df["Cross section.4"]*float(df["Branching ratio.4"].loc[0]))          , color = "hh:darkpink",   label=r"$b\bar{b} \tau_{had} \tau_{had}$")
plt.plot(df["kl"],df["SLT ggF+VBF Signal yields"]/(df["Cross section.5"]*float(df["Branching ratio.5"].loc[0])), color = "hh:lightturquoise",   label=r"$b\bar{b} \tau_{lep} \tau_{had}$ SLT")
plt.plot(df["kl"],df["LTT ggF+VBF Signal yields"]/(df["Cross section.5"]*float(df["Branching ratio.5"].loc[0])), color = "hh:darkblue",       label=r"$b\bar{b} \tau_{lep} \tau_{had}$ LTT")

ampl.draw_atlas_label(0.04, 0.955, ax, status = 'int', energy = '13 TeV', lumi = 139, desc = r"$HH \rightarrow b\bar{b} \tau \tau$" )
ampl.set_ylabel('Acceptance x Efficiency [%]', fontsize= 20)    
ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
ax.xaxis.set_ticks(np.arange(-10, 10 + 1, 2))
plt.xlim((-10,10))
plt.legend(fontsize=12)
plt.savefig("bbtautau_accxeff.pdf")

# combined -------------------------

fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(4,1)
ax = fig.add_subplot(gs[:4,0])

all_bbyy = (df["Signal yields"]+df["Signal yields.1"]+df["Signal yields.2"]+df["Signal yields.3"])
all_bbtautau_lephad = (df["SLT ggF+VBF Signal yields"]+df["LTT ggF+VBF Signal yields"])

plt.plot(df["kl"],all_bbyy/(df["Cross section.1"]*float(df["Branching ratio.1"].loc[0])),              color = "hh:darkpink", label=r"$b\bar{b} \gamma \gamma$ ")
plt.plot(df["kl"],all_bbtautau_lephad/(df["Cross section.5"]*float(df["Branching ratio.5"].loc[0])),   color = "#008F00",     label=r"$b\bar{b} \tau_{lep} \tau_{had}$ SLT+LTT")
plt.plot(df["kl"],df["Signal yields.4"]/(df["Cross section.4"]*float(df["Branching ratio.4"].loc[0])), color = "hh:darkblue", label=r"$b\bar{b} \tau_{had} \tau_{had}$")

ampl.draw_atlas_label(0.04, 0.955, ax, status = 'int', energy = '13 TeV', lumi = 139)
ampl.set_ylabel('Acceptance x Efficiency [%]', fontsize= 20)    
ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
ax.xaxis.set_ticks(np.arange(-10, 10 + 1, 2))
plt.xlim((-10,10))
plt.ylim((0,20))
plt.legend(fontsize=12)
plt.savefig("all_accxeff.pdf")