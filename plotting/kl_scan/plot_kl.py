# Jannicke Pearkes modified from Alex Wang, https://gitlab.cern.ch/atlas-physics/HDBS/DiHiggs/yybb/code/-/blob/alex/bbyyPlotter/plot_kl_scan.py
# who modified from https://gitlab.cern.ch/hartman/dihiggs4b/blob/master/PFlow-Topo/Limit-Comparisons.ipynb by Nicole Hartman
# requires python3 to use atlas_mpl_style


"""

Input: json files with the following format
["kappa_lambda": [-2sigma, -1sigma, expected, +1sigma, +2sigma, observed]

  "0": 12.034214254391598,# expected
  "2": 25.544788964859485,
  "1": 17.541475069768936,
  "-1": 8.671317738197763,
  "-2": 6.45907304342866,
  "obs": 7.79886154984291,
  "inj": 0

json files must be named according to nXpX, e.g. kl = -0.5 -> n0p5, kl = 1.0 -> 1p5
"""

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



def xs_ggF(kl):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
    return (70.3874-50.4111*kl+11.0595*kl**2)  #XS in fb

def xs_VBF(kl):
    #https://indico.cern.ch/event/995807/contributions/4184798/attachments/2175756/3683303/VBFXSec.pdf
    return (4.581-4.245*kl+1.359*kl**2)

def xs_HH(kl):
    return xs_ggF(kl) + xs_VBF(kl)

# When adding 2 independent Gaussians (e.g. ggF and VBF XS) we can simply add their means and add their sigmas in quadrature
def sigma_upper_ggF(kl):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
    #add the std on ggF HH due to qcd scale, PDF, and mtop in quadrature
    #return xs_ggF(kl) * math.sqrt((max(72.0744-51.7362*kl+11.3712*kl**2, 70.9286-51.5708*kl+11.4497*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2 + 0.026**2)
    #new mtop uncertainty:
    return xs_ggF(kl) * math.sqrt((max(76.6075 - 56.4818*kl + 12.635*kl**2, 75.4617 - 56.3164*kl + 12.7135*kl**2)  / xs_ggF(kl) - 1)**2 + 0.03**2)

def sigma_upper_VBF(kl):
    #from klambda = 1
    return xs_VBF(kl) * math.sqrt(0.0003**2 + 0.021**2)

def sigma_upper_HH(kl):
    return math.sqrt(sigma_upper_ggF(kl)**2 + sigma_upper_VBF(kl)**2)
    
def xs_upper_HH(kl):
    return xs_HH(kl) + sigma_upper_HH(kl)

def sigma_lower_ggF(kl):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
    #add the std on ggF HH due to qcd scale, PDF, and mtop in quadrature
    #return xs_ggF(kl) * math.sqrt((min(66.0621-46.7458*kl+10.1673*kl**2, 66.7581-47.721*kl+10.4535*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2 + 0.026**2)
    #new mtop uncertainty:
    return xs_ggF(kl) * math.sqrt((min(57.6809 - 42.9905*kl + 9.58474*kl**2, 58.3769 - 43.9657*kl + 9.87094*kl**2)  / xs_ggF(kl) - 1)**2 + 0.03**2)

def sigma_lower_VBF(kl):
    return xs_VBF(kl) * math.sqrt(0.0004**2 + 0.021**2)

def sigma_lower_HH(kl):
    return math.sqrt(sigma_lower_ggF(kl)**2 + sigma_lower_VBF(kl)**2)
    
def xs_lower_HH(kl):
    return xs_HH(kl) - sigma_lower_HH(kl)

 
    
def get_limits(glob_string,string_range,rescale_val=1.0):
    
    lambdas = []
    limit_bands = []

    # search for json files in provided string
    files = sorted(glob.glob(glob_string))
    for file in files:
        if "limits.json" in file:
            files.remove(file)       
    #print(files)
    
    # set up data frame 
    limits_df = pd.DataFrame(columns=["kl","-2","-1","exp","1","2","obs"])
    limits_list = []
    
    for file in files: 
        # parse file names to extract kl value
        if "alkaid" in file: # alkaid's naming convention is 0_kl_9p0.json
            kappa_string = file.split("/")[-1].split("_")[2][:-5]
        else: # my naming convention is 0_kl_9p0.json
            name = file.split("/")[-1]
            kappa_string = name.split("_")[-1][string_range]
        kappa_string = kappa_string.replace("n","-")
        kappa_string = kappa_string.replace("p",".")
        #print(float(kappa_string))
        lambdas += [float(kappa_string)] 

        # read in json file and put in dataframe
        with open(file) as my_json:
            limit = json.load(my_json)
        limits_list.append([float(kappa_string),limit["-2"]*rescale_val,limit["-1"]*rescale_val,limit["0"]*rescale_val,limit["1"]*rescale_val,limit["2"]*rescale_val,limit["obs"]*rescale_val])
    limits_df = pd.DataFrame(limits_list,columns=["kl","-2","-1","exp","1","2","obs"])
    limits_df.sort_values("kl",ignore_index=True,inplace=True)
    
    return limits_df

def get_intersections(lambdas, n_exp, lambdas_th, n_th):
    # get the intersection between expected and theory prediction
    
    # interpolate expected limit with same number of datapoints as used in theory prediction
    interpolated_limit = np.interp(lambdas_th, lambdas, n_exp) 

    #limitm1 = n*np.array(limit_bands[0]) - 1
    limitm1 = interpolated_limit - n_th 
    idx = np.argwhere(np.diff(np.sign(limitm1))).flatten() # determines what index intersection points are at 

    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
    intersections = [lambdas_th[x] - (lambdas_th[x+1] - lambdas_th[x])/(limitm1[x+1] - limitm1[x]) * limitm1[x] for x in idx]
    return intersections
    
def draw_limits(limits_df, channel_name,log=True):
    # Set up figure
    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(4,1)
    ax = fig.add_subplot(gs[:4,0])
    
    lambdas = limits_df["kl"]
    n = [xs_HH(kl) for kl in lambdas] # get expected cross-section at different kls
    
    # multiply mu by expected cross-section and plot obs, expected limits
    if log:
        ax.semilogy(lambdas, n * np.array(limits_df["obs"]),'k',label='Observed limit (95% CL)')
        ax.semilogy(lambdas, n * np.array(limits_df["exp"]),'k--',label='Expected limit (95% CL)')
    else:
        ax.plot(lambdas, n * np.array(limits_df["obs"]),'k',label='Observed limit (95% CL)')
        ax.plot(lambdas, n * np.array(limits_df["exp"]),'k--',label='Expected limit (95% CL)')
        
    
    #for i in range(len(lambdas)):
    #    print("kl:"+str(lambdas[i])+", obs:"+ str((n * np.array(limits_df["obs"]))[i])+", exp:"+str((n * np.array(limits_df["exp"]))[i]))


    
    # plot 1 & 2 sigma bands 
    ax.fill_between(lambdas, n * np.array(limits_df["-2"]), n * np.array(limits_df["2"]),  facecolor = '#FDC536', label='Expected limit $\pm 2\sigma$')
    ax.fill_between(lambdas, n * np.array(limits_df["-1"]), n * np.array(limits_df["1"]),  facecolor = '#4AD9D9', label='Expected limit $\pm 1\sigma$')

    # for the theory expected cross-section we can have a smoother function by running over more kl points
    lambdas_th = np.linspace(-10.0,10.0,1000) 
    n_th = [xs_HH(kl) for kl in lambdas_th] # get expected cross-section at different kls
    
    # plot theory prediction 
    ax.plot(lambdas_th,n_th,'C4', color = 'darkred', label='Theory prediction')
    th_band = ax.fill_between(lambdas_th, [xs_lower_HH(kl) for kl in lambdas_th], [xs_upper_HH(kl) for kl in lambdas_th],  facecolor = '#F2385A')
    
    if log:
        y_annotation = (0.1,0.18)
    else:
        y_annotation = (0.4,0.48)
    # get expected limits 
    intersections = get_intersections(lambdas, n*limits_df["exp"], lambdas_th, n_th)
    if intersections:
        print ('limits expected:', intersections)
        plt.annotate(r'Expected: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.04, y_annotation[0]), xycoords = 'axes fraction', fontsize = 15)
    
    #for x in intersections:
    #   ax.plot([x]*2,ylim,'blue')
    
    # get observed limits 
    intersections = get_intersections(lambdas, n*limits_df["obs"], lambdas_th, n_th)
    if intersections:
        plt.annotate(r'Observed: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.04,  y_annotation[1]), xycoords = 'axes fraction', fontsize = 15)
        print ('limits observed:', intersections)
    
    #for x in intersections:
    #        ax.plot([x]*2,ylim,'blue')
    
    #SM point
    ax.plot(1, xs_HH(1), linewidth = 0, marker = '*', markersize = 20, color = '#E9F1DF', markeredgecolor = 'black', label = 'SM prediction')


    # make pretty 
    if log:
        ylim = [10, 10e4] # set consistent y-axis
    else: 
        ylim = [0,2500]
    ax.set_ylim(ylim)
    ax.xaxis.set_ticks(np.arange(min(lambdas), max(lambdas) + 1, 2))
    ax.set_xlim([-10,10])
    ampl.set_ylabel('$\sigma_{ggF+VBF}$ (HH) [fb]', fontsize= 20)    
    ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
    ampl.draw_atlas_label(0.05, 0.95, ax, status = 'int', energy = '13 TeV', lumi = 139, desc = r"$HH \rightarrow$ "+channel_name)

    # border for the legend
    border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)
    
    # reorder the legend
    handles,labels = ax.get_legend_handles_labels()
    handles[2].set_linewidth(1.0)
    handles = [handles[0], handles[1], (handles[5], border_leg), (handles[4], border_leg), (th_band, handles[2], border_leg), handles[3]]
    labels = [labels[0], labels[1], labels[5], labels[4], labels[2], labels[3]]
    ax.legend(handles, labels, loc='upper right', fontsize = 'small', frameon = False)
    
    #plt.savefig('kl_scan.pdf')
    
def draw_all_limits(*args):
    """Last input must always be the combined one """
    
    # Set up figure
    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(4,1)
    ax = fig.add_subplot(gs[:4,0])
    
    # Set up color wheel
    palette = itertools.cycle(["#531B93","#008F00"])#["tab:orange","cornflowerblue","#343844",'darkcyan','seagreen'])#["peru","cornflowerblue","#343844",'darkcyan','seagreen'])
    
    # Plot each individual channel first 
    for my_tuple in args:
        
        limits_df = my_tuple[0]
        channel_label = my_tuple[1]
        
        lambdas = limits_df["kl"]
        n = [xs_HH(kl) for kl in lambdas] # get expected cross-section at different kls
        
        if channel_label != "Combined":
            my_color = next(palette) 
            my_width = 1.5
        else:
            my_color = 'k' #Black 
            my_width = 2.5
        
        # multiply mu by expected cross-section and plot obs, expected limits
        ax.semilogy(lambdas, n * np.array(limits_df["obs"]),color = my_color,linewidth=my_width,label=channel_label)
        ax.semilogy(lambdas, n * np.array(limits_df["exp"]),color = my_color,linestyle='--',linewidth=my_width,label=channel_label)
            
    
        # plot 1 & 2 sigma bands 
        if channel_label == "Combined":
            ax.fill_between(lambdas, n * np.array(limits_df["-2"]), n * np.array(limits_df["2"]),  facecolor = '#FDC536', label='Combined expected limit $\pm 2\sigma$')
            ax.fill_between(lambdas, n * np.array(limits_df["-1"]), n * np.array(limits_df["1"]),  facecolor = '#4AD9D9', label='Combined expected limit $\pm 1\sigma$')

    # for the theory expected cross-section we can have a smoother function by running over more kl points
    lambdas_th = np.linspace(-10.0,10.0,100) 
    n_th = [xs_HH(kl) for kl in lambdas_th] # get expected cross-section at different kls

    # plot theory prediction 
    ax.plot(lambdas_th,n_th,'C4', color = 'darkred', label='Theory prediction')
    th_band = ax.fill_between(lambdas_th, [xs_lower_HH(kl) for kl in lambdas_th], [xs_upper_HH(kl) for kl in lambdas_th],  facecolor = '#F2385A')
      

    # get expected limits 
    intersections = get_intersections(lambdas, n*limits_df["exp"], lambdas_th, n_th)
    if intersections:
        print ('limits expected:', intersections)
        plt.annotate(r'Expected: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.04, 0.10), xycoords = 'axes fraction', fontsize = 15)

    #for x in intersections:
    #   ax.plot([x]*2,ylim,'blue')

    # get observed limits 
    intersections = get_intersections(lambdas, n*limits_df["obs"], lambdas_th, n_th)
    if intersections:
        plt.annotate(r'Observed: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.04, 0.18), xycoords = 'axes fraction', fontsize = 15)
        print ('limits observed:', intersections)

    #for x in intersections:
    #       ax.plot([x]*2,ylim,'blue')

    #SM point
    ax.plot(1, xs_HH(1), linewidth = 0, marker = '*', markersize = 20, color = '#E9F1DF', markeredgecolor = 'black', label = 'SM prediction')

    # make pretty 
    ylim = [5, 1e4] # set consistent y-axis
    ax.set_ylim(ylim)
    ax.xaxis.set_ticks(np.arange(min(lambdas), max(lambdas) + 1, 2))
    ax.set_xlim([-10,10])
    ampl.set_ylabel('$\sigma_{ggF+VBF}$ (HH) [fb]', fontsize= 20)    
    ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
    ampl.draw_atlas_label(0.05, 0.95, ax, status = 'int', energy = '13 TeV', lumi = 139)

    # border for the legend
    border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)

    # reorder the legend
    handles,labels = ax.get_legend_handles_labels()

    handles = [lines.Line2D([0], [0], ls='-',lw=2,c='black'),lines.Line2D([0], [0], ls='--',lw=2,c='black'),handles[0], handles[2], handles[4],  (handles[9], border_leg), (handles[8], border_leg), (th_band,handles[6], border_leg), handles[7]]
    #handles = [handles[0], handles[1], (handles[5], border_leg), (handles[4], border_leg), (th_band, handles[2], border_leg), handles[3]]
    labels = ['Observed limit (95% CL)', 'Expected limit (95% CL)', labels[0], labels[2], labels[4],  labels[9], labels[8], labels[6], labels[7]]
    #plt.legend(bbox_to_anchor=(1.15, 1), loc=2, borderaxespad=0.,frameon = False)
    ax.legend(handles, labels, bbox_to_anchor=(1.05, 1),loc=2, fontsize = 'small', frameon = False)

    plt.savefig('all_channels_kl_scan.pdf',bbox_inches='tight')


if __name__ == "__main__": 
    
    print("bbyy")
    limits_ak_df_bbyy = get_limits("/eos/user/j/jpearkes/hh_combination_outputs/individual/alkaid_aug_27/bbyy_new/*[!y].json",slice(2,-5),rescale_val=1.0/32.776*1000);
    draw_limits(limits_ak_df_bbyy,r"$b\bar{b} \gamma \gamma$")
    plt.savefig('bbyy_kl_scan.pdf')
    #draw_limits(limits_ak_df_bbyy,r"$b\bar{b} \gamma \gamma$",log=False)

    print("bbtautau")
    limits_ak_df_bbtautau = get_limits("/eos/user/j/jpearkes/hh_combination_outputs/individual/alkaid_aug_27/bbtautau_new/*[!y].json",slice(2,-5),rescale_val=1.0/32.776*1000);
    draw_limits(limits_ak_df_bbtautau,r"$b\bar{b} \tau \tau$")
    plt.savefig('bbtautau_kl_scan.pdf')
    #draw_limits(limits_ak_df_bbtautau,r"$b\bar{b} \tau \tau$",log=False)

    print("Combined")
    limits_ak_df_combined = get_limits("/eos/user/j/jpearkes/hh_combination_outputs/individual/alkaid_aug_27/combined_new/A-bbtautau_bbyy-fullcorr/*[!y].json",slice(2,-5),rescale_val=1.0/32.776*1000);
    draw_limits(limits_ak_df_combined,r"$b\bar{b} \gamma \gamma + b\bar{b} \tau \tau$")
    #draw_limits(limits_ak_df_combined,r"$b\bar{b} \gamma \gamma + b\bar{b} \tau \tau$",log=False)
    plt.savefig('combined_kl_scan.pdf')

    draw_all_limits((limits_ak_df_bbyy,r"$b\bar{b} \gamma \gamma$"),
                    (limits_ak_df_bbtautau,r"$b\bar{b} \tau \tau$"),
                    (limits_ak_df_combined,"Combined"))