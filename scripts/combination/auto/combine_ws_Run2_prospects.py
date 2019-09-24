#!/usr/bin/env python

import workspaceCombiner as wsc
import aux_utils as utils
import correlation_scheme as cs
import LimitSetting as ls
import os

############################################
##### ----- Combination settings ----- #####
############################################

batch_tag = "Run2_prospects_batch"

# - Number of processes to run in parallel
nProc = 14

# - Input folder where the regularised and rescaled workspaces are found:
rescaled_ws_prepath = "/.data/englert/projects/hh_combination/workspaces/{0}/rescaled/".format(batch_tag)

# - Config folder where the the .xml config files are placed
config_file_prepath = "/.data/englert/projects/hh_combination/workspaces/{0}/cfg/combination/".format(batch_tag)

# - Output folder where the combined workspaces will be placed:
output_ws_prepath   = "/.data/englert/projects/hh_combination/workspaces/{0}/combined/".format(batch_tag)

# - Fit option
fit_option = -1

exp_or_obs     = "obs"
doBetterBands  = "false"   
dataName       = 'combData'
asimovDataName = ''
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


###################################
### --- Non-res combination --- ###
###################################

nonres_combination_list = { 
                             'A-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                          }

nonres_pts = [0]

combine_list(nonres_pts, nonres_combination_list, 'nonres',  "fullcorr")
combine_list(nonres_pts, nonres_combination_list, 'nonres',  "nocorr"  )

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
#manager = utils.job_manager(func=wsc.task_combine_and_calc_limit, nProc=nProc)
manager = utils.job_manager(func=wsc.task_combine_calc_limit_and_generate_asimov, nProc=nProc)

manager.set_task_args(task_list)
manager.submit()

    
for rootfiles_dir, scaling, datafile_path, isSM in datafile_arg_list:
    ls.get_limit_from_root_files(dir_path=rootfiles_dir,
                                     scaling=scaling,
                                     output_dat=datafile_path,
                                     isSM=isSM)
