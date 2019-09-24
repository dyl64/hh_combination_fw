#!/usr/bin/env python

import os

import ROOT as R
from ROOT import TFile

import RooStat as rs
import aux_utils as utils
import LimitSetting as lset

#################################
### --- Utility functions --- ###
#################################

def write_workspace_with_set_resonance_mass(input_ws_path, output_ws_path, mX=300.0, resonance_mass_varname='mHiggs'):

    tf = TFile(input_ws_path)
    
    ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
    mc = rs.GetModelConfig(ws) 
    
    ws_name = ws.GetName()
    mc_name = mc.GetName()
    firstpoi_name = rs.GetfirstPOINameFromMC(mc)
    
    pois     = mc.GetParametersOfInterest()
    poi      = pois.first()
    poi_name = poi.GetName()

    mHiggs = ws.var(resonance_mass_varname)
    
    mHiggs.setVal(mX)
    ws.writeToFile(output_ws_path)


def print_resonance_mass(input_ws_path, resonance_mass_varname='mHiggs'):
    tf = TFile(output_ws_path)
    
    ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
    mc = rs.GetModelConfig(ws) 
    
    mHiggs = ws.var("mHiggs")
    mHiggs.Print()


def get_resonance_mass_variable(input_ws_path, resonance_mass_varname='mHiggs'):
    tf = TFile(output_ws_path)
    
    ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
    mc = rs.GetModelConfig(ws) 
    
    mHiggs = ws.var("mHiggs")
    return mHiggs


output_ws_folder = '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/spin0/'

mass_ranges = {
                'low_mass' : { 'input_ws_path' :
                              '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/spin0_original/2018_07_26/3000_ggbb_lowmass_unblinded_tH.root',
                              'mass' : 
                              [280]
                               #[260, 275, 300, 325, 350, 400]
                             },
                #'medium_mass' : { 'input_ws_path' :
                              #'/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/spin0_original/2018_07_26/3000_ggbb_lowmass_unblinded_400_tH.root',
                              #'mass' : 
                              #[450]
                             #},
                #'high_mass' : { 'input_ws_path' :
                                #'/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/spin0_original/2018_07_26/4500_ggbb_highmass_res_unblinded_tH.root',
                                #'mass' :
                                #[500, 550, 600, 700, 800, 900, 1000]
                              #}
              }


doLimits = True

for mass_range, options in mass_ranges.items():

    print("Mass range: {}".format(mass_range))

    for mass in options['mass']:

        input_ws_path = options['input_ws_path']
        output_ws_path = os.path.join(output_ws_folder, "{}.root".format(mass))

        print("Writing {}".format(output_ws_path))

        write_workspace_with_set_resonance_mass(input_ws_path, output_ws_path, mX=mass)
        mXvar = get_resonance_mass_variable(output_ws_path)
        mass_in_new_workspace = mXvar.getVal()

        if mass_in_new_workspace != mass:
            print("mass_in_new_workspace: {} doesn't match with mass: {}".format(mass_in_new_workspace, mass) )
        else:
            print("mass_in_new_workspace: {} == mass_to_be_set: {}".format(mass_in_new_workspace, mass) )

        ## -- Run Asimov limits to have a quick cross-check with existing results
        if doLimits:
            output_limit_path = os.path.join(output_ws_folder, "{}_limit_exp.dat".format(mass))
            
            lset.runAsymptoticsCLs_autodetect(output_ws_path,
                                              output_limit_path,
                                              exp_or_obs='exp',
                                              doBetterBands='false',
                                              dataName='obsData',
                                              asimovDataName='',
                                              CL='0.95')
