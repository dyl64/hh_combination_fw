#!/usr/bin/env python

import sys
import os
import re
from functools import partial

import workspaceCombiner as wsc
import aux_utils as utils
import git

#input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt40_GeV_wout_syst/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt40_GeV_wout_syst/"


#input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt75_GeV_wout_syst/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt75_GeV_wout_syst/"

#input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt40_GeV_with_syst/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt40_GeV_with_syst/"

#input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt75_GeV_with_syst/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt75_GeV_with_syst/"

input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt40_GeV_wout_syst_bbtautau_stat_only/"
output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/prospects_HL_LHC_bbbb_pt40_GeV_wout_syst_bbtautau_stat_only/"

new_poiname        = "xsec_br"
exp_or_obs         = "exp"
doBetterBands      = "false"
dataName           = "combData"
asimovDataName     = "asimovData_0"
CL                 = "0.95"
scaling_release    = 'r02'
git_stamp_path     = os.path.join(output_dir_prepath, "git.stamp")

def create_task_arg(type, channel):

    input_dir_path = os.path.join(input_dir_prepath, channel, type)

    return (input_dir_path, output_dir_prepath, type, channel, scaling_release, new_poiname,
            exp_or_obs, doBetterBands, dataName, asimovDataName, CL)


task_list = []
task_list.append( create_task_arg('nonres',       'bbbb') )
task_list.append( create_task_arg('nonres',       'bbtautau') )

# - Create a job manager
nProc = 2
manager = utils.job_manager(func=wsc.task_pipeline_ws, nProc=nProc)

manager.set_task_args(task_list)
manager.submit()

git.save_hash_to_file(git_stamp_path)
