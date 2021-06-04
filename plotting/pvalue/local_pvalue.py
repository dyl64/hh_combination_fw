#!/usr/bin/env python
# Rui Zhang 6.2020
# rui.zhang@cern.ch

import sys
import os
import os.path
from datetime import date

from ROOT import *
gROOT.SetBatch(True)
from math import *
from array import array
import pdb
import pandas as pd

data_bbbb_bbtautau = {
    'mass':  [
        1000,
1100,
1200,
1400,
1600,
251,
260,
280,
300,
400,
500,
600,
700,
800,
900,],
        'Observed_pValue': [
# 0.401342,
# 0.00131283,
# 0.0307821,
# 0.0273256,
# 0.120591,
# 0.0246233,
# 0.187753,
# 0.730889,
# 0.498805,
# 0.988059,
# 0.511084,
# 0.949659,
# 0.424439,
# 0.397478,
# 0.129427,
0.0654712,
0.000334102,
0.0181715,
0.0218623,
0.122243,
0.0274915,
0.234553,
0.893728,
0.660085,
0.986365,
0.44285,
0.862179,
0.2583,
0.0809096,
0.0183558,

],
        }

data_bbtautau = {
    'mass': [
251,
260,
280,
300,
325,
350,
400,
450,
500,
550,
600,
700,
800,
900,
1000,
1100,
1200,
1400,
1600,
    ],
    'Observed_pValue': [
0.0312835,
0.262276,
0.94198,
0.746268,
0.837681,
0.915817,
0.961767,
0.850882,
0.398573,
0.884549,
0.657247,
0.16291,
0.00803867,
0.00293355,
0.00149598,
0.00986557,
0.0803663,
0.174713,
0.510668,
    ]
}

data_bbbb = {
    'mass': [
1000,
1100,
1200,
1300,
1400,
1500,
1600,
1800,
251,
260,
280,
300,
400,
500,
600,
700,
800,
900,
    ],
    'Observed_pValue': [
#         0.744821,
# 0.00480809,
# 0.0480638,
# 0.302761,
# 0.0318545,
# 0.0347573,
# 0.120178,
# 0.293239,
# 0.263728,
# 0.164244,
# 0.0307612,
# 0.172778,
# 0.931377,
# 0.61,
# 0.958721,
# 0.613712,
# 0.790914,
# 0.408279,
0.744681,
0.00481031,
0.0481164,
0.303278,
0.0318316,
0.0347413,
0.120227,
0.293444,
0.263728,
0.164244,
0.0307611,
0.172778,
0.931377,
0.61,
0.958721,
0.613712,
0.790914,
0.408223,
    ]
}


def defineCanvas(name, title) :
    canv = TCanvas(name)
    canv.SetTitle(title)
    return canv

def setLegend(leg) :

    leg.SetFillColor(kWhite)
    leg.SetLineColor(kBlack)
    leg.SetTextSize(0.05*0.8)
    leg.SetTextFont(42)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetShadowColor(0)

def setTextPads(textsize) :

    t = TLatex()
    t.SetTextSize(textsize)
    t.SetNDC()
    t.SetTextFont(72)
    t.SetTextColor(1)
    p = TLatex()
    p.SetTextSize(textsize)
    p.SetNDC()
    p.SetTextFont(42)
    p.SetTextColor(1)
    info = TLatex()
    info.SetTextSize(textsize*0.8)
    info.SetNDC()
    info.SetTextFont(42)
    info.SetTextColor(1)
    lumi = TLatex()
    lumi.SetTextSize(textsize*0.8)
    lumi.SetNDC()
    lumi.SetTextFont(42)
    lumi.SetTextColor(1)
    zeroS = TLatex()
    zeroS.SetTextSize(textsize*1.3)
    zeroS.SetNDC()
    zeroS.SetTextFont(42)
    zeroS.SetTextColor(kRed)
    oneS = TLatex()
    oneS.SetTextSize(textsize*1.3)
    oneS.SetNDC()
    oneS.SetTextFont(42)
    oneS.SetTextColor(kRed)

    return t, p, info, lumi, zeroS, oneS

##====main====##

totGr = TMultiGraph()

def get_info(df):
    return df.shape[0], array("d", df['mass'].tolist()), array("d", df['Observed_pValue'].tolist())

all_massPoints = set()
dfs = []
for data in [data_bbbb, data_bbtautau, data_bbbb_bbtautau]:
    dfs.append(pd.DataFrame (data, columns = ['mass', 'Observed_pValue']).sort_values(by=['mass']))
    # print(dfs[-1])
line_color = [kBlue-4, kMagenta+2, 1] # bbyy: kPink-2
titles = ['b#bar{b}b#bar{b}', 'b#bar{b}#tau^{+}#tau^{-}', 'Combined']

canv = defineCanvas("p0_graph", "p0_graph")
leg = TLegend(0.2, 0.2, 0.4, 0.4)
setLegend(leg)

for i, df in enumerate(dfs):
    nPoints, massPoints, Observed_pValue = get_info(df)
    all_massPoints.update(massPoints)
    obsGraph = TGraph(nPoints, massPoints, Observed_pValue)

    canv.SetLogy()
    t, p, info, lumi, zeroS, oneS = setTextPads(0.05)
    obsGraph.SetLineStyle(1)
    obsGraph.SetLineWidth(3-(1*bool(i)))
    obsGraph.SetMarkerStyle(21)
    obsGraph.SetMarkerSize(0.8)
    obsGraph.SetMarkerColor(line_color[i])
    obsGraph.SetLineColor(line_color[i])

    leg.AddEntry(obsGraph, titles[i], "lp")
    totGr.Add(obsGraph)



totGr.Draw("al")
totGr.GetXaxis().SetTitle("m_{X} [GeV]")
totGr.GetYaxis().SetTitle("Local p_{0}")
totGr.GetYaxis().SetTitleOffset(1)
totGr.GetXaxis().SetTitleOffset(0.9)
totGr.GetYaxis().SetRangeUser(5.e-6, 2)
totGr.GetXaxis().SetRangeUser(min(all_massPoints)*0.98, max(all_massPoints)*1.02)
totGr.Draw("lP")
leg.Draw("same")
t.DrawLatex(0.4, 0.28, "ATLAS")
p.DrawLatex(0.53, 0.28, "Internal") # Preliminary
lumi.DrawLatex(0.4, 0.22, "#sqrt{s}=13 TeV, 126--139 fb^{-1}")



def line(value):
    sigma = TF1("sigma", value, min(all_massPoints), max(all_massPoints))
    sigma.SetLineColor(kGray+1)
    sigma.SetLineStyle(7)
    sigma.SetLineWidth(2)
    return sigma

def drawNsigma(n, x, y):
    t = TLatex()
    t.SetTextSize(.03)
    t.SetNDC()
    t.SetTextFont(42)
    t.SetTextColor(kGray+1)
    t.DrawLatex(x, y, "{0} #sigma".format(n))

sigma = []
for i, (p, y) in enumerate(zip(['0.5', "1.58655253931457074e-01", "2.27501319481792086e-02", "1.34989803163009588e-03", "0.000032"], [.78, .69, .58, .48, .28])):
    sigma.append(line(p))
    sigma[-1].Draw('samel')
    drawNsigma(i, .85, y)
    # for df in dfs:
    #     print('Crossing p =',p, ', sigma =', i, ', number =', df[df['Observed_pValue']<float(p)]['Observed_pValue'].count())


for ext in [".pdf"]:
    canv.Print('local_p0' + ext)
