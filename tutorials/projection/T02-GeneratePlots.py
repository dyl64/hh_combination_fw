import os
import math
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from quickstats.plots import UpperLimit1DPlot
from quickstats.plots import UpperLimit2DPlot
from quickstats.plots import Likelihood1DPlot
from quickstats.plots.color_schemes import QUICKSTATS_PALETTES
color_pallete = QUICKSTATS_PALETTES['darklines']

from pdb import set_trace

if "hh_combination_fw_path" not in os.environ:
    os.environ['hh_combination_fw_path'] = os.path.abspath("../../")
outdir = "${hh_combination_fw_path}/output0/projection_nonres_14TeV_3000ifb/lumi3000ifb/"
outdir = os.path.expandvars(outdir)


syst_scenarios = ['stat_only', 'theo_exp_baseline', 'theo_only', 'run2_syst']
studies = ['SM', 'kl_param', 'kl_individual']
channels = ['bbtautau', 'bbyy']
resonant_type = 'nonres'
combine_tag = 'A-bbtautau_bbyy-fullcorr'


def get_limit_data(scenario, study):
    data = {}
    for channel in channels:
        limit_path = os.path.join(outdir, scenario, study, 'limits', resonant_type, channel, 'limits.json')
        data[channel] = json.load(open(limit_path))
    limit_path = os.path.join(outdir, scenario, study, 'limits', resonant_type, 'combined',
                              combine_tag, 'limits.json')
    data['combined'] = json.load(open(limit_path))
    return data
def get_likelihood_data(scenario, klhypo):
    data = {}
    for channel in channels:
        limit_path = os.path.join(outdir, scenario, 'kl_parameterised', 'likelihood_scans', resonant_type, channel, 
                                  f'klambda_{klhypo}', 'klambda.json')
        data[channel] = json.load(open(limit_path))
    limit_path = os.path.join(outdir, scenario, 'kl_parameterised', 'likelihood_scans', resonant_type, 'combined',
                              combine_tag, f'klambda_{klhypo}', 'klambda.json')
    data['combined'] = json.load(open(limit_path))
    return data
def get_pvalue_data(scenario, lumi):
    data = {}
    for channel in channels:
        limit_path = os.path.join(outdir.replace("lumi3000ifb", f"lumi{lumi}ifb"), scenario, 'SM', 'pvalues', resonant_type, channel, 
                                  '0_asimovData_1_NP_Nominal_mu_0.json')
        data[channel] = json.load(open(limit_path))
    limit_path = os.path.join(outdir.replace("lumi3000ifb", f"lumi{lumi}ifb"), scenario, 'SM', 'pvalues', resonant_type, 'combined',
                              combine_tag, '0_asimovData_1_NP_Nominal_mu_0.json')
    data['combined'] = json.load(open(limit_path))
    # filter columns
    for channel in data:
        data[channel] = {k:[v] for k,v in data[channel].items() if k in ['pvalue', 'significance', 'qmu']}
        data[channel]['lumi'] = [lumi]
    return data
def merge_pvalue_data_lumi(scenario):
    data_all = []
    for lumi in [1000, 1500, 2000, 2500, 3000]:
        data = get_pvalue_data(scenario, lumi)
        data_all.append(data)

    for key, value in data_all[0].items():
        for key2, value2 in value.items():
            for data_new in data_all[1:]:
                value2.extend(data_new[key][key2])
    return data_all[0]

def merge_pvalue_data_kl(scenario):
    from quickstats.components import ParamParser
    file_expr = "<mass[F]>_kl_<klambda[P]>"
    param_expr = 'kl=-2_8_0.2'
    para = ParamParser(file_expr, param_expr)
    int_param_points = para.get_internal_param_points()
    columns = ['kl', 'pvalue', 'significance']
    data = {}
    for channel in channels+['combined']:
        data[channel] = {}
        for column in columns:
            data[channel][column] = []
        for point in int_param_points:
            file_prefix = '0_'+para.str_encode_parameters(point)
            limit_path = os.path.join(outdir, scenario, 'kl_individual', 'pvalues', resonant_type, channel, combine_tag if channel == 'combined' else '',
                                      file_prefix+'_asimovData_1_NP_Nominal_mu_0.json')
            result = json.load(open(limit_path))
            data[channel]['kl'].append(point['kl'])
            for column in columns[1:]:
                data[channel][column].append(result[column])
        #json.dump(data[channel][channel], f'significance_kl_{channel}.json', indent=2)
    return data

def get_pvalue_data_kl(scenario):
    data = {}
    for channel in channels:
        limit_path = os.path.join(outdir, scenario, 'kl_individual', 'pvalues', resonant_type, channel, 
                                  'result_asimovData_1_NP_Nominal_mu_0.json')
        data[channel] = json.load(open(limit_path))
    limit_path = os.path.join(outdir, scenario, 'SM', 'pvalues', resonant_type, 'combined',
                              combine_tag, 'result_asimovData_1_NP_Nominal_mu_0.json')
    data['combined'] = json.load(open(limit_path))
    for channel in data:
        data[channel] = {k:v for k,v in data[channel].items() if k in ['pvalue', 'significance', 'qmu']}
    return data


syst_scenario_label_map = {
    'stat_only': r"No syst. unc.",
    'theo_exp_baseline' : r"Baseline",
    'theo_only': r"Theoretical unc. halved",
    'run2_syst': r"Run-2 syst. unc.",
}
channel_label_map = {
    'bbyy': r"$\mathrm{b\bar{b}\gamma\gamma}$",
    'bbtautau': r"$\mathrm{b\bar{b}\tau^+\tau^-}$",
    'combined': r"Combined",
}
channel_text = {
    'bbtautau': r'$\mathrm{HH\rightarrow b\bar{b}\tau^+\tau^-}$',
    'bbyy': r'$\mathrm{HH\rightarrow b\bar{b}\gamma\gamma}$',
    'combined': r'$\mathrm{HH\rightarrow b\bar{b}\tau^+\tau^-} + b\bar{b}\gamma\gamma$',
}
syst_scenario_text = {
    'stat_only': r"Non-resonant HH, No syst. unc.",
    'theo_exp_baseline' : r"Non-resonant HH, Baseline",
    'theo_only': r"Non-resonant HH, Theoretical unc. halved",
    'run2_syst': r"Non-resonant HH, Run-2 syst. unc.",
}


## ## 1. SM Limit Plot
#
## ### 1.1 Data Loading
#
#def data_loading():
#    sm_limit_df = {}
#    sm_limit_df2 = {}
#    for scenario in syst_scenarios:
#        data = get_limit_data(scenario, 'SM')
#        # flatten 1 point limit
#        for k,v in data.items():
#            for p,v_ in v.items():
#                data[k][p] = v_[0]
#        # channel-based df
#        for channel in data:
#            if channel not in sm_limit_df2:
#                sm_limit_df2[channel] = {}
#            sm_limit_df2[channel][scenario] = data[channel]
#        # scenario-based df
#        sm_limit_df[scenario] = pd.DataFrame(data)
#    for channel in sm_limit_df2:
#        sm_limit_df2[channel] = pd.DataFrame(sm_limit_df2[channel])
#    return sm_limit_df, sm_limit_df2
#sm_limit_df, sm_limit_df2 = data_loading()
#
#
## ### 1.2 Plotting
#
#def plotting():
#    for channel in ['bbyy', 'bbtautau', 'combined']:
#        analysis_label_options = {'fontsize':30, 'energy': '14 TeV', 
#                                  'lumi': '3000 fb$^{-1}$',
#                                  'extra_text': channel_text[channel] + '//' + r'$\sigma_{ggF+VBF}^{SM}=32.78$ fb'}
#        plotter = UpperLimit1DPlot(sm_limit_df2[channel], syst_scenario_label_map,
#                                   analysis_label_options=analysis_label_options)
#        plotter.draw(xlabel=r"95% CL upper limit on signal strength", draw_observed=False)
#        plt.savefig(f"plots/SM_limit_{channel}.pdf", bbox_inches="tight")
#        print('Save fig', f"plots/SM_limit_{channel}.pdf")
#
#plotting()
#
#
## ## 2. KL Limit Scan
#
## ### 2.1 Data Loading
#
## #### 2.1a Individual workspace limits
#def data_loading_indiv():
#    kl_individual_limit_df  = {}
#    kl_individual_limit_df2 = {}
#    for scenario in syst_scenarios:
#        kl_individual_limit_df[scenario] = {}
#        data = get_limit_data(scenario, 'kl_individual')
#        for channel in data:
#            df = pd.DataFrame(data[channel]).set_index(['klambda'])
#            if channel not in kl_individual_limit_df2:
#                kl_individual_limit_df2[channel] = {}
#            kl_individual_limit_df[scenario][channel] = df
#            kl_individual_limit_df2[channel][scenario] = df
#    return kl_individual_limit_df, kl_individual_limit_df2
#kl_individual_limit_df, kl_individual_limit_df2 = data_loading_indiv()
#
## #### 2.1b Parameterised workspace limits
#def data_loading_param():
#    kl_param_limit_df  = {}
#    kl_param_limit_df2 = {}
#    for scenario in syst_scenarios:
#        kl_param_limit_df[scenario] = {}
#        data = get_limit_data(scenario, 'kl_parameterised')
#        for channel in data:
#            df = pd.DataFrame(data[channel]).set_index(['klambda'])
#            if channel not in kl_param_limit_df2:
#                kl_param_limit_df2[channel] = {}
#            kl_param_limit_df[scenario][channel] = df
#            kl_param_limit_df2[channel][scenario] = df
#    return kl_param_limit_df, kl_param_limit_df2
#kl_param_limit_df, kl_param_limit_df2 = data_loading_param()
#
## ### 2.2 Plotting
#
##Now using values from LHCWHGHHHXGGBGGGXXX
#SCALE_GGF = 31.05/31.0358 #31.02/31.0358   #correct to xs at mH = 125.09 
#SCALE_VBF = 1.726/(4.581-4.245+1.359) # 1.723/(4.581-4.245+1.359)
#
#def xs_ggF(kl):
#    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
#    return (70.3874-50.4111*kl+11.0595*kl**2)*SCALE_GGF #XS in fb
#
#def xs_VBF(kl):
#    #https://indico.cern.ch/event/995807/contributions/4184798/attachments/2175756/3683303/VBFXSec.pdf
#    return (4.581-4.245*kl+1.359*kl**2)*SCALE_VBF
#
#def xs_HH(kl, s=14):
#    if s == 13:
#        return xs_ggF(kl) + xs_VBF(kl)
#    elif s == 14:
#        return xs_ggF(kl)*1.18 + xs_VBF(kl) * 1.19
#
## When adding 2 independent Gaussians (e.g. ggF and VBF XS) we can simply add their means and add their sigmas in quadrature
#def sigma_upper_ggF(kl):
#    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
#    #add the std on ggF HH due to qcd scale, PDF, and mtop in quadrature
#    #return xs_ggF(kl) * math.sqrt((max(72.0744-51.7362*kl+11.3712*kl**2, 70.9286-51.5708*kl+11.4497*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2 + 0.026**2)
#    #new mtop uncertainty:
#    return xs_ggF(kl) * math.sqrt((max(76.6075 - 56.4818*kl + 12.635*kl**2, 75.4617 - 56.3164*kl + 12.7135*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2)
#
#def sigma_upper_VBF(kl):
#    #from klambda = 1
#    return xs_VBF(kl) * math.sqrt(0.0003**2 + 0.021**2)
#
#def sigma_upper_HH(kl, s=14):
#    error = math.sqrt(sigma_upper_ggF(kl)**2 + sigma_upper_VBF(kl)**2)
#    if s == 14:
#        error /= 2
#    return error
#
#def xs_upper_HH(kl, s=14):
#    return xs_HH(kl, s) + sigma_upper_HH(kl, s)
#
#def sigma_lower_ggF(kl):
#    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
#    #add the std on ggF HH due to qcd scale, PDF, and mtop in quadrature
#    #return xs_ggF(kl) * math.sqrt((min(66.0621-46.7458*kl+10.1673*kl**2, 66.7581-47.721*kl+10.4535*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2 + 0.026**2)
#    #new mtop uncertainty:
#    return xs_ggF(kl) * math.sqrt((min(57.6809 - 42.9905*kl + 9.58474*kl**2, 58.3769 - 43.9657*kl + 9.87094*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2)
#
#def sigma_lower_VBF(kl):
#    return xs_VBF(kl) * math.sqrt(0.0004**2 + 0.021**2)
#
#def sigma_lower_HH(kl, s=14):
#    error = math.sqrt(sigma_lower_ggF(kl)**2 + sigma_lower_VBF(kl)**2)
#    if s == 14:
#        error /= 2
#    return error
#    
#def xs_lower_HH(kl, s=14):
#    return xs_HH(kl, s) - sigma_lower_HH(kl, s)
#
#def get_intersections(lambdas, n_exp, lambdas_th, n_th):
#    # get the intersection between expected and theory prediction
#    
#    # interpolate expected limit with same number of datapoints as used in theory prediction
#    interpolated_limit = np.interp(lambdas_th, lambdas, n_exp) 
#
#    #limitm1 = n*np.array(limit_bands[0]) - 1
#    limitm1 = interpolated_limit - n_th 
#    idx = np.argwhere(np.diff(np.sign(limitm1))).flatten() # determines what index intersection points are at 
#
#    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
#    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
#    intersections = [lambdas_th[x] - (lambdas_th[x+1] - lambdas_th[x])/(limitm1[x+1] - limitm1[x]) * limitm1[x] for x in idx]
#    return intersections
#
#
#
#klambda_values = kl_individual_limit_df2['bbyy']['theo_exp_baseline'].index.astype(float).values
#scale_factor = np.array([xs_HH(kl, s=14) for kl in klambda_values])
#
#klambda_theory_values = np.linspace(min(klambda_values), max(klambda_values), 1000) 
#theory_xs_values = np.array([xs_HH(kl, s=14) for kl in klambda_theory_values])
#theory_xs_lower = np.array([xs_lower_HH(kl, s=14) for kl in klambda_theory_values])
#theory_xs_upper = np.array([xs_upper_HH(kl, s=14) for kl in klambda_theory_values])
#
## #### 3.2a Individual workspace plot
#def plotting_kl_indiv():
#    syst_scenario = 'theo_exp_baseline'
#    for channel in ['bbyy', 'bbtautau', 'combined']:
#        analysis_label_options = {
#            'loc': (0.05, 0.95),
#            'energy': '14 TeV',
#            'lumi': r'3000 fb$^{-1}$',
#            'fontsize': 30,
#            'extra_text':channel_text[channel] + '//Individual workspace'    
#        }
#        styles = {
#            'legend':{
#                'loc': (0.58, 0.67),
#                'fontsize': 17
#            }
#        }
#        
#        plotter = UpperLimit2DPlot(kl_individual_limit_df2[channel][syst_scenario], 
#                                   scale_factor=scale_factor, styles=styles,
#                                   analysis_label_options=analysis_label_options)
#        plotter.add_curve(klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper, 
#                          label="Theory prediction")
#        plotter.add_highlight(1, xs_HH(1, s=14),
#                              label="SM prediction")
#        ax = plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel=r"$\sigma_{ggF+VBF}(HH) [fb]$",
#                     draw_observed=False, log=True, ylim=[7, 1.5e3], xlim=[-2,6])
#        intersections = get_intersections(klambda_values, 
#                                          scale_factor*kl_individual_limit_df2[channel][syst_scenario]['0'],
#                                          klambda_theory_values, theory_xs_values)
#        ax.annotate(r'Expected: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), 
#                    (0.05, 0.08), xycoords = 'axes fraction', fontsize = 15)
#        plt.savefig(f"plots/kl_limit_{syst_scenario}_individual_ws_{channel}.pdf", bbox_inches="tight")
#        print("Save fig", f"plots/kl_limit_{syst_scenario}_individual_ws_{channel}.pdf")
#
#plotting_kl_indiv()
#
## #### 3.2b Parameterised workspace plot
#def plotting_kl_param():
#    syst_scenario = 'theo_exp_baseline'
#    for channel in ['bbyy', 'bbtautau', 'combined']:
#        analysis_label_options = {
#            'loc': (0.05, 0.95),
#            'energy': '14 TeV',
#            'lumi': r'3000 fb$^{-1}$',
#            'fontsize': 30,
#            'extra_text':channel_text[channel] + '//Parameterised workspace'    
#        }
#        styles = {
#            'legend':{
#                'loc': (0.58, 0.68),
#                'fontsize': 17
#            }
#        }
#        
#        plotter = UpperLimit2DPlot(kl_param_limit_df2[channel][syst_scenario], 
#                                   scale_factor=scale_factor, styles=styles,
#                                   analysis_label_options=analysis_label_options)
#        plotter.add_curve(klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper, 
#                          label="Theory prediction")
#        plotter.add_highlight(1, xs_HH(1, s=14),
#                              label="SM prediction")
#        ax = plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel=r"$\sigma_{ggF+VBF}(HH) [fb]$",
#                     draw_observed=False, log=True, ylim=[7, 1.5e3], xlim=[-2,6])
#        intersections = get_intersections(klambda_values, 
#                                          scale_factor*kl_individual_limit_df2[channel][syst_scenario]['0'],
#                                          klambda_theory_values, theory_xs_values)
#        ax.annotate(r'Expected: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), 
#                    (0.05, 0.08), xycoords = 'axes fraction', fontsize = 15)
#        plt.savefig(f"plots/kl_limit_{syst_scenario}_parameterised_ws_{channel}.pdf", bbox_inches="tight")
#        print('Save fig', f"plots/kl_limit_{syst_scenario}_parameterised_ws_{channel}.pdf")
#
#plotting_kl_param()
#
#
## #### 3.2c Parameterised vs Individual workspace plot
#def plot_kl_param_vs_indiv():
#    syst_scenario = 'theo_exp_baseline'
#    for channel in ['bbyy', 'bbtautau', 'combined']:
#        analysis_label_options = {
#            'loc': (0.05, 0.95),
#            'energy': '14 TeV',
#            'lumi': r'3000 fb$^{-1}$',
#            'fontsize': 30,
#            'extra_text':channel_text[channel] + '//Indiv. WS vs Param. WS'    
#        }
#        styles = {
#            'legend':{
#                'loc': (0.5, 0.68),
#                'fontsize': 15
#            }
#        }
#        
#        LABELS = {
#            '2sigma': 'Expected limit $\pm 2\sigma$ [indiv. ws]',
#            '1sigma': 'Expected limit $\pm 1\sigma$ [indiv. ws]',
#            'expected': 'Expected limit (95% CL) [indiv. ws]',
#            'observed': 'Observed limit (95% CL) [indiv. ws]'
#        }
#        
#        LABELS_SEC = {
#            '2sigma': 'Expected limit $\pm 2\sigma$ [param. ws]',
#            '1sigma': 'Expected limit $\pm 1\sigma$ [param. ws]',
#            'expected': 'Expected limit (95% CL) [param. ws]',
#            'observed': 'Observed limit (95% CL) [param. ws]'
#        }
#        
#        plotter = UpperLimit2DPlot(kl_individual_limit_df2[channel][syst_scenario],
#                                   kl_param_limit_df2[channel][syst_scenario],
#                                   scale_factor=scale_factor, styles=styles,
#                                   labels=LABELS,
#                                   labels_sec=LABELS_SEC,
#                                   analysis_label_options=analysis_label_options)
#        plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel=r"$\sigma_{ggF+VBF}(HH) [fb]$",
#                     draw_observed=False, log=True, ylim=[8, 4e3], xlim=[-2,6])
#        plt.savefig(f"plots/kl_limit_{syst_scenario}_comparison_ws_{channel}.pdf", bbox_inches="tight")
#        print("Save fig", f"plots/kl_limit_{syst_scenario}_comparison_ws_{channel}.pdf")
#
#plot_kl_param_vs_indiv()
#
#
## ## 3. KL Likelihood Scan
#
## ### 3.1 Data Loading
#def data_loading_lh(klhypo):
#    likelihood_df  = {}
#    likelihood_df2 = {}
#    for scenario in syst_scenarios:
#        likelihood_df[scenario] = {}
#        data = get_likelihood_data(scenario, klhypo)
#        for channel in data:
#            df = pd.DataFrame(data[channel]).dropna()
#            if channel not in likelihood_df2:
#                likelihood_df2[channel] = {}
#            likelihood_df[scenario][channel] = df
#            likelihood_df2[channel][scenario] = df
#    return likelihood_df, likelihood_df2
#
#likelihood_df, likelihood_df2 = {}, {}
#likelihood_df[0], likelihood_df2[0] = data_loading_lh(0)
#likelihood_df[1], likelihood_df2[1] = data_loading_lh(1)
#
#
## ### 3.2 Plotting
#
## #### 3.2a Channel-based plot
#def plot_lh_chan(klhypo):
#    styles_map = {
#        'stat_only': {"color": "#343844", "marker": "P"},
#        'theo_exp_baseline':  {"color": "#F2385A", "marker": "o"},
#        'theo_only': {"color": "#FDC536", "marker": "s"},
#        'run2_syst': {"color": "#36B1BF", "marker": "d"}
#    }
#    
#    styles = {
#        'legend':{
#            'loc': (0.25, 0.45)
#        }
#    }
#    analysis_label_options = {
#        'loc': (0.25, 0.95),
#        'energy': '14 TeV',
#        'lumi': r'3000 fb$^{-1}$',
#        'fontsize': 30
#    }
#
#    for channel in ['bbyy', 'bbtautau', 'combined']:
#        channel_analysis_label_options = {**analysis_label_options, 'extra_text':channel_text[channel]}
#        plotter = Likelihood1DPlot(likelihood_df2[klhypo][channel], label_map=syst_scenario_label_map, styles_map=styles_map, 
#                                   styles=styles, analysis_label_options=channel_analysis_label_options)
#        plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ymax=12, xmin=-2.5, xmax=8, draw_sigma_line=True)
#        plt.savefig(f"plots/likelihood_scan_mu_{klhypo}_{channel}.pdf", bbox_inches="tight")
#        print("Save fig", f"plots/likelihood_scan_mu_{klhypo}_{channel}.pdf")
#
#for i in [0, 1]:
#    plot_lh_chan(i)
#
## #### 3.2a Scenario-based plot
#def plt_lh_scen(klhypo):
#    styles_map = {
#        'bbyy'    : {"color": "#F2385A", "marker": "P"},
#        'bbtautau': {"color": "#FDC536", "marker": "s"},
#        'combined': {"color": "#36B1BF", "marker": "o"}
#    }
#    
#    styles = {
#        'legend':{
#            'loc': (0.25, 0.5)
#        }
#    }
#    analysis_label_options = {
#        'loc': (0.25, 0.95),
#        'energy': '14 TeV',
#        'lumi': r'3000 fb$^{-1}$',
#        'fontsize': 30
#    }
#    for syst_scenario in ['theo_exp_baseline']:
#        channel_analysis_label_options = {**analysis_label_options, 'extra_text':syst_scenario_text[syst_scenario]}
#        plotter = Likelihood1DPlot(likelihood_df[klhypo][syst_scenario], label_map=channel_label_map, styles_map=styles_map, 
#                                   styles=styles, analysis_label_options=channel_analysis_label_options)
#        plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ymax=12, xmin=-2, xmax=8.5, draw_sigma_line=True)
#        plt.savefig(f"plots/likelihood_scan_mu_{klhypo}_{syst_scenario}.pdf", bbox_inches="tight")
#        print("Save fig", f"plots/likelihood_scan_mu_{klhypo}_{syst_scenario}.pdf")
#
#for i in [0, 1]:
#    plt_lh_scen(i)
#
#
## ## 4. P-Value & significance
#
## ## 4.0. SM
##def pvalue():
##    pvalue_df  = {}
##    pvalue_df2 = {}
##    for scenario in syst_scenarios:
##        pvalue_df[scenario] = {}
##        data = get_pvalue_data(scenario)
##        pvalue_df[scenario] = pd.DataFrame(data).transpose()
##        for channel in data:
##            if channel not in pvalue_df2:
##                pvalue_df2[channel] = {}
##            pvalue_df2[channel][scenario] = data[channel]
##    for channel in data:
##        pvalue_df2[channel] = pd.DataFrame(pvalue_df2[channel]).transpose()
##        print('channel', channel, 'pvalue', pvalue_df2[channel])
##
## ## 4.1. kl scan (channel based)

#def data_loading_sig():
#    significance_df  = {}
#    significance_df2 = {}
#    for scenario in syst_scenarios:
#        significance_df[scenario] = {}
#        data = merge_pvalue_data_kl(scenario)
#        for channel in data:
#            df = pd.DataFrame(data[channel]).dropna()
#            if channel not in significance_df2:
#                significance_df2[channel] = {}
#            significance_df[scenario][channel] = df
#            significance_df2[channel][scenario] = df
#    return significance_df, significance_df2
#
#significance_df, significance_df2 = data_loading_sig()
#
#def plot_significance_chan():
#    from quickstats.utils.common_utils import combine_dict
#    styles_map = {
#        'stat_only': {"color": "#343844", "marker": "P"},
#        'theo_exp_baseline':  {"color": "#F2385A", "marker": "o"},
#        'theo_only': {"color": "#FDC536", "marker": "s"},
#        'run2_syst': {"color": "#36B1BF", "marker": "d"}
#    }
#    
#    styles = {
#        'legend':{
#            'loc': (0.25, 0.45)
#        }
#    }
#    analysis_label_options = {
#        'loc': (0.25, 0.95),
#        'energy': '14 TeV',
#        'lumi': r'3000 fb$^{-1}$',
#        'fontsize': 30
#    }
#    config = {
#        'sigma_values': (3, 5),
#        'sigma_line_styles':{
#            'color': 'gray',
#            'linestyle': '--'
#        }
#    }
#
#    for channel in ['bbyy', 'bbtautau', 'combined']:
#        channel_analysis_label_options = {**analysis_label_options, 'extra_text':channel_text[channel]}
#        plotter = Likelihood1DPlot(significance_df2[channel], label_map=syst_scenario_label_map, styles_map=styles_map, 
#                                   styles=styles, analysis_label_options=channel_analysis_label_options)
#        plotter.config = combine_dict(plotter.config, config)
#        plotter.draw(xattrib='kl', yattrib='significance', xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel="Significance [$\sigma$]", ymax=12, xmin=-2.5, xmax=8, draw_sigma_line=True)
#        plt.savefig(f"plots/significance_scan_{channel}.pdf", bbox_inches="tight")
#        print("Save fig", f"plots/significance_scan_{channel}.pdf")
#
#plot_significance_chan()
#
# ## 4.2. lumi scan (channel based)

def data_loading_lumi():
    lumi_df  = {}
    lumi_df2 = {}
    for scenario in syst_scenarios:
        lumi_df[scenario] = {}
        data = merge_pvalue_data_lumi(scenario)
        for channel in data:
            df = pd.DataFrame(data[channel]).dropna()
            if channel not in lumi_df2:
                lumi_df2[channel] = {}
            lumi_df[scenario][channel] = df
            lumi_df2[channel][scenario] = df
    return lumi_df, lumi_df2

lumi_df, lumi_df2 = data_loading_lumi()

def plot_significance_lumi():
    from quickstats.utils.common_utils import combine_dict
    styles_map = {
        'stat_only': {"color": "#343844", "marker": "P"},
        'theo_exp_baseline':  {"color": "#F2385A", "marker": "o"},
        'theo_only': {"color": "#FDC536", "marker": "s"},
        'run2_syst': {"color": "#36B1BF", "marker": "d"}
    }
    
    styles = {
        'legend':{
            'loc': (0.55, 0.65)
        }
    }
    analysis_label_options = {
        'loc': (0.05, 0.95),
        'energy': '14 TeV',
        'lumi': r'3000 fb$^{-1}$',
        'fontsize': 30
    }
    config = {
        'sigma_values': (),
        'sigma_line_styles':{
            'color': 'gray',
            'linestyle': '--'
        }
    }

    for channel in ['bbyy', 'bbtautau', 'combined']:
        channel_analysis_label_options = {**analysis_label_options, 'extra_text':channel_text[channel]}
        plotter = Likelihood1DPlot(lumi_df2[channel], label_map=syst_scenario_label_map, styles_map=styles_map, 
                                   styles=styles, analysis_label_options=channel_analysis_label_options)
        plotter.config = combine_dict(plotter.config, config)
        plotter.draw(xattrib='lumi', yattrib='significance', xlabel=r"Integrated Luminosity [fb$^{-1}$]", ylabel="Significance [$\sigma$]", ymax=7, xmin=800, xmax=3200, draw_sigma_line=True)
        plt.savefig(f"plots/significance_lumi_{channel}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/significance_lumi_{channel}.pdf")

plot_significance_lumi()
