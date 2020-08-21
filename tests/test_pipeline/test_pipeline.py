#!/usr/bin/env python

import sys
import os
import re
from functools import partial
import traceback

import workspaceCombiner as wsc
import aux_utils as utils
import git


hh_combination_fw_path = os.environ['hh_combination_fw_path']

input_dir_prepath  = os.path.join(hh_combination_fw_path, 'tests/reference_workspaces/')
#input_dir_prepath  = "/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/36invfbWorkspaces/input/36invfb/"
output_dir_prepath = os.path.join(hh_combination_fw_path, 'tests/test_pipeline/test_batch/')

#utils.mkdir_p(output_dir_prepath)

new_poiname        = "xsec_br"
exp_or_obs         = "exp"
doBetterBands      = "false"
dataName           = "combData"
asimovDataName     = "asimovData_0"
CL                 = "0.95"
scaling_release    = 't00'
blind              = False
git_stamp_path     = os.path.join(output_dir_prepath, "git.stamp")

def create_task_arg(type, channel):

    input_dir_path = os.path.join(input_dir_prepath, channel, type)

    return (input_dir_path, output_dir_prepath, type, channel, scaling_release, new_poiname,
            exp_or_obs, doBetterBands, dataName, asimovDataName, CL, blind)


task_list = []
task_list.append( create_task_arg('spin0',        'bbbb') )
task_list.append( create_task_arg('spin0',        'bbtautau') )

# - Create a job manager
nProc = 2
manager = utils.job_manager(func=wsc.task_pipeline_ws, nProc=nProc)

manager.set_task_args(task_list)
try:
    manager.submit()
except:
    raise Exception("".join(traceback.format_exception(*sys.exc_info())))

git.save_hash_to_file(git_stamp_path)
