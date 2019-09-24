#!/usr/bin/env python

import workspaceCombiner as wsc
import aux_utils as utils
import correlation_scheme as cs
import LimitSetting as ls
import os
import git

hh_combination_fw_path = os.environ['hh_combination_fw_path']

############################################
##### ----- Combination settings ----- #####
############################################

batch_tag = "2017_12_18_without_bbyy"

# - Number of processes to run in parallel
nProc = 14

# - Input folder where the regularised and rescaled workspaces are found:
rescaled_ws_prepath = os.path.join(hh_combination_fw_path, './tests/test_pipeline/test_batch/rescaled/')

# - Config folder where the the .xml config files are placed
config_file_prepath = os.path.join(hh_combination_fw_path, "./tests/test_pipeline/test_batch/cfg/combination/")

# - Output folder where the combined workspaces will be placed:
output_ws_prepath = os.path.join(hh_combination_fw_path, "./tests/test_combination/test_combined/")

# - Git stamp path
git_stamp_path     = os.path.join(output_ws_prepath, "git.stamp")

# - Fit option
fit_option = -1

exp_or_obs     = "exp"
doBetterBands  = "false"   
dataName       = 'combData'
asimovDataName = 'asimovData_0'
CL             = 0.95

POI_name = 'xsec_br'

# - List containing all pt_config`s
all_pt_configs = []

datafile_arg_list = []


prep_pts = wsc.prepare_pts_short(fit_option,
                                 exp_or_obs, 
                                 doBetterBands,    
                                 dataName,
                                 asimovDataName,
                                 CL,
                                 POI_name,
                                 rescaled_ws_prepath,
                                 config_file_prepath,
                                 output_ws_prepath)


def combine_list(masses, combination_list, type, scheme, extratag=False):
    global all_pt_configs
    global datafile_arg_list

    for comb, channels in combination_list.items():
        if extratag:
            tag_pattern = "{}-{}-{}"
            tag = tag_pattern.format(comb, scheme, extratag)
        else:
            tag_pattern = "{}-{}"
            tag = tag_pattern.format(comb, scheme)
        pts = prep_pts(masses, type, tag, cs.get_same_scheme_for_all_channels(channels, scheme=scheme))
        all_pt_configs += pts

        rootfiles_dir = os.path.join(output_ws_prepath, '../limits/root-files/',  type, 'combined', tag)
        print(rootfiles_dir)
        datafile_name = "{0}-combined-{1}.dat".format(type, tag)
        datafile_path = os.path.join(output_ws_prepath, '../limits/data-files/', datafile_name)
        if type == 'nonres':
            isSM = True
        else:
            isSM = False

        datafile_arg_list.append( (rootfiles_dir, 'no', datafile_path, isSM)  )

##################################
### --- Spin-0 combination --- ###
##################################

spin0_combination_list = { 
                             'bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                            }

spin0_masses    = [500, 600]
combine_list(spin0_masses, spin0_combination_list, 'spin0',  "fullcorr")

#############################
### ----- Task list ----- ###
#############################

task_list = wsc.create_combination_task_list_from_pt_config_list(all_pt_configs, fit_option)

##############################
### -----  Execution ----- ###
##############################

print("##########################")
utils.prog_info()
print("##########################")

# - Create a job manager
manager = utils.job_manager(func=wsc.task_combine_calc_limit_and_generate_asimov, nProc=nProc)

manager.set_task_args(task_list)
manager.submit()

for rootfiles_dir, scaling, datafile_path, isSM in datafile_arg_list:

    ls.get_exp_and_obs_limit(rootfiles_dir, scaling=scaling, output_dat=datafile_path, isSM=isSM)   

git.save_hash_to_file(git_stamp_path)
