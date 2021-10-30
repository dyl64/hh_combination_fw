# Jannicke Pearkes modified from Alex Wang, https://gitlab.cern.ch/atlas-physics/HDBS/DiHiggs/yybb/code/-/blob/alex/bbyyPlotter/plot_kl_scan.py
# who modified from https://gitlab.cern.ch/hartman/dihiggs4b/blob/master/PFlow-Topo/Limit-Comparisons.ipynb by Nicole Hartman
# requires python3 to use atlas_mpl_style

from pdb import set_trace

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
from argparse import ArgumentParser
import os
import numpy as np
import glob
import math
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 100
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.lines as lines
import collections
import json
import pandas as pd
import itertools

#Now using values from LHCWHGHHHXGGBGGGXXX
SCALE_GGF = 31.05/31.0358 #31.02/31.0358   #correct to xs at mH = 125.09 
SCALE_VBF = 1.726/(4.581-4.245+1.359) # 1.723/(4.581-4.245+1.359)

def xs_ggF(kl):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
    return (70.3874-50.4111*kl+11.0595*kl**2)*SCALE_GGF #XS in fb

def xs_VBF(kl):
    #https://indico.cern.ch/event/995807/contributions/4184798/attachments/2175756/3683303/VBFXSec.pdf
    return (4.581-4.245*kl+1.359*kl**2)*SCALE_VBF

def xs_HH(kl):
    return xs_ggF(kl) + xs_VBF(kl)

# When adding 2 independent Gaussians (e.g. ggF and VBF XS) we can simply add their means and add their sigmas in quadrature
def sigma_upper_ggF(kl):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
    #add the std on ggF HH due to qcd scale, PDF, and mtop in quadrature
    #return xs_ggF(kl) * math.sqrt((max(72.0744-51.7362*kl+11.3712*kl**2, 70.9286-51.5708*kl+11.4497*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2 + 0.026**2)
    #new mtop uncertainty:
    return xs_ggF(kl) * math.sqrt((max(76.6075 - 56.4818*kl + 12.635*kl**2, 75.4617 - 56.3164*kl + 12.7135*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2)

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
    return xs_ggF(kl) * math.sqrt((min(57.6809 - 42.9905*kl + 9.58474*kl**2, 58.3769 - 43.9657*kl + 9.87094*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2)

def sigma_lower_VBF(kl):
    return xs_VBF(kl) * math.sqrt(0.0004**2 + 0.021**2)

def sigma_lower_HH(kl):
    return math.sqrt(sigma_lower_ggF(kl)**2 + sigma_lower_VBF(kl)**2)
    
def xs_lower_HH(kl):
    return xs_HH(kl) - sigma_lower_HH(kl)

#Input: json file with the following format
#["kappa_lambda": [-2sigma, -1sigma, expected, +1sigma, +2sigma, observed]

# "0": 12.034214254391598,# expected
#   "2": 25.544788964859485,
#   "1": 17.541475069768936,
#   "-1": 8.671317738197763,
#   "-2": 6.45907304342866,
#   "obs": 7.79886154984291,
#   "inj": 0

def draw_mu(limits, limit_bands, channel_name, use_ampl=True):
    fig = plt.figure(figsize=(8, 6))

    add_subplot = 0


    gs = gridspec.GridSpec(4,1)
    ax = fig.add_subplot(gs[:4,0])
    
    lambdas = list(limits.keys())

    
    ax.semilogy(lambdas, np.array(limit_bands[3]),'k',label='Observed mu (95%)')
    ax.semilogy(lambdas, np.array(limit_bands[0]),'k--',label='Expected mu (95%)')

    ax.fill_between(lambdas, np.array(limit_bands[-2]), np.array(limit_bands[2]),  facecolor = '#FDC536', label='Expected limit $\pm 2\sigma$')
    ax.fill_between(lambdas, np.array(limit_bands[-1]), np.array(limit_bands[1]),  facecolor = '#4AD9D9', label='Expected limit $\pm 1\sigma$')

    # The extra bands that I wanted to add
    ax.semilogy(lambdas, np.ones(len(lambdas)),'k',label='mu=1')
    
    ax.xaxis.set_ticks(np.arange(min(lambdas), max(lambdas) + 1, 2))

    #reorder the legend
    handles,labels = ax.get_legend_handles_labels()

    ax.legend(handles, labels, loc='upper right', fontsize = 'small', frameon = False)

    if use_ampl:
        import atlas_mpl_style as ampl
        ampl.use_atlas_style()
        ax.set_ylabel('$\mu$ (HH) [fb]', fontsize=16)
        ax.set_xlabel('$\mathrm{\kappa_\lambda}$', fontsize=16)
        ax.draw_atlas_label(0.05, 0.95, ax, status = 'int', energy = '13 TeV', lumi = 139, desc = r"$HH \rightarrow$ "+channel_name)
    else:
        ax.set_ylabel('$\mu$ (HH) [fb]', fontsize=16)
        ax.set_xlabel('$\mathrm{\kappa_\lambda}$', fontsize=16)

    plt.xlim([-10, 10])

def get_limits(glob_string,string_range,rescale_val=1.0):
    
    lambdas = []
    limit_bands = []

    # search for json files in provided string
    files = sorted(glob.glob(glob_string))
    for ifile in files:
        if "limits.json" in ifile:
            files.remove(ifile)       
    
    # set up data frame 
    limits_df = pd.DataFrame(columns=["kl","-2","-1","exp","1","2","obs"])
    limits_list = []
    
    for ifile in files: 
        # parse ifile names to extract kl value
        kappa_string = ifile.split("/")[-1].split("_")[2][:-5]
        kappa_string = kappa_string.replace("n","-")
        kappa_string = kappa_string.replace("p",".")
        lambdas += [float(kappa_string)] 

        # read in json file and put in dataframe
        with open(ifile) as my_json:
            limit = json.load(my_json)
        limits_list.append([float(kappa_string),limit["-2"]*rescale_val,limit["-1"]*rescale_val,limit["0"]*rescale_val,limit["1"]*rescale_val,limit["2"]*rescale_val,limit["obs"]*rescale_val])
    limits_df = pd.DataFrame(limits_list,columns=["kl","-2","-1","exp","1","2","obs"])
    limits_df.sort_values("kl", inplace=True)
    
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
    
def draw_limits(limits_df, channel_name,log=True, status='int', use_ampl=True):
    # Set up figure
    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(4,1)
    ax = fig.add_subplot(gs[:4,0])
    
    lambdas = limits_df["kl"]
    n = [xs_HH(kl) for kl in lambdas] # get expected cross-section at different kls
    
    # multiply mu by expected cross-section and plot obs, expected limits
    if log:
        if args.unblind:
            ax.semilogy(lambdas, n * np.array(limits_df["obs"]),'k',label='Observed limit (95% CL)')
        ax.semilogy(lambdas, n * np.array(limits_df["exp"]),'k--',label='Expected limit (95% CL)')
    else:
        if args.unblind:
            ax.plot(lambdas, n * np.array(limits_df["obs"]),'k',label='Observed limit (95% CL)')
        ax.plot(lambdas, n * np.array(limits_df["exp"]),'k--',label='Expected limit (95% CL)')
        
    
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
        plt.annotate(r'Expected: $\mathrm{\kappa_\lambda} \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.04, y_annotation[0]), xycoords = 'axes fraction', fontsize = 15)
    
    # get observed limits 
    if args.unblind:
        intersections = get_intersections(lambdas, n*limits_df["obs"], lambdas_th, n_th)
        if intersections:
            plt.annotate(r'Observed: $\mathrm{\kappa_\lambda} \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.04,  y_annotation[1]), xycoords = 'axes fraction', fontsize = 15)
            print ('limits observed:', intersections)
    
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
    if use_ampl:
        import atlas_mpl_style as ampl
        ampl.use_atlas_style()
        ampl.set_ylabel('$\sigma_{ggF+VBF}$ (HH) [fb]', fontsize= 20)    
        ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
        ampl.draw_atlas_label(0.05, 0.95, ax, status = status, energy = '13 TeV', lumi = 139, desc = r"$HH \rightarrow$ "+channel_name)
    else:
        ax.set_ylabel('$\sigma_{ggF+VBF}$ (HH) [fb]', fontsize= 20)    
        ax.set_xlabel(r'$\kappa_\lambda$', fontsize=20)

    # border for the legend
    border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)
    
    ## reorder the legend
    #handles, labels = ax.get_legend_handles_labels()
    #set_trace()
    #handles[2].set_linewidth(1.0)
    #handles = [handles[0], handles[1], (handles[5], border_leg), (handles[4], border_leg), (th_band, handles[2], border_leg), handles[3]]
    #labels = [labels[0], labels[1], labels[5], labels[4], labels[2], labels[3]]
    #ax.legend(handles, labels, loc='upper right', fontsize = 'small', frameon = False)

    return plt

def draw_all_limits(status, *channels, use_ampl=True):
    """Last input must always be the combined one """
    
    # Set up figure
    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(4,1)
    ax = fig.add_subplot(gs[:4,0])
    
    # Set up color wheel
    palette = itertools.cycle(["#9A0EEA",'#008F00'])

    # Plot each individual channel first 
    for my_tuple in channels:
        
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
        if args.unblind:
            ax.semilogy(lambdas, n * np.array(limits_df["obs"]),color = my_color,linewidth=my_width,label=channel_label)
        ax.semilogy(lambdas, n * np.array(limits_df["exp"]),color = my_color,linestyle='--',linewidth=my_width,label=channel_label)
            
    
        # plot 1 & 2 sigma bands 
        if channel_label == "Combined":
            ax.fill_between(lambdas, n * np.array(limits_df["-2"]), n * np.array(limits_df["2"]),  facecolor = '#FDC536', label='Comb. exp. limit $\pm 2\sigma$')
            ax.fill_between(lambdas, n * np.array(limits_df["-1"]), n * np.array(limits_df["1"]),  facecolor = '#4AD9D9', label='Comb. exp. limit $\pm 1\sigma$')

    # for the theory expected cross-section we can have a smoother function by running over more kl points
    lambdas_th = np.linspace(-10.0,10.0,1000) 
    n_th = [xs_HH(kl) for kl in lambdas_th] # get expected cross-section at different kls

    # plot theory prediction 
    ax.plot(lambdas_th,n_th,'C4', color = 'darkred', label='Theory prediction')
    th_band = ax.fill_between(lambdas_th, [xs_lower_HH(kl) for kl in lambdas_th], [xs_upper_HH(kl) for kl in lambdas_th],  facecolor = '#F2385A')
      
    annotation_x = 0.04
    annotation_y = 0.09
    # get expected limits 
    intersections = get_intersections(lambdas, n*limits_df["exp"], lambdas_th, n_th)
    if intersections:
        print ('limits expected:', intersections)
        plt.annotate(r'Expected: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (annotation_x,annotation_y), xycoords = 'axes fraction', fontsize = 15)


    # get observed limits 
    if args.unblind:
        intersections = get_intersections(lambdas, n*limits_df["obs"], lambdas_th, n_th)
        if intersections:
            plt.annotate(r'Observed: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (annotation_x,annotation_y+0.08), xycoords = 'axes fraction', fontsize = 15)

    #SM point
    ax.plot(1, xs_HH(1), linewidth = 0, marker = '*', markersize = 20, color = '#E9F1DF', markeredgecolor = 'black', label = 'SM prediction')

    # make pretty 
    ylim = [10, 2e4] # set consistent y-axis
    ax.set_ylim(ylim)
    ax.xaxis.set_ticks(np.arange(min(lambdas), max(lambdas) + 1, 2))
    ax.set_xlim([-10,10])
    if use_ampl:
        ampl.set_ylabel('$\sigma_{ggF+VBF}$ (HH) [fb]', fontsize= 20)    
        ampl.set_xlabel(r'$\kappa_\lambda$', fontsize=20)
        ampl.draw_atlas_label(0.04, 0.955, ax, status = status, energy = '13 TeV', lumi = 139)
    else:
        ax.set_ylabel('$\sigma_{ggF+VBF}$ (HH) [fb]', fontsize= 20)    
        ax.set_xlabel(r'$\kappa_\lambda$', fontsize=20)

    # border for the legend
    border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)

    # reorder the legend
    #handles,labels = ax.get_legend_handles_labels()
    #handles = [lines.Line2D([0], [0], ls='-',lw=2,c='black'),lines.Line2D([0], [0], ls='--',lw=2,c='black'),handles[0], handles[2], handles[4],  (handles[9], border_leg), (handles[8], border_leg), (th_band,handles[6], border_leg), handles[7]]
    #labels = ['Observed limit (95% CL)', 'Expected limit (95% CL)', labels[0], labels[2], labels[4],  labels[9], labels[8], labels[6], labels[7]]
    #l1 = ax.legend(handles[0:2]+handles[5:], labels[0:2]+labels[5:], loc=(0.52,0.62),fontsize = 13, frameon = False)
    #l2 = ax.legend(handles[2:5], labels[2:5], loc=(0.75,0.05),fontsize = 13, frameon = False)
    #plt.gca().add_artist(l1)

    return plt

def main(args):
    out_path = f'{args.input_path}/figures'
    bbyy_path = os.path.join(args.input_path, "limits", "nonres", "bbyy", "0_kl_*[!summary].json")
    limits_ak_df_bbyy = get_limits(bbyy_path, slice(2,-5),rescale_val=1.0/32.776*1000);
    limits_ak_df_bbyy.to_csv(f'{out_path}/kl_xsec_scan_bbyy.csv')
    plt = draw_limits(limits_ak_df_bbyy,r"$\mathrm{b\bar{b}\gamma\gamma}$", status=args.status, use_ampl=not args.ci)
    plt.savefig(f'{out_path}/kl_xsec_scan_bbyy.pdf',bbox_inches='tight')

    bbtautau_path = os.path.join(args.input_path, "limits", "nonres", "bbtautau", "0_kl_*[!summary].json")
    limits_ak_df_bbtautau = get_limits(bbtautau_path,slice(2,-5),rescale_val=1.0/32.776*1000);
    limits_ak_df_bbtautau.to_csv(f'{out_path}/kl_xsec_scan_bbtautau.csv')
    plt = draw_limits(limits_ak_df_bbtautau,r"$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$", status=args.status, use_ampl=not args.ci)
    plt.savefig(f'{out_path}/kl_xsec_scan_bbtautau.pdf',bbox_inches='tight')

    combined_path = os.path.join(args.input_path, "limits", "nonres", "combined", "A-bbtautau_bbyy-fullcorr", "0_kl_*[!summary].json")
    limits_ak_df_combined = get_limits(combined_path,slice(2,-5),rescale_val=1.0/32.776*1000);
    limits_ak_df_combined.to_csv(f'{out_path}/kl_xsec_scan_combined.csv')
    #plt = draw_limits(limits_ak_df_combined,r"$\mathrm{b\bar{b}\gamma\gamma + b\bar{b}\tau^{+}\tau^{-}}$", status=args.status, use_ampl=not args.ci)
    #plt.savefig(f'{out_path}/kl_xsec_scan_all.pdf',bbox_inches='tight')

    plt = draw_all_limits(args.status,
                    (limits_ak_df_bbyy,r"$\mathrm{b\bar{b}\gamma\gamma}$"),
                    (limits_ak_df_bbtautau,r"$\mathrm{b\bar{b}\tau^{+}\tau^{-}}$"),
                    (limits_ak_df_combined,"Combined"),
                    use_ampl=not args.ci)
    plt = draw_limits(limits_ak_df_combined,r"$\mathrm{b\bar{b}\gamma\gamma + b\bar{b}\tau^{+}\tau^{-}}$", status=args.status, use_ampl=not args.ci)
    plt.savefig(f'{out_path}/kl_xsec_scan_all.pdf',bbox_inches='tight')


if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mPlot kl plots.\033[0m")
    parser.add_argument('-ci', action='store_true', default=False, required=False, help='')
    parser.add_argument('-p', '--status', type=str, default='int', required=False, help='')
    parser.add_argument('-i', '--input_path', type=str, required=True, help='')
    parser.add_argument('--unblind', action='store_true', default=False, required=False, help='')

    args = parser.parse_args()
    main(args)
