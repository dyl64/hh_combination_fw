#!/usr/bin/env python

import os
import csv
import ctypes

import aux_utils as utils

import parameter_space as ps
from parameter_space import parameter_point as param_pt

import ROOT

#ROOT.gROOT.ProcessLine(".L external/plotting/exclusion_13TeV.C+")

ROOT.gStyle.SetOptStat(0);

#result_pts_path = '/.data/englert/projects/hh_combination/software/hh_combination_fw/scans/scan_runs/result_pts.dat' 
#result_pts_path = '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/scan_runs/hMSSM_mA_180-500_tanb_1-4_50_by_50_pts.dat'
result_pts_path = '/.data/englert/projects/hh_combination/software/hh_combination_fw/scans/scan_runs/hMSSM_mA_180-600_tanb_1-4_100_by_100/result_pts.dat'


output_dir = '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/exclusion_plots/'

utils.mkdir_p(output_dir)
#output_rootfile_path = '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/histo.root'

model = 'hMSSM'
channels    = ['bbbb', 'bbtautau', 'combined']
limit_types = ['exp',   'obs']

xsec_to_be_compared = ps.models[model]['xsec_to_be_compared']


mA_min = 180.0
mA_max = 500.0
mA_nBins = 51
mA_step = (mA_max - mA_min)/mA_nBins

tanb_min = 1.0
tanb_max = 4.0
tanb_nBins = 51
tanb_step = (tanb_max - tanb_min)/tanb_nBins

#tf = ROOT.TFile(output_rootfile_path, "RECREATE")

G_isLogy = False
G_isLogx = False

G_frame = ROOT.TH2D("frame", ";m_{A}; tan#beta", mA_nBins, mA_min, mA_max, tanb_nBins, tanb_min, tanb_max)

def newLayer():
    null = ROOT.TPad("null", "null", 0, 0, 1, 1);
    null.SetFillStyle(0);
    null.SetFrameFillStyle(0);
    null.Draw()
    null.cd()
    if G_isLogy: gPad.SetLogy()
    if G_isLogx: gPad.SetLogx()
    ROOT.gPad.Update()


def draw_histo(histo, draw_mode, out_fig):
    canvas = ROOT.TCanvas("canvas_tmp","tmpc",1000,800);
    histo.Draw(draw_mode)
    canvas.SaveAs(out_fig)


def draw_contour(histo, output_fig_path):
    canvas = ROOT.TCanvas("canvas_tmp","tmpc",1000,800);
    contour_levels = (ctypes.c_double*2)()
    contour_levels[0] = 1.0
    contour_levels[1] = 2.0
    contour_levels_ptr = ctypes.pointer(contour_levels)
    histo.SetContour(2, ctypes.pointer(contour_levels))
    histo.Draw("CONT0");
    canvas.SaveAs(output_fig_path)

def paintBand(histo, name):
    _isbatch = ROOT.gROOT.IsBatch()
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine('%s->SetContour(1,_lvl)' % histo.GetName() )
    
    _c = ROOT.gPad
    _tmpc = ROOT.TCanvas('tmpc','tmpc',1000,800)
    histo.Draw('cont list')
    _tmpc.Update()
    _conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    
    _g = ROOT.gDirectory;
    _gr_f = ROOT.TFile(name, "RECREATE" );
    _conts.Write();
    ROOT.gDirectory = _g;
    ROOT.gPad = _c
    ROOT.gROOT.SetBatch(_isbatch)


def draw_contours_adv(histo, color, output_basename_path, mode):

    output_rootfile = output_basename_path + ".root"
    output_pdf      = output_basename_path + ".pdf"

    _c = ROOT.gPad;
    _tmpc = ROOT.TCanvas("tmpc","tmpc",1000,800);
    contour_levels = ctypes.c_double(1.0)
    contour_levels_ptr = ctypes.pointer(contour_levels)
    histo.SetContour(1, contour_levels_ptr)
    histo.Draw("cont list");
    
    _tmpc.Update(); 
    _conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours");
    
    # - Save to rotfile
    _g = ROOT.gDirectory;
    _gr_f = ROOT.TFile(output_rootfile, "RECREATE")
    _conts.Write();
    gDirectory = _g;
    
    # draw contours
    _c.cd();
    newLayer();
    G_frame.Draw("AXIS");

    if  _conts.GetEntries() >= 1:

        _conts_lvl0 = _conts.At(0);
        for icurv in range(0, _conts_lvl0.GetEntries()):
            _gr = _conts_lvl0.At(icurv).Clone( "%s_contour_%d".format(histo.GetName(), icurv))

            if mode == 'exp':
                _gr.SetLineWidth( 2 );
                _gr.SetLineStyle( 2 );
                _gr.SetLineColor(color);
                _gr.Draw("C");

            if mode == 'transparent_cover':
                if not ROOT.gStyle.GetCanvasPreferGL():
                    ROOT.gStyle.SetCanvasPreferGL(1)

                    col = ROOT.gROOT.GetColor(color);
                    col.SetAlpha( 0.5 );
                    _gr.SetFillColor( color );
                    _gr.Draw("CF");
                    ROOT.gStyle.SetCanvasPreferGL(0);


    _tmpc.SaveAs(output_pdf)

    return _conts


ROOT.gROOT.ProcessLine('double _lvl[] = {1.0};')
histos = {}

# - Create TH2Ds
for ch in channels:
    histos[ch] = {}
    for limit_type in limit_types:
        xsec_theory_over_limit_ch_limit_type_key = "{}_over_limit_{}_{}".format(xsec_to_be_compared, ch, limit_type)
        histos[ch][limit_type] = ROOT.TH2D(xsec_theory_over_limit_ch_limit_type_key, ";m_{A}; tan#beta", mA_nBins, mA_min,
             mA_max, tanb_nBins, tanb_min, tanb_max)


# - Read in pts
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

#               ROOT.paintBand(hist, ROOT.kOrange, 5, os.path.join() )


# - Create figures
for ch in channels:
    for limit_type in limit_types:

        histo = histos[ch][limit_type]
        xsec_theory_over_limit_ch_limit_type_key = "{}_over_limit_{}_{}".format(xsec_to_be_compared, ch, limit_type)

        contour_filename = "{}_tgraph.root".format(xsec_theory_over_limit_ch_limit_type_key)
        contour_path = os.path.join(output_dir, contour_filename)
        paintBand(histo, contour_path)

        histo_figname = "{}_histo.pdf".format(xsec_theory_over_limit_ch_limit_type_key)
        histo_figpath =  os.path.join(output_dir, histo_figname)

        #ROOT.paintBand(histo, ROOT.kOrange, 5, contour_basename+".root" )
        #draw_histo(histo, "COLZ", histo_figpath)
        #draw_contour(histo, contour_basename_path+'.pdf')
        #draw_contours(histo, ROOT.kOrange, contour_basename_path, mode='transparent_cover')

#tf.Write()
#tf.Close()
