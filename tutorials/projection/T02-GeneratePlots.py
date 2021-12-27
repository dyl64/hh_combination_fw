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
from quickstats.utils.common_utils import combine_dict

from pdb import set_trace

### 1. Setup
## 1.1 Global variables related to input
if "hh_combination_fw_path" not in os.environ:
    os.environ['hh_combination_fw_path'] = os.path.abspath("../../")
outdir = "${hh_combination_fw_path}/output/projection_nonres_14TeV_3000ifb/lumi3000ifb/"
#outdir = "${hh_combination_fw_path}/../../FullRun2Workspaces/batches/v3000invfb_20211214_condor/projection_nonres_14TeV_3000ifb/lumi3000ifb/"
outdir = os.path.expandvars(outdir)


syst_scenarios = ['stat_only', 'theo_exp_baseline', 'theo_only', 'run2_syst']
studies = ['SM', 'kl_param', 'kl_individual']
channels = ['bbtautau', 'bbyy']
resonant_type = 'nonres'
combine_tag = 'A-bbtautau_bbyy-fullcorr'

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
    'bbtautau': r'$\mathrm{HH\rightarrow b\bar{b}\tau^+\tau^-}$'+'//Projection from Run 2 data',
    'bbyy': r'$\mathrm{HH\rightarrow b\bar{b}\gamma\gamma}$'+'//Projection from Run 2 data',
    'combined': r'$\mathrm{HH\rightarrow b\bar{b}\tau^+\tau^-} + b\bar{b}\gamma\gamma$'+'//Projection from Run 2 data',
}
syst_scenario_text = {
    'stat_only': r"Non-resonant HH" + "//No syst. unc.",
    'theo_exp_baseline' : r"Non-resonant HH" + "//Baseline",
    'theo_only': r"Non-resonant HH" + "//Theoretical unc. halved",
    'run2_syst': r"Non-resonant HH" + "//Run-2 syst. unc.",
}


## 1.2 Theory calculation related

#Now using values from LHCWHGHHHXGGBGGGXXX
SCALE_GGF = 31.05/31.0358 #31.02/31.0358   #correct to xs at mH = 125.09 
SCALE_VBF = 1.726/(4.581-4.245+1.359) # 1.723/(4.581-4.245+1.359)

def xs_ggF(kl):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
    return (70.3874-50.4111*kl+11.0595*kl**2)*SCALE_GGF #XS in fb

def xs_VBF(kl):
    #https://indico.cern.ch/event/995807/contributions/4184798/attachments/2175756/3683303/VBFXSec.pdf
    return (4.581-4.245*kl+1.359*kl**2)*SCALE_VBF

def xs_HH(kl, s=14):
    if s == 13:
        return xs_ggF(kl) + xs_VBF(kl)
    elif s == 14:
        return xs_ggF(kl)*1.18 + xs_VBF(kl) * 1.19

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

def sigma_upper_HH(kl, s=14):
    error = math.sqrt(sigma_upper_ggF(kl)**2 + sigma_upper_VBF(kl)**2)
    if s == 14:
        error /= 2
    return error

def xs_upper_HH(kl, s=14):
    return xs_HH(kl, s) + sigma_upper_HH(kl, s)

def sigma_lower_ggF(kl):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGHH?redirectedfrom=LHCPhysics.LHCHXSWGHH#Latest_recommendations_for_gluon
    #add the std on ggF HH due to qcd scale, PDF, and mtop in quadrature
    #return xs_ggF(kl) * math.sqrt((min(66.0621-46.7458*kl+10.1673*kl**2, 66.7581-47.721*kl+10.4535*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2 + 0.026**2)
    #new mtop uncertainty:
    return xs_ggF(kl) * math.sqrt((min(57.6809 - 42.9905*kl + 9.58474*kl**2, 58.3769 - 43.9657*kl + 9.87094*kl**2) * SCALE_GGF / xs_ggF(kl) - 1)**2 + 0.03**2)

def sigma_lower_VBF(kl):
    return xs_VBF(kl) * math.sqrt(0.0004**2 + 0.021**2)

def sigma_lower_HH(kl, s=14):
    error = math.sqrt(sigma_lower_ggF(kl)**2 + sigma_lower_VBF(kl)**2)
    if s == 14:
        error /= 2
    return error
    
def xs_lower_HH(kl, s=14):
    return xs_HH(kl, s) - sigma_lower_HH(kl, s)



## 1.3 Helper functions

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


## 1.4 Get SM limit data
## 1.4.1 Get SM limit data for one scenario one lumi
def get_limit_SM(scenario, study, lumi=None):
    data = {}
    for channel in channels + ['combined']:
        limit_path = os.path.join(outdir.replace("lumi3000ifb", f"lumi{lumi}ifb") if lumi else outdir, scenario, study, 'limits', resonant_type, channel, combine_tag if channel == 'combined' else '', 'limits.json')
        data[channel] = json.load(open(limit_path))
        if lumi:
            data[channel]['lumi'] = [lumi]
    if lumi:
        data[channel]['lumi'] = [lumi]
    return data

## 1.4.2 get SM limit data for one scenario all lumi
def merge_limit_SM_lumi(scenario, study='SM'):
    data_all = []
    for lumi in [1000, 1500, 2000, 2500, 3000]:
        data = get_limit_SM(scenario, study, lumi)
        data_all.append(data)

    for key, value in data_all[0].items():
        for key2, value2 in value.items():
            for data_new in data_all[1:]:
                value2.extend(data_new[key][key2])
    return data_all[0]

## 1.4.3 get SM limit data for one scenario one lumi
def merge_limit_SM_scen():
    sm_limit_df = {}
    sm_limit_df2 = {}
    for scenario in syst_scenarios:
        data = get_limit_SM(scenario, 'SM')
        # flatten 1 point limit
        for k,v in data.items():
            for p,v_ in v.items():
                data[k][p] = v_[0]
        # channel-based df
        for channel in data:
            if channel not in sm_limit_df2:
                sm_limit_df2[channel] = {}
            sm_limit_df2[channel][scenario] = data[channel]
        # scenario-based df
        sm_limit_df[scenario] = pd.DataFrame(data)
    for channel in sm_limit_df2:
        sm_limit_df2[channel] = pd.DataFrame(sm_limit_df2[channel])

    return sm_limit_df, sm_limit_df2


## 1.5 Get likelihood data
## 1.5.1 Get likelihood data for one scenario under kl hypothesis
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


## 1.6 Get pvalue/significance data
## 1.6.1 Get pvalue/significance data for one scenario one lumi
def get_pvalue_SM(scenario, lumi):
    data = {}
    for channel in channels:
        limit_path = os.path.join(outdir.replace("lumi3000ifb", f"lumi{lumi}ifb"), scenario, 'SM', 'pvalues', resonant_type, channel, '0_asimovData_1_NP_Nominal_mu_0.json')
        data[channel] = json.load(open(limit_path))
    limit_path = os.path.join(outdir.replace("lumi3000ifb", f"lumi{lumi}ifb"), scenario, 'SM', 'pvalues', resonant_type, 'combined', combine_tag, '0_asimovData_1_NP_Nominal_mu_0.json')
    data['combined'] = json.load(open(limit_path))
    # filter columns
    results = {}
    for channel in data:
        results[channel] = {k:[v] for k,v in data[channel].items() if k in ['pvalue', 'significance', 'qmu']}
        results[channel].update({k:[v] for k,v in data[channel]['uncond_fit'].items() if k in ['muhat', 'muhat_errlo', 'muhat_errhi']})
        results[channel]['lumi'] = [lumi]
    return results

## 1.6.2 Get pvalue/significance data for one scenario all lumi
def merge_pvalue_SM_lumi(scenario):
    data_all = []
    for lumi in [1000, 1500, 2000, 2500, 3000]:
        data = get_pvalue_SM(scenario, lumi)
        data_all.append(data)

    for key, value in data_all[0].items():
        for key2, value2 in value.items():
            for data_new in data_all[1:]:
                value2.extend(data_new[key][key2])
    return data_all[0]

## 1.6.3 Get pvalue/significance data for all scenario one lumi (not used)
def merge_pvalue_SM_scen():
    pvalue_df  = {}
    pvalue_df2 = {}
    for scenario in syst_scenarios:
        pvalue_df[scenario] = {}
        data = get_pvalue_SM(scenario, 3000)
        pvalue_df[scenario] = pd.DataFrame(data).transpose()
        for channel in data:
            if channel not in pvalue_df2:
                pvalue_df2[channel] = {}
            pvalue_df2[channel][scenario] = data[channel]
    for channel in data:
        pvalue_df2[channel] = pd.DataFrame(pvalue_df2[channel]).transpose()
        set_trace()
        print('channel', channel, 'pvalue', pvalue_df2[channel])

## 1.6.5 Get pvalue/significance data for all individual kl for one scenario
def merge_pvalue_kl(scenario):
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
            limit_path = os.path.join(outdir, scenario, 'kl_individual', 'pvalues', resonant_type, channel, combine_tag if channel == 'combined' else '', file_prefix+'_asimovData_1_NP_Nominal_mu_0.json')
            result = json.load(open(limit_path))
            data[channel]['kl'].append(point['kl'])
            for column in columns[1:]:
                data[channel][column].append(result[column])
        #json.dump(data[channel][channel], f'significance_kl_{channel}.json', indent=2)
    return data

## 1.6.7 (not used)
def get_pvalue_data_kl(scenario):
    data = {}
    for channel in channels:
        limit_path = os.path.join(outdir, scenario, 'kl_individual', 'pvalues', resonant_type, channel, 'result_asimovData_1_NP_Nominal_mu_0.json')
        data[channel] = json.load(open(limit_path))
    limit_path = os.path.join(outdir, scenario, 'SM', 'pvalues', resonant_type, 'combined', combine_tag, 'result_asimovData_1_NP_Nominal_mu_0.json')
    data['combined'] = json.load(open(limit_path))
    for channel in data:
        data[channel] = {k:v for k,v in data[channel].items() if k in ['pvalue', 'significance', 'qmu']}
    return data



## Global settings
analysis_label_options_default = {
    'energy': '14 TeV',
    'lumi': '3000 fb$^{-1}$',
    'fontsize': 30,
    'loc': (0.05, 0.95),
}
styles_default = {
'kl_likelihood_chan_mu1': {
    'legend':{
        'loc': (0.23, 0.43),
        },
    },
'kl_likelihood_chan_mu0': {
    'legend':{
        'loc': (1.02, 0.43),
        },
    },
'kl_likelihood_scen_mu1': {
    'legend':{
        'loc': (0.23, 0.47),
        },
    },
'kl_likelihood_scen_mu0': {
    'legend':{
        'loc': (1.02, 0.47),
        },
    },
'kl_significance': {
    'legend':{
        'loc': (0.27, 0.43),
        },
    },
'kl_xsec': {
    'legend':{
        'loc': (0.58, 0.67),
        'fontsize': 17
        }
    },
'kl_comp': {
    'legend':{
        'loc': (0.5, 0.67),
        'fontsize': 15
        }
    },
'lumi_scan': {
    'legend':{
        'loc': (0.52, 0.68),
        'fontsize': 17
        }
    }
}

## 2. SM Limit Plot

def plotting_SM():
    sm_limit_df, sm_limit_df2 = merge_limit_SM_scen()
    os.makedirs("plots/csv/", exist_ok=True)
    for key, value in sm_limit_df.items():
        value.to_csv(f"plots/csv/SM_limit__{key}.csv")
    for key, value in sm_limit_df2.items():
        value.to_csv(f"plots/csv/SM_limit__{key}.csv")

    for channel in ['bbyy', 'bbtautau', 'combined']:
        analysis_label_options_new = {'extra_text': channel_text[channel] + '//' + r'$\sigma_{ggF+VBF}^{SM}=32.78$ fb'}
        analysis_label_options = combine_dict(analysis_label_options_default, analysis_label_options_new)
        plotter = UpperLimit1DPlot(sm_limit_df2[channel], syst_scenario_label_map, analysis_label_options=analysis_label_options)
        plotter.draw(xlabel=r"95% CL upper limit on signal strength", draw_observed=False)
        plt.savefig(f"plots/SM_limit_{channel}.pdf", bbox_inches="tight")
        print('Save fig', f"plots/SM_limit_{channel}.pdf")


## 3. KL Limit Scan
def theory_kl_curve(reference):
    klambda_values = reference.index.astype(float).values
    scale_factor = np.array([xs_HH(kl, s=14) for kl in klambda_values])
    klambda_theory_values = np.linspace(min(klambda_values), max(klambda_values), 1000) 
    theory_xs_values = np.array([xs_HH(kl, s=14) for kl in klambda_theory_values])
    theory_xs_lower = np.array([xs_lower_HH(kl, s=14) for kl in klambda_theory_values])
    theory_xs_upper = np.array([xs_upper_HH(kl, s=14) for kl in klambda_theory_values])
    return klambda_values, scale_factor, klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper


#### 3.1 Individual workspace limits
def data_loading_indiv():
    kl_individual_limit_df  = {}
    kl_individual_limit_df2 = {}
    for scenario in syst_scenarios:
        kl_individual_limit_df[scenario] = {}
        data = get_limit_SM(scenario, 'kl_individual')
        for channel in data:
            df = pd.DataFrame(data[channel]).set_index(['klambda'])
            if channel not in kl_individual_limit_df2:
                kl_individual_limit_df2[channel] = {}
            kl_individual_limit_df[scenario][channel] = df
            kl_individual_limit_df2[channel][scenario] = df
    return kl_individual_limit_df, kl_individual_limit_df2


def plotting_kl_indiv():
    syst_scenario = 'theo_exp_baseline'
    kl_individual_limit_df, kl_individual_limit_df2 = data_loading_indiv()
    os.makedirs("plots/csv/", exist_ok=True)
    for channel, value in kl_individual_limit_df2.items():
        for scenario, df in value.items():
            df.to_csv(f'plots/csv/kl_limit_{scenario}_individual_ws_{channel}.csv')

    for channel in ['bbyy', 'bbtautau', 'combined']:
        analysis_label_options_new = {
            'extra_text':channel_text[channel]
        }
        analysis_label_options = combine_dict(analysis_label_options_default, analysis_label_options_new)
        styles = styles_default['kl_xsec']
        
        klambda_values, scale_factor, klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper = theory_kl_curve(kl_individual_limit_df2['bbyy']['theo_exp_baseline'])
        plotter = UpperLimit2DPlot(kl_individual_limit_df2[channel][syst_scenario], scale_factor=scale_factor, styles=styles, analysis_label_options=analysis_label_options)
        plotter.add_curve(klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper, label="Theory prediction")
        plotter.add_highlight(1, xs_HH(1, s=14), label="SM prediction")
        ax = plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel=r"$\sigma_{ggF+VBF}(HH) [fb]$", draw_observed=False, log=True, ylim=[7, 1.5e3], xlim=[-2,6])
        intersections = get_intersections(klambda_values, scale_factor*kl_individual_limit_df2[channel][syst_scenario]['0'], klambda_theory_values, theory_xs_values)
        ax.annotate(r'Expected: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.05, 0.08), xycoords = 'axes fraction', fontsize = 15)
        plt.savefig(f"plots/kl_limit_{syst_scenario}_individual_ws_{channel}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/kl_limit_{syst_scenario}_individual_ws_{channel}.pdf")



#### 3.2 Parameterised workspace limits
def data_loading_param():
    kl_param_limit_df  = {}
    kl_param_limit_df2 = {}
    for scenario in syst_scenarios:
        kl_param_limit_df[scenario] = {}
        data = get_limit_SM(scenario, 'kl_parameterised')
        for channel in data:
            df = pd.DataFrame(data[channel]).set_index(['klambda'])
            if channel not in kl_param_limit_df2:
                kl_param_limit_df2[channel] = {}
            kl_param_limit_df[scenario][channel] = df
            kl_param_limit_df2[channel][scenario] = df
    return kl_param_limit_df, kl_param_limit_df2

def plotting_kl_param():
    syst_scenario = 'theo_exp_baseline'
    kl_param_limit_df, kl_param_limit_df2 = data_loading_param()
    for channel in ['bbyy', 'bbtautau', 'combined']:
        analysis_label_options_new = {
            'extra_text':channel_text[channel] + '//Parameterised workspace'    
        }
        analysis_label_options = combine_dict(analysis_label_options_default, analysis_label_options_new)
        styles = styles_default['kl_xsec']
        
        klambda_values, scale_factor, klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper = theory_kl_curve(kl_param_limit_df2['bbyy']['theo_exp_baseline'])
        plotter = UpperLimit2DPlot(kl_param_limit_df2[channel][syst_scenario], scale_factor=scale_factor, styles=styles, analysis_label_options=analysis_label_options)
        plotter.add_curve(klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper, label="Theory prediction")
        plotter.add_highlight(1, xs_HH(1, s=14), label="SM prediction")
        ax = plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel=r"$\sigma_{ggF+VBF}(HH) [fb]$", draw_observed=False, log=True, ylim=[7, 1.5e3], xlim=[-2,6])
        intersections = get_intersections(klambda_values, scale_factor*kl_param_limit_df2[channel][syst_scenario]['0'], klambda_theory_values, theory_xs_values)
        ax.annotate(r'Expected: $\kappa_\lambda \in [%.1f, %.1f]$' %(intersections[0], intersections[1]), (0.05, 0.08), xycoords = 'axes fraction', fontsize = 15)
        plt.savefig(f"plots/kl_limit_{syst_scenario}_parameterised_ws_{channel}.pdf", bbox_inches="tight")
        print('Save fig', f"plots/kl_limit_{syst_scenario}_parameterised_ws_{channel}.pdf")



#### 3.3 Parameterised vs Individual workspace plot
def plot_kl_param_vs_indiv():
    syst_scenario = 'theo_exp_baseline'
    kl_individual_limit_df, kl_individual_limit_df2 = data_loading_indiv()
    for channel in ['bbyy', 'bbtautau', 'combined']:
        analysis_label_options_new = {
            'extra_text':channel_text[channel] + '//Indiv. WS vs Param. WS'    
        }
        analysis_label_options = combine_dict(analysis_label_options_default, analysis_label_options_new)
        styles = styles_default['kl_comp']
        
        LABELS = {
            '2sigma': 'Expected limit $\pm 2\sigma$ [indiv. ws]',
            '1sigma': 'Expected limit $\pm 1\sigma$ [indiv. ws]',
            'expected': 'Expected limit (95% CL) [indiv. ws]',
            'observed': 'Observed limit (95% CL) [indiv. ws]'
        }
        
        LABELS_SEC = {
            '2sigma': 'Expected limit $\pm 2\sigma$ [param. ws]',
            '1sigma': 'Expected limit $\pm 1\sigma$ [param. ws]',
            'expected': 'Expected limit (95% CL) [param. ws]',
            'observed': 'Observed limit (95% CL) [param. ws]'
        }
        
        kl_param_limit_df, kl_param_limit_df2 = data_loading_param()
        klambda_values, scale_factor, klambda_theory_values, theory_xs_values, theory_xs_lower, theory_xs_upper = theory_kl_curve(kl_param_limit_df2['bbyy']['theo_exp_baseline'])
        plotter = UpperLimit2DPlot(kl_individual_limit_df2[channel][syst_scenario],
                                   kl_param_limit_df2[channel][syst_scenario],
                                   scale_factor=scale_factor, styles=styles,
                                   labels=LABELS,
                                   labels_sec=LABELS_SEC,
                                   analysis_label_options=analysis_label_options)
        plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel=r"$\sigma_{ggF+VBF}(HH) [fb]$", draw_observed=False, log=True, ylim=[8, 4e3], xlim=[-2,6])
        plt.savefig(f"plots/kl_limit_{syst_scenario}_comparison_ws_{channel}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/kl_limit_{syst_scenario}_comparison_ws_{channel}.pdf")


## 4. KL Likelihood Scan
## 4.0 Get likelihood data for all scenario under kl hypothesis
def data_loading_lh(klhypo):
    likelihood_df  = {}
    likelihood_df2 = {}
    for scenario in syst_scenarios:
        likelihood_df[scenario] = {}
        data = get_likelihood_data(scenario, klhypo)
        for channel in data:
            df = pd.DataFrame(data[channel]).dropna()
            if channel not in likelihood_df2:
                likelihood_df2[channel] = {}
            likelihood_df[scenario][channel] = df
            likelihood_df2[channel][scenario] = df
    return likelihood_df, likelihood_df2

likelihood_df, likelihood_df2 = {}, {}
likelihood_df[0], likelihood_df2[0] = data_loading_lh(0)
likelihood_df[1], likelihood_df2[1] = data_loading_lh(1)

styles_map = {}
styles_map['scenario'] = {
    'stat_only': {"color": "#343844", "marker": "P"},
    'theo_exp_baseline':  {"color": "#F2385A", "marker": "o"},
    'theo_only': {"color": "#FDC536", "marker": "s"},
    'run2_syst': {"color": "#36B1BF", "marker": "d"}
}
styles_map['channel'] = {
    'bbyy'    : {"color": "#9A0EEA", "marker": "v"},
    'bbtautau': {"color": "#008F00", "marker": "^"},
    'combined': {"color": "#000000", "marker": "o"}
}

from scipy.interpolate import interp1d
def get_intersections2(df, level):
    xvalues = df['mu'].to_numpy()
    yvalues = df['qmu'].to_numpy()
    func_theory = interp1d(xvalues, yvalues)
    x_new = np.arange(min(xvalues), max(xvalues), 0.01)
    y_new = func_theory(x_new)
    
    asign = np.sign(y_new-level)
    signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)
    return x_new[signchange==1]


#### 4.1 Channel-based plot
def plot_lh_chan(klhypo):
    
    analysis_label_options_new = {
        1: {
            'loc': (0.23, 0.95),
        },
        0: {
            'loc': (1.02, 0.95),
        },
    }
    analysis_label_options = combine_dict(analysis_label_options_default, analysis_label_options_new[klhypo])
    styles = styles_default[f'kl_likelihood_chan_mu{klhypo}']
    os.makedirs("plots/csv/", exist_ok=True)
    for kl, value in likelihood_df2.items():
        for channel, v in value.items():
            for scenario, df in v.items():
                df.to_csv(f"plots/csv/likelihood_scan_mu_{kl}_{channel}_{scenario}.csv")

    intersects = {}
    for channel in channels + ['combined']:
        channel_analysis_label_options = {**analysis_label_options, 'extra_text':channel_text[channel]}
        plotter = Likelihood1DPlot(likelihood_df2[klhypo][channel], label_map=syst_scenario_label_map, styles_map=styles_map['scenario'], styles=styles, analysis_label_options=channel_analysis_label_options)

        intersects[channel] = {}
        for scenario, df in likelihood_df2[klhypo][channel].items():
            intersects[channel][scenario] = {}
            for level in [1, 4]:
                intersections = get_intersections2(df, level)
                intersects[channel][scenario][level] = intersections.tolist()

        plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ymax=20, xmin=-2, xmax=8, draw_sigma_line=True)
        plt.savefig(f"plots/likelihood_scan_mu_{klhypo}_{channel}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/likelihood_scan_mu_{klhypo}_{channel}.pdf")

    with open(f'plots/csv/likelihood_scan_mu_{klhypo}.json', 'w') as f:
        print('save', f'plots/csv/likelihood_scan_mu_{klhypo}.json')
        json.dump(intersects, f, indent=2)
        print(json.dumps(intersects, indent=2))


#### 4.2 Scenario-based plot
def plot_lh_scen(klhypo):
    analysis_label_options_new = {
        1: {
            'loc': (0.23, 0.95),
        },
        0: {
            'loc': (1.02, 0.95),
        },
    }
    analysis_label_options = combine_dict(analysis_label_options_default, analysis_label_options_new[klhypo])
    styles = styles_default[f'kl_likelihood_scen_mu{klhypo}']

    for syst_scenario in syst_scenarios:
        channel_analysis_label_options = {**analysis_label_options, 'extra_text':syst_scenario_text[syst_scenario]}
        plotter = Likelihood1DPlot(likelihood_df[klhypo][syst_scenario], label_map=channel_label_map, styles_map=styles_map['channel'], styles=styles, analysis_label_options=channel_analysis_label_options)
        plotter.draw(xlabel=r"$\mathrm{\kappa_{\lambda}}$", ymax=20, xmin=-2, xmax=8, draw_sigma_line=True)
        plt.savefig(f"plots/likelihood_scan_mu_{klhypo}_{syst_scenario}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/likelihood_scan_mu_{klhypo}_{syst_scenario}.pdf")


## 5. P-Value & significance
## 5.1. kl scan (channel based)
def merge_pvalue_data_kl_scen():
    significance_df  = {}
    significance_df2 = {}
    for scenario in syst_scenarios:
        significance_df[scenario] = {}
        data = merge_pvalue_kl(scenario)
        for channel in data:
            df = pd.DataFrame(data[channel]).dropna()
            if channel not in significance_df2:
                significance_df2[channel] = {}
            significance_df[scenario][channel] = df
            significance_df2[channel][scenario] = df
    return significance_df, significance_df2


def plot_significance_chan():
    
    analysis_label_options_new = {
        'loc': (0.27, 0.95),
    }
    analysis_label_options = combine_dict(analysis_label_options_default, analysis_label_options_new)
    config = {
        'sigma_values': (3, 5),
        'sigma_line_styles':{
            'color': 'gray',
            'linestyle': '--'
        }
    }
    styles = styles_default['kl_significance']

    significance_df, significance_df2 = merge_pvalue_data_kl_scen()
    for channel in channels + ['combined']:
        channel_analysis_label_options = {**analysis_label_options, 'extra_text':channel_text[channel]}
        plotter = Likelihood1DPlot(significance_df2[channel], label_map=syst_scenario_label_map, styles_map=styles_map['scenario'], styles=styles, analysis_label_options=channel_analysis_label_options)
        plotter.config = combine_dict(plotter.config, config)
        plotter.draw(xattrib='kl', yattrib='significance', xlabel=r"$\mathrm{\kappa_{\lambda}}$", ylabel="Significance [$\sigma$]", ymax=12, xmin=-2, xmax=8, draw_sigma_line=True)
        plt.savefig(f"plots/significance_scan_{channel}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/significance_scan_{channel}.pdf")


# ## 4.2. lumi scan (channel based)

def merge_pvalue_SM_lumi_scen():
    lumi_df  = {}
    lumi_df2 = {}
    for scenario in syst_scenarios:
        lumi_df[scenario] = {}
        data = merge_pvalue_SM_lumi(scenario)
        for channel in data:
            df = pd.DataFrame(data[channel]).dropna()
            if channel not in lumi_df2:
                lumi_df2[channel] = {}
            lumi_df[scenario][channel] = df
            lumi_df2[channel][scenario] = df
    return lumi_df, lumi_df2


def plot_significance_lumi():
    
    analysis_label_options = analysis_label_options_default
    config = {
        'sigma_values': (),
        'sigma_line_styles':{
            'color': 'gray',
            'linestyle': '--'
        }
    }
    styles = styles_default['lumi_scan']

    pvalue_lumi_df, pvalue_lumi_df2 = merge_pvalue_SM_lumi_scen()
    os.makedirs("plots/csv/", exist_ok=True)
    for channel, value in pvalue_lumi_df2.items():
        for scenario, df in value.items():
            df.to_csv(f"plots/csv/significance_lumi_{channel}__{scenario}.csv")
    for channel in channels + ['combined']:
        channel_analysis_label_options = {**analysis_label_options, 'extra_text':channel_text[channel]}
        plotter = Likelihood1DPlot(pvalue_lumi_df2[channel], label_map=syst_scenario_label_map, styles_map=styles_map['scenario'], 
                                   styles=styles, analysis_label_options=channel_analysis_label_options)
        plotter.config = combine_dict(plotter.config, config)
        plotter.draw(xattrib='lumi', yattrib='significance', xlabel=r"Integrated Luminosity [fb$^{-1}$]", ylabel="Significance [$\sigma$]", ymax=7, xmin=800, xmax=3200, draw_sigma_line=True)
        plt.savefig(f"plots/significance_lumi_{channel}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/significance_lumi_{channel}.pdf")


## 
def merge_limit_SM_lumi_scen():
    limit_lumi_df  = {}
    limit_lumi_df2 = {}
    for scenario in syst_scenarios:
        limit_lumi_df[scenario] = {}
        data = merge_limit_SM_lumi(scenario)
        for channel in data:
            df = pd.DataFrame(data[channel]).dropna()
            if channel not in limit_lumi_df2:
                limit_lumi_df2[channel] = {}
            limit_lumi_df[scenario][channel] = df
            limit_lumi_df2[channel][scenario] = df
    return limit_lumi_df, limit_lumi_df2


def plot_limit_lumi():
    analysis_label_options = analysis_label_options_default
    config = {
        'sigma_values': (),
        'sigma_line_styles':{
            'color': 'gray',
            'linestyle': '--'
        }
    }

    limit_lumi_df, limit_lumi_df2 = merge_limit_SM_lumi_scen()
    os.makedirs("plots/csv/", exist_ok=True)
    for channel, value in limit_lumi_df2.items():
        for scenario, df in value.items():
            df.to_csv(f"plots/csv/limit_lumi_{channel}__{scenario}.csv")
    for channel in channels + ['combined']:
        channel_analysis_label_options = {**analysis_label_options, 'extra_text':channel_text[channel]}
        styles = styles_default['lumi_scan']
        if channel == 'bbyy':
            channel_analysis_label_options['loc'] = (0.05, 0.30)
            styles['legend']['loc'] = (0.52, 0.05)
        plotter = Likelihood1DPlot(limit_lumi_df2[channel], label_map=syst_scenario_label_map, styles_map=styles_map['scenario'], styles=styles, analysis_label_options=channel_analysis_label_options)
        plotter.config = combine_dict(plotter.config, config)
        plotter.draw(xattrib='lumi', yattrib='0', xlabel=r"Integrated Luminosity [fb$^{-1}$]", ylabel="95% CL Upper Limit on Signal Strength", ymax=3, xmin=800, xmax=3200, draw_sigma_line=True)
        plt.savefig(f"plots/limit_lumi_{channel}.pdf", bbox_inches="tight")
        print("Save fig", f"plots/limit_lumi_{channel}.pdf")

plotting_SM()
plotting_kl_indiv()
plotting_kl_param()
plot_kl_param_vs_indiv()
for i in [0, 1]:
    plot_lh_chan(i)
    plot_lh_scen(i)
plot_significance_chan()
plot_significance_lumi()
plot_limit_lumi()
