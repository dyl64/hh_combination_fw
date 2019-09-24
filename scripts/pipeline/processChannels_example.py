#!/usr/bin/env python

import sys
import os
import re
from functools import partial

import workspaceCombiner as wsc
import aux_utils as utils
import git

#input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/current/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2017_11_27/"

# - Cross-check
input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/current/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2018_06_28_sign_off/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2018_07_04_bbtautau_lambda_test_Florian/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2018_07_04_bbtautau_lambda_test_David/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2018_07_04_bbtautau_lambda_test_original2/"
#output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2018_08_15/"
output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2018_08_27_bbbb_modified/"

new_poiname        = "xsec_br"
exp_or_obs         = "exp"
doBetterBands      = "false"
dataName           = "combData"
asimovDataName     = "-"
CL                 = "0.95"
scaling_release    = 'r03'
git_stamp_path     = os.path.join(output_dir_prepath, "git.stamp")

def create_task_arg(type, channel):

    input_dir_path = os.path.join(input_dir_prepath, channel, type)

    return (input_dir_path, output_dir_prepath, type, channel, scaling_release, new_poiname,
            exp_or_obs, doBetterBands, dataName, asimovDataName, CL)


task_list = []
#task_list.append( create_task_arg('lambda',       'bbtautau') )
#task_list.append( create_task_arg('lambda',       'bbbb') )
#task_list.append( create_task_arg('lambda',       'bbyy') )
task_list.append( create_task_arg('nonres',       'bbyy') )
task_list.append( create_task_arg('nonres',       'bbbb') )
task_list.append( create_task_arg('nonres',       'bbtautau') )
#task_list.append( create_task_arg('nonres',       'WWyy') )
#task_list.append( create_task_arg('nonres',       'bbWW') )
#task_list.append( create_task_arg('spin0',        'bbbb') )
#task_list.append( create_task_arg('spin0',        'bbtautau') )
#task_list.append( create_task_arg('spin0',        'bbyy') )
#task_list.append( create_task_arg('spin0',        'bbWW') )
#task_list.append( create_task_arg('spin0',        'WWyy') )
#task_list.append( create_task_arg('spin2_c_1.0',  'bbbb') )
#task_list.append( create_task_arg('spin2_c_1.0',  'bbtautau') )
#task_list.append( create_task_arg('spin2_c_1.0',  'bbWW') )
#task_list.append( create_task_arg('spin2_c_2.0',  'bbbb') )
#task_list.append( create_task_arg('spin2_c_2.0',  'bbWW') )

print(task_list)

# - Create a job manager
nProc = 16
manager = utils.job_manager(func=wsc.task_pipeline_ws, nProc=nProc)

manager.set_task_args(task_list)
manager.submit()

git.save_hash_to_file(git_stamp_path)
