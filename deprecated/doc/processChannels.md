# `processChannels`


## Settings

**Variables you should modify or make sure they are the ones you actually want:**
- `input_dir_prepath`: path to the input directory.

    The input workspaces should be stored in the following format:
        - `./<channel>/<type>/<mass>.root`
    
    For the naming conventions please see the framework [conventions][conventions].

    Example:
        - `./bbbb/spin0/300.root`
    

    
- `nProc`: Number of processes you'd like to use in parallel.
- `output_dir_prepath`: path to the output directory
- `scaling_release`: Release version of the scaling factors, see
    [python_modules/scalings.py](./python_modules/scalings.py)

**Auxiliary variables:**
- `new_poiname`: name of the new POI
- `exp_or_obs`: obsolete - both exp and observed limits are calculated
- `doBetterBands`: doBetterBands flag inside `runAsymptoticsCLs`
- `dataName`: name of the observed data within the workspace. Default: combData
- `asimovDataName`: name of the asimovData
- `CL`: confidence level


## How it works in a nutshell

The `task_list` is created and appended by each `<type>-<channel>` pair. The task list is just a
list of arguments supplied to the task function, in this case `wsc.task_pipeline_ws`. The set of
tasks is processed my the job manager, `manager`.

## Source code

~~~~
import sys
import os
import re
from functools import partial

import workspaceCombiner as wsc
import aux_utils as utils
import git

input_dir_prepath  = "/.data/englert/projects/hh_combination/workspaces/current/"
output_dir_prepath = "/.data/englert/projects/hh_combination/workspaces/2017_12_18_without_bbyy/"
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
task_list.append( create_task_arg('nonres',       'bbyy') )
task_list.append( create_task_arg('nonres',       'bbbb') )
task_list.append( create_task_arg('nonres',       'bbtautau') )
task_list.append( create_task_arg('nonres',       'WWyy') )
task_list.append( create_task_arg('nonres',       'bbWW') )
#task_list.append( create_task_arg('spin0',        'bbbb') )
#task_list.append( create_task_arg('spin0',        'bbtautau') )
#task_list.append( create_task_arg('spin0',        'bbWW') )
#task_list.append( create_task_arg('spin0',        'WWyy') )
#task_list.append( create_task_arg('spin2_c_1.0',  'bbbb') )
#task_list.append( create_task_arg('spin2_c_1.0',  'bbtautau') )
#task_list.append( create_task_arg('spin2_c_1.0',  'bbWW') )
#task_list.append( create_task_arg('spin2_c_2.0',  'bbbb') )
#task_list.append( create_task_arg('spin2_c_2.0',  'bbWW') )

# - Create a job manager
nProc = 16
manager = utils.job_manager(func=wsc.task_pipeline_ws, nProc=nProc)

manager.set_task_args(task_list)
manager.submit()

git.save_hash_to_file(git_stamp_path)
~~~~


[conventions]: ./doc/conventions.md
