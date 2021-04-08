#!/usr/bin/env python

import sys
import os
import re
from functools import partial

import workspaceCombiner as wsc
import aux_utils as utils
import git

input_dir_prepath  = ("../input" if len(sys.argv) < 2 else sys.argv[1]) + '/20210309/'
output_dir_prepath = ("../output" if len(sys.argv) < 3 else sys.argv[2]) + '/v140invfb_20210309-2'
new_poiname        = "xsec_br"
exp_or_obs         = "obs"
doBetterBands      = "true"
dataName           = "combData"
asimovDataName     = "asimovData_0"
CL                 = "0.95"
scaling_release    = 'r02'
blind              = True
git_stamp_path     = os.path.join(output_dir_prepath, "git.stamp")

def create_task_arg(type, channel):

    input_dir_path = os.path.join(input_dir_prepath, channel, type)
    job_batch_start = [s for s in sys.argv if 'job_batch_start=' in s]
    job_batch_start = int(job_batch_start[0].split('=')[-1]) if job_batch_start else None
    job_batch_stop   = [s for s in sys.argv if 'job_batch_stop=' in s]
    job_batch_stop   = int(job_batch_stop[0].split('=')[-1]) if job_batch_stop else None

    return (input_dir_path, output_dir_prepath, type, channel, scaling_release, new_poiname,
            exp_or_obs, doBetterBands, dataName, asimovDataName, CL, blind, job_batch_start, job_batch_stop)


channel = [s for s in sys.argv if 'channel=' in s]
if channel:
    channel = channel[0].split('=')[-1]
signal = [s for s in sys.argv if 'signal=' in s]
if signal:
    signal = signal[0].split('=')[-1]

task_list = []
if signal:
    task_list.append( create_task_arg(signal,       channel) )
    nProc = 4
else:
    # task_list.append( create_task_arg('nonres',       'bbbb') )
    # task_list.append( create_task_arg('nonres',       'bbtautau') )
    # task_list.append( create_task_arg('nonres',       'bbyy') )
    task_list.append( create_task_arg('nonres',       'WWWW') )
    #task_list.append( create_task_arg('nonres',       'bbWW') )
    #task_list.append( create_task_arg('nonres',       'WWWW') )
    # task_list.append( create_task_arg('spin0',        'bbbb') )
    # task_list.append( create_task_arg('spin0',        'bbtautau') )
    # task_list.append( create_task_arg('spin0',        'bbyy') )
    #task_list.append( create_task_arg('spin0',        'WWyy') )
    #task_list.append( create_task_arg('spin0',        'bbWW') )
    #task_list.append( create_task_arg('spin0',        'WWWW') )
    #task_list.append( create_task_arg('spin0_boosted_statOnly_fromChannel', 'bbbb') )
    #task_list.append( create_task_arg('spin0_boosted', 'bbtautau') )
    #task_list.append( create_task_arg('spin2_c_1.0',  'bbbb') )
    #task_list.append( create_task_arg('spin2_c_1.0',  'bbtautau') )
    #task_list.append( create_task_arg('spin2_c_1.0',  'bbWW') )
    #task_list.append( create_task_arg('spin2_c_2.0',  'bbbb') )
    #task_list.append( create_task_arg('spin2_c_2.0',  'bbtautau') )
    #task_list.append( create_task_arg('spin2_c_2.0',  'bbWW') )

    # task_list.append( create_task_arg('lambda',  'bbbb') )
    # task_list.append( create_task_arg('lambda',  'bbtautau') )
    # task_list.append( create_task_arg('lambda',  'bbyy') )


    #task_list.append( create_task_arg('nonres_statOnly',       'bbbb') )
    #task_list.append( create_task_arg('nonres_statOnly',       'bbtautau') )
    #task_list.append( create_task_arg('nonres_statOnly',       'bbyy') )
    #task_list.append( create_task_arg('nonres_statOnly',       'WWyy') )
    #task_list.append( create_task_arg('nonres_statOnly',       'bbWW') )
    #task_list.append( create_task_arg('nonres_statOnly',       'WWWW') )
    #task_list.append( create_task_arg('spin0_statOnly',        'bbbb') )
    #task_list.append( create_task_arg('spin0_statOnly',        'bbtautau') )
    #task_list.append( create_task_arg('spin0_statOnly',        'bbyy') )
    #task_list.append( create_task_arg('spin0_statOnly',        'WWyy') )
    #task_list.append( create_task_arg('spin0_statOnly',        'bbWW') )
    #task_list.append( create_task_arg('spin0_statOnly',        'WWWW') )
    #task_list.append( create_task_arg('spin2_c_1.0_statOnly',  'bbbb') )
    #task_list.append( create_task_arg('spin2_c_1.0_statOnly',  'bbtautau') )
    #task_list.append( create_task_arg('spin2_c_1.0_statOnly',  'bbWW') )
    #task_list.append( create_task_arg('spin2_c_2.0_statOnly',  'bbbb') )
    #task_list.append( create_task_arg('spin2_c_2.0_statOnly',  'bbtautau') )
    #task_list.append( create_task_arg('spin2_c_2.0_statOnly',  'bbWW') )

    #task_list.append( create_task_arg('lambda_statOnly',  'bbbb') )
    #task_list.append( create_task_arg('lambda_statOnly',  'bbtautau') )
    # task_list.append( create_task_arg('lambda_statOnly',  'bbyy') )


    #task_list.append( create_task_arg('nonres_140invfb',       'bbtautau') )
    #task_list.append( create_task_arg('nonres_300invfb',       'bbtautau') )
    #task_list.append( create_task_arg('nonres_440invfb',       'bbtautau') )
    #task_list.append( create_task_arg('nonres_140invfb',       'bbyy') )
    #task_list.append( create_task_arg('nonres_440invfb',       'bbyy') )
    #task_list.append( create_task_arg('lambda_140invfb',       'bbtautau') )
    #task_list.append( create_task_arg('lambda_300invfb',       'bbtautau') )
    #task_list.append( create_task_arg('lambda_440invfb',       'bbtautau') )
    #task_list.append( create_task_arg('lambda_140invfb',       'bbyy') )
    #task_list.append( create_task_arg('lambda_440invfb',       'bbyy') )

    #task_list.append( create_task_arg('nonres_140invfb_statOnly',       'bbtautau') )
    #task_list.append( create_task_arg('nonres_300invfb_statOnly',       'bbtautau') )
    #task_list.append( create_task_arg('nonres_440invfb_statOnly',       'bbtautau') )
    #task_list.append( create_task_arg('lambda_140invfb_statOnly',       'bbtautau') )
    #task_list.append( create_task_arg('lambda_300invfb_statOnly',       'bbtautau') )
    #task_list.append( create_task_arg('lambda_440invfb_statOnly',       'bbtautau') )


    #task_list.append( create_task_arg('spin0_interp275',  'bbtautau') )
    #task_list.append( create_task_arg('spin0_interp300',  'bbtautau') )
    #task_list.append( create_task_arg('spin2_c_1.0_interp260',  'bbtautau') )
    #task_list.append( create_task_arg('spin2_c_1.0_interp300',  'bbtautau') )


    #task_list.append( create_task_arg('lambda-test',  'bbbb') )
    #task_list.append( create_task_arg('lambda-test',  'bbtautau') )
    #task_list.append( create_task_arg('lambda-test',  'bbyy') )

    #task_list.append( create_task_arg('nonres_withXsecSyst', 'bbtautau') )
    #task_list.append( create_task_arg('nonres-test', 'bbtautau') )
    #task_list.append( create_task_arg('spin0-interpolated',  'bbbb') )
    #task_list.append( create_task_arg('nonres_testLibIssue', 'bbbb') )
    #task_list.append( create_task_arg('nonres_testLibIssue', 'bbtautau') )
    #task_list.append( create_task_arg('nonres_testLibIssue', 'bbyy') )
    nProc = 16


# - Create a job manager

manager = utils.job_manager(func=wsc.task_pipeline_ws, nProc=nProc)

manager.set_task_args(task_list)
manager.submit()

git.save_hash_to_file(git_stamp_path)
