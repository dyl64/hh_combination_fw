#!/usr/bin/env python

import aux_utils as utils
import ROOT 

###############################
### --- Exclusion plots --- ###
###############################


def create_single_contour(histo, name, contour_level=1.0):
    """Creates a TGraph containg a single contour curve."""
    _isbatch = ROOT.gROOT.IsBatch()
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine('{}->SetContour({},_lvl)'.format(histo.GetName(), contour_level) )
    
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


##############################
### --- ROOT functions --- ###
##############################


def draw_TPave(x1=0.15, y1=0.75, x2=0.95, y2=0.95, bordersize=1):

    legpave = ROOT.TPave(x1, y1, x2, y2, bordersize, "NB NDC" )
    legpave.SetFillColor(ROOT.kWhite)
    legpave.SetFillStyle(1001)
    legpave.SetLineColor(ROOT.kBlack)
    legpave.SetLineWidth(1)
    legpave.Draw()

    return legpave


def draw_TLine(x1, x2, y1, y2):

    legline = ROOT.TLine(x1, y1, x2, y2) 
    legline.SetLineColor(ROOT.kBlack)
    legline.SetLineWidth(1)
    legline.Draw()
    return legline


def draw_ATLAS_label(text="#it{ATLAS} #bf{#sqrt{s} = 13 TeV, 36.1 fb^{-1}} hMSSM",
                          x1=0.15, y1=0.87, x2=0.95, y2=0.95):

    label = ROOT.TPaveText(x1,y1,x2,y2,"ndc")
    label.SetBorderSize(0)
    label.SetFillStyle(0)
    label.SetFillColor(0)   
    label.AddText(text)
    label.Draw()
    return label


def draw_legend(plot_options,
                     x1=0.20, y1=0.76, x2=0.95, y2=0.85):

    leg = ROOT.TLegend(x1, y1, x2, y2, "", "NDC")
    leg.SetNColumns(2)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)

    for contour_line, options in plot_options.items():

        mode = ''

        if options['doDrawFill']:
            mode += 'F'
        if options['doDrawLine']:
            mode += 'L'

        leg.AddEntry(options['tgraph'], options['legend'], mode)

    leg.Draw()
    return leg


def setup_style():

    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(1)


def get_frame(x1, x2, y1, y2):
    
    frame = ROOT.TH2F("frame",";m_{A} [GeV];tan#beta;", 1, x1, x2, 1, y1, y2)
    frame.SetTitleSize( 0.05 , "X" )
    frame.SetTitleSize( 0.05 , "Y" )
    frame.SetTitleFont( 42 , "X" )
    frame.SetTitleFont( 42 , "Y" )
    frame.SetLabelSize( 0.05 , "X" )
    frame.SetLabelSize( 0.05 , "Y" )
    frame.SetLabelFont( 42 , "X" )
    frame.SetLabelFont( 42 , "Y" )
    frame.SetTitleOffset( 1.4, "X" )
    frame.SetTitleOffset( 1.4, "Y" )

    return frame


def draw_tgraph_contour(tgraph, linecolor=4, fillcolor=4, linestyle=4, alpha=1.0, doDrawFill=False,
        doDrawLine=True, *args, **kwargs):

    color = ROOT.gROOT.GetColor(linecolor)
    color.SetAlpha(alpha)

    tgraph.SetLineColor(linecolor)
    tgraph.SetFillColor(fillcolor)
    tgraph.SetLineStyle(linestyle)
    if doDrawFill:
        tgraph.Draw('Fsame')
    if doDrawLine:
        tgraph.Draw('Lsame')


def mH_labels( list_mH, y_pos=1.0):

    list_labels = []
    for mH in list_mH:
        x_pos = mH - 8
        label = ROOT.TLatex(x_pos, y_pos, str(mH) )
        label.SetTextColor(ROOT.kGray+1)
        label.SetTextFont(42)
        label.SetTextSize(0.030)
        label.SetTextAngle(90)
        label.Draw()
        list_labels.append(label)
    return list_labels


def create_canvas(lmargin=0.15, rmargin=0.05, bmargin=0.15, tmargin=0.25, hres=1000, vres=1000):

    canvas = ROOT.TCanvas("c","",hres,vres)
    canvas.SetMargin(lmargin, rmargin, bmargin, tmargin)
    return canvas


def get_objects(path, object_type="TGraph"):

    list = []
    tf = ROOT.TFile(path)
    next = tf.GetListOfKeys()

    for key in tf.GetListOfKeys():
        cl = ROOT.gROOT.GetClass(key.GetClassName())
        if not cl.InheritsFrom(object_type):
            continue
        list.append(key.ReadObj())

    return tf, list

def load_TGraph(path, graph_name='Graph'):

    tf = ROOT.TFile(path)
    tgraph = tf.Get(graph_name)
    tf.Close()
    return tgraph

