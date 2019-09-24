#!/usr/bin/env python

import os
import glob

import ROOT as R
from ROOT import TFile

import RooStat as rs

input_folder = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/nonres_440invfb/unsorted_POIs" 
output_folder = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/nonres_440invfb/" 


def write_workspace_with_modified_POI(input_ws_path, output_ws_path, poi_name="mu"):

    tf = TFile(input_ws_path)
    
    ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
    mc = rs.GetModelConfig(ws) 
    
    ws_name = ws.GetName()
    mc_name = mc.GetName()
    
    
    mc.SetParametersOfInterest(poi_name)
    pois = rs.RooArgSet(mc.GetParametersOfInterest())
    
    for poi in pois:
        poi.Print()
    
    poi = pois.argset.first()
    poi.setConstant(False)
    poi.setRange(-1, 100.0)
    poi.Print()
    ws.writeToFile(output_ws_path)




root_files_in_input_folder = glob.glob( os.path.join(input_folder,'*.root') )

for input_ws_path in root_files_in_input_folder:

    filename = os.path.basename(input_ws_path)
    output_ws_path = os.path.join(output_folder, filename)

    write_workspace_with_modified_POI(input_ws_path, output_ws_path, poi_name="npbBSM") #lambda: mu_hh, nonres: npbBSM



