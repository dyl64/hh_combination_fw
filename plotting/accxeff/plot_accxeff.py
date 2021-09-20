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


# Read in an process table --------------
columns = ["kl",
 "yields_bbyy_lm_tight","xsec_bbyy_lm_tight","br_bbyy_lm_tight",
 "yields_bbyy_lm_loose","xsec_bbyy_lm_loose","br_bbyy_lm_loose",
 "yields_bbyy_hm_tight","xsec_bbyy_hm_tight","br_bbyy_hm_tight",
 "yields_bbyy_hm_loose","xsec_bbyy_hm_loose","br_bbyy_hm_loose",
 "yields_bbtautau_hadhad","xsec_bbtautau_hadhad","br_bbtautau_hadhad",
 "yields_bbtautau_lephad_slt","yields_bbtautau_lephad_ltt","xsec_bbtautau_lephad","br_bbtautau_lephad"]

df = pd.read_csv("Efficiency-3.csv",skiprows=2,names=columns)

# Cross-section and BR is same for all bbyy categories
df["xsec_bbyy"] = df["xsec_bbyy_lm_tight"]
df["br_bbyy"] = df["br_bbyy_lm_tight"]
df["xsec_bbtautau"] = df["xsec_bbtautau_hadhad"]

df = df.drop(["xsec_bbyy_lm_tight","br_bbyy_lm_tight",
"xsec_bbyy_lm_loose","br_bbyy_lm_loose",
"xsec_bbyy_hm_tight","br_bbyy_hm_tight",
"xsec_bbyy_hm_loose","br_bbyy_hm_loose",
 "xsec_bbtautau_hadhad","xsec_bbtautau_lephad"],axis=1)

# Branching ratios
br_bbyy = float(df["br_bbyy"].loc[0])
br_bbtautau_hadhad = float(df["br_bbtautau_hadhad"].loc[0])
br_bbtautau_lephad = float(df["br_bbtautau_lephad"].loc[0])

# Lumi 
lumi = 3.21956 + 32.9881 + 44.3074 + 58.4501
print("lumi: "+str(lumi)+"/fb")

# Combine yields
yields_all_bbyy = (df["yields_bbyy_lm_tight"]+df["yields_bbyy_lm_loose"]+df["yields_bbyy_hm_tight"]+df["yields_bbyy_hm_loose"])
yields_all_bbtautau_lephad = (df["yields_bbtautau_lephad_slt"]+df["yields_bbtautau_lephad_ltt"])

# Accxeff calculations
accxeff_hm_tight = df["yields_bbyy_hm_tight"]/(df["xsec_bbyy"]*br_bbyy*lumi)*100.0
accxeff_hm_loose = df["yields_bbyy_hm_loose"]/(df["xsec_bbyy"]*br_bbyy*lumi)*100.0
accxeff_lm_tight = df["yields_bbyy_lm_tight"]/(df["xsec_bbyy"]*br_bbyy*lumi)*100.0
accxeff_lm_loose = df["yields_bbyy_lm_loose"]/(df["xsec_bbyy"]*br_bbyy*lumi)*100.0
accxeff_bbyy = yields_all_bbyy/(df["xsec_bbyy"]*br_bbyy*lumi)*100.0

accxeff_bbtautau_hadhad = df["yields_bbtautau_hadhad"]/(df["xsec_bbtautau"]*br_bbtautau_hadhad*lumi)*100.0
accxeff_bbtautau_lephad_ltt = df["yields_bbtautau_lephad_ltt"]/(df["xsec_bbtautau"]*br_bbtautau_lephad*lumi)*100.0
accxeff_bbtautau_lephad_slt = df["yields_bbtautau_lephad_slt"]/(df["xsec_bbtautau"]*br_bbtautau_lephad*lumi)*100.0
accxeff_bbtautau_lephad = accxeff_bbtautau_lephad_slt+accxeff_bbtautau_lephad_ltt#yields_all_bbtautau_lephad/(df["xsec_bbtautau"]*br_bbtautau_lephad*lumi)*100.0
accxeff_bbtautau = accxeff_bbtautau_hadhad+accxeff_bbtautau_lephad

sm_accxeff_bbyy =            float(yields_all_bbyy[df["kl"]==1.0]/(df["xsec_bbyy"][df["kl"]==1.0]*br_bbyy*lumi)*100.0)
sm_accxeff_bbtautau_lephad = float(yields_all_bbtautau_lephad[df["kl"]==1.0]/(df["xsec_bbtautau"][df["kl"]==1.0]*br_bbtautau_lephad*lumi)*100.0)
sm_accxeff_bbtautau_hadhad = float(df["yields_bbtautau_hadhad"][df["kl"]==1.0]/(df["xsec_bbtautau"][df["kl"]==1.0]*br_bbtautau_hadhad*lumi)*100.0)
sm_accxeff_bbtautau =   sm_accxeff_bbtautau_lephad+sm_accxeff_bbtautau_hadhad   



# bbyy -------------------------

fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(4,1)
ax = fig.add_subplot(gs[:4,0])

plt.plot(df["kl"],accxeff_hm_tight, color = "hh:darkpink",label="High Mass BDT Tight")
plt.plot(df["kl"],accxeff_hm_loose, color = "hh:darkyellow",label="High Mass BDT Loose")
plt.plot(df["kl"],accxeff_lm_tight, color = "hh:darkblue",label="Low Mass BDT Tight")
plt.plot(df["kl"],accxeff_lm_loose, color = "#008F00",label="Low Mass BDT Loose")


ampl.draw_atlas_label(0.04, 0.955, ax, status = 'int', energy = '13 TeV', lumi = 139, desc = r"$HH \rightarrow b\bar{b} \gamma \gamma$" )
ampl.set_ylabel('Acceptance x Efficiency [%]', fontsize= 20)    
ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
ax.xaxis.set_ticks(np.arange(-10, 10 + 1, 2))
plt.xlim((-10,10))
plt.ylim((0,10))
plt.legend(fontsize=12)
plt.savefig("bbyy_accxeff.pdf")

# bbtautau ------------------------- 

fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(4,1)
ax = fig.add_subplot(gs[:4,0])

plt.plot(df["kl"],accxeff_bbtautau_hadhad    , color = "#008F00",   label=r"$b\bar{b} \tau_{had} \tau_{had}$")
plt.plot(df["kl"],accxeff_bbtautau_lephad_slt, color = "hh:darkyellow",   label=r"$b\bar{b} \tau_{lep} \tau_{had}$ SLT")
plt.plot(df["kl"],accxeff_bbtautau_lephad_ltt, color = "hh:darkblue",       label=r"$b\bar{b} \tau_{lep} \tau_{had}$ LTT")
plt.plot(df["kl"],accxeff_bbtautau_lephad,     color = "hh:darkpink",     label=r"$b\bar{b} \tau_{lep} \tau_{had}$ SLT+LTT")


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


plt.plot(df["kl"],accxeff_bbyy,             color = "hh:darkpink", label=r"$b\bar{b} \gamma \gamma$ ")
plt.plot(df["kl"],accxeff_bbtautau,        color = '#9A0EEA', label=r"$b\bar{b} \tau \tau$")
#plt.plot(df["kl"],accxeff_bbtautau_lephad,   color = "#008F00",     label=r"$b\bar{b} \tau_{lep} \tau_{had}$ SLT+LTT")
#plt.plot(df["kl"],accxeff_bbtautau_hadhad,   color = "hh:darkblue", label=r"$b\bar{b} \tau_{had} \tau_{had}$")

ampl.set_ylabel('Acceptance x Efficiency [%]', fontsize= 20) 
plt.ylim((0,20))
ampl.draw_atlas_label(0.04, 0.955, ax, status = 'int', energy = '13 TeV', lumi = 139) 
ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
ax.xaxis.set_ticks(np.arange(-10, 10 + 1, 2))
plt.xlim((-10,10))
plt.legend(fontsize=12)
plt.savefig("all_accxeff.pdf")


fig2 = plt.figure(figsize=(8, 6))
gs2 = gridspec.GridSpec(4,1)
ax2 = fig.add_subplot(gs[:4,0])

# Normalized by SM efficiency                                                                   
plt.plot(df["kl"],accxeff_bbyy/sm_accxeff_bbyy,             color = "hh:darkpink", label=r"$b\bar{b} \gamma \gamma$ ")
plt.plot(df["kl"],accxeff_bbtautau/sm_accxeff_bbtautau,      color = '#9A0EEA', label=r"$b\bar{b} \tau \tau$")
#plt.plot(df["kl"],accxeff_bbtautau_lephad/sm_accxeff_bbtautau_lephad,   color = "#008F00",     label=r"$b\bar{b} \tau_{lep} \tau_{had}$ SLT+LTT")
#plt.plot(df["kl"],accxeff_bbtautau_hadhad/sm_accxeff_bbtautau_hadhad,   color = "hh:darkblue", label=r"$b\bar{b} \tau_{had} \tau_{had}$")

ampl.set_ylabel('(Acceptance x Efficiency) / \n ($\kappa_\lambda=1$ Acceptance x Efficiency)', fontsize= 20) 
ampl.draw_atlas_label(0.04, 0.955, ax, status = 'int', energy = '13 TeV', lumi = 139) 
ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
ax2.xaxis.set_ticks(np.arange(-10, 10 + 1, 2))
plt.xlim((-10,10))

plt.legend(fontsize=12)
plt.savefig("all_normalized_accxeff.pdf")