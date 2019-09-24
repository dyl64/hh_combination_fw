#!/usr/bin/env python

import os
import csv
import ctypes

import aux_utils as utils

import parameter_space as ps
from parameter_space import parameter_point as param_pt
import root_plot as rplot

import ROOT

ROOT.gStyle.SetOptStat(0);

#result_pts_path = '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/scan_runs/hMSSM_mA_180-500_tanb_1-4_50_by_50_pts.dat'
result_pts_path = '/.data/englert/projects/hh_combination/software/hh_combination_fw/scans/scan_runs/hMSSM_mA_180-600_tanb_1-4_100_by_100/result_pts.dat'
output_dir = '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/exclusion_plots/'

utils.mkdir_p(output_dir)

model = 'hMSSM'
channels    = ['bbbb', 'bbtautau', 'combined']
limit_types = ['exp',   'obs']

xsec_to_be_compared = ps.models[model]['xsec_to_be_compared']

mA_min = 180.0
mA_max = 600.0
mA_nBins = 101
mA_step = (mA_max - mA_min)/mA_nBins

tanb_min = 1.0
tanb_max = 4.0
tanb_nBins = 101
tanb_step = (tanb_max - tanb_min)/tanb_nBins

ROOT.gROOT.ProcessLine('double _lvl[] = {1.0};')
histos = {}

### --- Create TH2Ds --- ###
for ch in channels:
    histos[ch] = {}
    for limit_type in limit_types:
        xsec_theory_over_limit_ch_limit_type_key = "{}_over_limit_{}_{}".format(xsec_to_be_compared, ch, limit_type)
        histos[ch][limit_type] = ROOT.TH2D(xsec_theory_over_limit_ch_limit_type_key, ";m_{A}; tan#beta", mA_nBins, mA_min,
             mA_max, tanb_nBins, tanb_min, tanb_max)


### --- Read in pts --- ###
with open(result_pts_path , 'r') as inp:
    reader = csv.DictReader(inp, delimiter=' ')

    for pt in reader:

        pt = param_pt.from_dict(model, pt) 
        mA   = pt['mA']
        tanb = pt['tanb']

        for ch in channels:
            for limit_type in limit_types:
                histo = histos[ch][limit_type]
                xsec_theory_over_limit_ch_limit_type_key = "{}_over_limit_{}_{}".format(xsec_to_be_compared, ch, limit_type)

                try:
                    xsec_theory_over_limit_ch_limit_type = float(pt[xsec_theory_over_limit_ch_limit_type_key])
                except:
                    xsec_theory_over_limit_ch_limit_type = 0.0

                #print("{}: {} {}".format(pt, xsec_theory_over_limit_ch_limit_type_key,
                #    xsec_theory_over_limit_ch_limit_type))
    
                gbin = histo.FindBin(float(mA), float(tanb))
                histo.SetBinContent(gbin, xsec_theory_over_limit_ch_limit_type)


### --- Create figures --- ###
for ch in channels:
    for limit_type in limit_types:

        histo = histos[ch][limit_type]
        xsec_theory_over_limit_ch_limit_type_key = "{}_over_limit_{}_{}".format(xsec_to_be_compared, ch, limit_type)

        contour_tgraph_filename = "{}_tgraph.root".format(xsec_theory_over_limit_ch_limit_type_key)
        contour_tgraph_path = os.path.join(output_dir, contour_tgraph_filename)
        rplot.create_single_contour(histo, contour_tgraph_path)

        histo_figname = "{}_histo.pdf".format(xsec_theory_over_limit_ch_limit_type_key)
        histo_figpath =  os.path.join(output_dir, histo_figname)
