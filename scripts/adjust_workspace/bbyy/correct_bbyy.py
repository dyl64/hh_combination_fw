#!/usr/bin/env python


import os

import ROOT as R
from ROOT import TFile

import RooStat as rs
import aux_utils as utils

#input_ws_path  = "./1265_ggbb_nonres_expo.root" 
#input_ws_path  = "../current/bbyy/nonres/0.root" 
input_ws_path  = "./1265_ggbb_nonres_expo.root" 
output_ws_path = "../../current/bbyy/nonres/0.root"

tf = TFile( input_ws_path )

ws = rs.GetTypeFromTFile(tf, type="RooWorkspace")
mc = rs.GetModelConfig(ws) 

ws_name = ws.GetName()
mc_name = mc.GetName()
firstpoi_name = rs.GetfirstPOINameFromMC(mc)

pois     = mc.GetParametersOfInterest()
poi      = pois.first()
poi_name = poi.GetName()


print("Workspace name:   {0}".format(ws_name))
print("ModelConfig name: {0}".format(mc_name))
print("First POI name:   {0}".format(firstpoi_name))

# - Old method - #
#print(pois)

#iter = pois.createIterator()
#poi = iter.Next()
#while poi:
#    print(poi.GetName())
#    poi = iter.Next()
#
#

pois_argset = rs.RooArgSet(pois)
for i, poi in enumerate(pois_argset):
    msg = "{} name: {}".format(i, poi.GetName())
    print(msg)

mu         = ws.var("mu")
mu_XS_VBF  = ws.var("mu_XS_VBF")
mu_XS_ggF  = ws.var("mu_XS_ggF")


print("--- Before ---")

mu.Print()
mu_XS_VBF.Print()
mu_XS_ggF.Print()

print("mu isConstant: {}".format(mu.isConstant()) )
print("mu_XS_ggF isConstant: {}".format(mu_XS_ggF.isConstant()) )
print("mu_XS_VBF isConstant: {}".format(mu_XS_VBF.isConstant()) )

#############################
### --- Modifications --- ###
#############################

mu.setConstant()
mu_XS_ggF.setConstant()
mu_XS_VBF.setConstant()

mu.setVal(1.0)
mu_XS_ggF.setVal(1.0)
mu_XS_VBF.setVal(1.0)

#############################

print("--- After ---")

print("mu isConstant: {}".format(mu.isConstant()) )
print("mu_XS_ggF isConstant: {}".format(mu_XS_ggF.isConstant()) )
print("mu_XS_VBF isConstant: {}".format(mu_XS_VBF.isConstant()) )

mu.Print()
mu_XS_VBF.Print()
mu_XS_ggF.Print()

ws.writeToFile(output_ws_path)

# - mu_XS_VBF
# - mu_XS_ggF

#mc.Print()
#ws.Print()

#for poi in pois:
#    print(poi.GetName())
