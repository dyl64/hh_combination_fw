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

def write_workspace_with_set_lambda(input_ws_path, output_ws_path, lambdaVal=1.0, lambda_varname='lambda'):

    tf = TFile(input_ws_path)
    
    ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
    mc = rs.GetModelConfig(ws) 
    
    ws_name = ws.GetName()
    mc_name = mc.GetName()
    firstpoi_name = rs.GetfirstPOINameFromMC(mc)
    
    pois     = mc.GetParametersOfInterest()
    poi      = pois.first()
    poi_name = poi.GetName()

    varLambda = ws.var(lambda_varname)
    
    varLambda.setVal(lambdaVal)
    varLambda.setConstant() # added afterwards --> need to test
    ws.writeToFile(output_ws_path)


def print_lambda(input_ws_path, lambda_varname='lambda'):
    tf = TFile(output_ws_path)
    
    ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
    mc = rs.GetModelConfig(ws) 
    
    varLambda = ws.var("lambda")
    varLambda.Print()


def get_lambda_variable(input_ws_path, lambda_varname='lambda'):
    tf = TFile(output_ws_path)
    
    ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
    mc = rs.GetModelConfig(ws) 
    
    varLambda = ws.var("lambda")
    return varLambda


input_ws_path = '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/lambda_440invfb_original/LambdaWorkspace_newyield_projection_noss_440/Combined.root'
output_ws_folder = '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/lambda_440invfb/'

lambda_values = [-20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
#lambda_values = [3]


doLimits = True

for lambda_val in lambda_values:

    print("Lambda value: {}".format(lambda_val))


    output_ws_path = os.path.join(output_ws_folder, "{}.root".format(lambda_val))
    print("Writing {}".format(output_ws_path))
    
    write_workspace_with_set_lambda(input_ws_path, output_ws_path, lambdaVal=lambda_val)
    lambda_var = get_lambda_variable(output_ws_path)
    lambda_in_new_workspace = lambda_var.getVal()
    
    if lambda_in_new_workspace != lambda_val:
        print("lambda_in_new_workspace: {} doesn't match with lambda: {}".format(lambda_in_new_workspace, lambda_val) )
    else:
        print("lambda_in_new_workspace: {} == lambda_to_be_set: {}".format(lambda_in_new_workspace, lambda_val) )
        
    ## -- Run Asimov limits to have a quick cross-check with existing results
    if doLimits:
        output_limit_path = ""

        output_limit_path = os.path.join(output_ws_folder, "{}_limit_exp.dat".format(lambda_val))
        
        lset.runAsymptoticsCLs_autodetect(output_ws_path,
                                          output_limit_path,
                                          exp_or_obs='exp',
                                          doBetterBands='false',
                                          dataName='obsData',
                                          asimovDataName='',
                                          CL='0.95')



#old version

#for lambda_val in lambda_values:
#
#    print("Lambda value: {}".format(lambda_val))
#
#    input_ws_path = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw/test_input/vfinal_02/bbyy/lambda_original/Combined.root"
#    output_ws_path = ""
#    if lambda_val < 0:
#        output_ws_path = os.path.join(output_ws_folder, "0{}.root".format(abs(lambda_val)))
#    else:
#        output_ws_path = os.path.join(output_ws_folder, "{}.root".format(lambda_val))
#    
#    print("Writing {}".format(output_ws_path))
#    
#    write_workspace_with_set_lambda(input_ws_path, output_ws_path, lambdaVal=lambda_val)
#    lambda_var = get_lambda_variable(output_ws_path)
#    lambda_in_new_workspace = lambda_var.getVal()
#    
#    if lambda_in_new_workspace != lambda_val:
#        print("lambda_in_new_workspace: {} doesn't match with lambda: {}".format(lambda_in_new_workspace, lambda_val) )
#    else:
#        print("lambda_in_new_workspace: {} == lambda_to_be_set: {}".format(lambda_in_new_workspace, lambda_val) )
#        
#    ## -- Run Asimov limits to have a quick cross-check with existing results
#    if doLimits:
#        output_limit_path = ""
#        if lambda_val < 0:
#            output_limit_path = os.path.join(output_ws_folder, "0{}_limit_exp.dat".format(abs(lambda_val)))
#        else:
#            output_limit_path = os.path.join(output_ws_folder, "{}_limit_exp.dat".format(lambda_val))
#        
#        lset.runAsymptoticsCLs_autodetect(output_ws_path,
#                                          output_limit_path,
#                                          exp_or_obs='exp',
#                                          doBetterBands='false',
#                                          dataName='obsData',
#                                          asimovDataName='',
#                                          CL='0.95')
        
