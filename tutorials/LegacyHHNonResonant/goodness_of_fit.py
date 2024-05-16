#!/usr/bin/env python3

# Need xRooFit, suggest to set up environment via:
#       asetup StatAnalysis,0.2,latest # el7
#       asetup StatAnalysis,0.3,latest # el9

# Fitting results should be saved as snapshot in advance

import json
import ROOT

outputs = {}
for channel in ['bbbb','bbyy','bbtautau','combined']:
    if channel == 'bbyy':
        roolist = ROOT.RooLinkedList()
        roolist.Add(ROOT.RooFit.Binned(0))
    else:
        roolist = ROOT.RooLinkedList()
        roolist.Add(ROOT.RooFit.Binned(1))
    c = 'combined/bbbb_bbtautau_bbyy-fullcorr' if channel=='combined' else channel
    f = ROOT.TFile(f"/afs/ihep.ac.cn/users/c/cyz/besfs/HH_comb/hh_combination_fw_new/run_heft_final/output/workspace/heft/{c}/0_fit.root", "READ")
    ws = f.Get("combWS")
    w = ROOT.xRooNode(ws)
    nll = w.nll('combData',roolist)
    initial_nll = nll.get().getVal()
    saturated = nll.saturatedVal()
    outputs[channel] = {"initial_NLL":initial_nll, "saturated":saturated}
    if channel == 'bbbb':
        outputs[channel]["saturated_Iza"] = 49328.6

    for snap in ["SM_fit","SM_fix","chhh_fit","chhh_cgghh_fit","chhh_ctthh_fit","cgghh_ctthh_fit","chhh_cgghh_ctthh_fit","all_fit","bkg_fit"]:
        ws.loadSnapshot(snap)
        w = ROOT.xRooNode(ws)
        nll = w.nll('combData',roolist)
        nll_val = nll.get().getVal()
        pgof = nll.pgof()
        ndof = nll.ndof()
        outputs[channel][snap] = {"NLL":nll_val, "pgof":pgof, "ndof":ndof}
    
    f.Close()

with open('goodness_of_fit.json', 'w') as file:
    json.dump(outputs, file, indent=4)