#!/usr/bin/env python

import workspaceCombiner as wsc
import aux_utils as utils
import correlation_scheme as cs
import LimitSetting as ls
import os
import git

############################################
##### ----- Combination settings ----- #####
############################################

#batch_tag = "Debugging_fit_option_-1"
#batch_tag = "2017_11_27"
#batch_tag = "2017_12_18_without_bbyy"
#batch_tag = "2018_06_11"
#batch_tag = "2018_06_28_sign_off"
#batch_tag = "2018_08_15"
batch_tag = "2018_08_27_bbbb_modified"


# - Number of processes to run in parallel
nProc = 14

# - Input folder where the regularised and rescaled workspaces are found:
rescaled_ws_prepath = "/.data/englert/projects/hh_combination/workspaces/{0}/rescaled/".format(batch_tag)

# - Config folder where the the .xml config files are placed
config_file_prepath = "/.data/englert/projects/hh_combination/workspaces/{0}/cfg/combination/".format(batch_tag)

# - Output folder where the combined workspaces will be placed:
output_ws_prepath = "/.data/englert/projects/hh_combination/workspaces/{0}/combined/".format(batch_tag)

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


def combine_list(masses, combination_list, type, scheme, scheme_tag=None, same_scheme_for_all_channels=True, extratag=False):
    global all_pt_configs
    global datafile_arg_list

    for comb, channels in combination_list.items():

        if same_scheme_for_all_channels:
            scheme_dict = cs.get_same_scheme_for_all_channels(channels, scheme=scheme)
            scheme_tag = scheme
        else:
            scheme_dict = {}
            for channel in channels:
                scheme_dict[channel] = scheme[channel]

        if extratag:
            tag_pattern = "{}-{}-{}"
            tag = tag_pattern.format(comb, scheme_tag, extratag)
        else:
            tag_pattern = "{}-{}"
            tag = tag_pattern.format(comb, scheme_tag)

        pts = prep_pts(masses, type, tag, scheme_dict)
        print(scheme_dict)

        all_pt_configs += pts

        rootfiles_dir = os.path.join(output_ws_prepath, '../limits/root-files/',  type, 'combined', tag)

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
                             'A-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],
                             'A-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'],
#                            'A-bbbb_bbtautau_bbyy_WWyy'      : ['bbbb', 'bbtautau', 'bbyy', 'WWyy'],
#                            'A-bbbb_bbtautau_WWyy_bbWW' : ['bbbb', 'bbtautau', 'WWyy', 'bbWW']
                          }

nonres_pts = [0]

nonres_scheme_bbbb_bbtautau      = {'bbbb' : 'fullcorr_nonres', 'bbtautau' : 'fullcorr' }
nonres_scheme_bbbb_bbtautau_bbyy = {'bbbb' : 'fullcorr_nonres', 'bbtautau' : 'fullcorr', 'bbyy':'fullcorr' }

combine_list(nonres_pts, nonres_combination_list, 'nonres',  nonres_scheme_bbbb_bbtautau_bbyy, 'fullcorr',
        same_scheme_for_all_channels=False)
#combine_list(nonres_pts, nonres_combination_list, 'nonres',  "nocorr"  )

##################################
### --- Spin-0 combination --- ###
##################################

spin0_combination_list_AB = { 
                             'AB-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
#                            'AB-bbbb_bbtautau_WWyy' : ['bbbb', 'bbtautau', 'WWyy']
                            }

spin0_combination_list_A = { 
#                          'A-bbbb_WWyy'          : ['bbbb', 'WWyy'],
                           'A-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                           'A-bbbb_bbtautau_bbyy'      : ['bbbb', 'bbtautau', 'bbyy'],
#                          'A-bbbb_bbtautau_WWyy' : ['bbbb', 'bbtautau', 'WWyy']
                           }

spin0_combination_list_B = { 
                            'B-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
#                           'B-bbbb_bbtautau_WWyy'      : ['bbbb', 'bbtautau', 'WWyy'],
#                           'B-bbbb_bbtautau_WWyy_bbWW' : ['bbbb', 'bbtautau', 'WWyy', 'bbWW']
                           }

spin0_combination_list_C = { 
                            'C-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
#                           'C-bbbb_bbtautau_bbWW' : ['bbbb', 'bbtautau', 'bbWW']
                           }

spin0_combination_list = { 
                            'A-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                            'A-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy']
                           }

spin0_masses    = [260, 300, 400, 500, 600, 700, 800, 900, 1000]
#spin0_masses    = [260, 300, 400, 500, 600, 700, 800, 900, 1000]
spin0_masses_A  = [260, 300, 400]
#spin0_masses_A  = [300]
spin0_masses_AB = [260, 300, 400, 500]
spin0_masses_B  = [500]
spin0_masses_C  = [600, 700, 800, 900, 1000]



#combine_list(spin0_masses, spin0_combination_list, 'spin0',  "fullcorr")
#combine_list(spin0_masses, spin0_combination_list, 'spin0',  "nocorr")

#combine_list(spin0_masses_A, spin0_combination_list_A,   'spin0',  "fullcorr")
#combine_list(spin0_masses_A, spin0_combination_list_A,   'spin0',  "nocorr"  )
#
#combine_list(spin0_masses_AB, spin0_combination_list_AB, 'spin0',  "fullcorr")
#combine_list(spin0_masses_AB, spin0_combination_list_AB, 'spin0',  "nocorr"  )
#
#combine_list(spin0_masses_B, spin0_combination_list_B,   'spin0',  "fullcorr")
#combine_list(spin0_masses_B, spin0_combination_list_B,   'spin0',  "nocorr"  )
#combine_list(spin0_masses_C, spin0_combination_list_C,   'spin0',  "fullcorr")
#combine_list(spin0_masses_C, spin0_combination_list_C,   'spin0',  "nocorr"  )

########################################
### --- Spin-2 c=1.0 combination --- ###
########################################

spin2_c_10_masses_A = [260, 300, 400]
spin2_c_10_masses_B = [500, 600, 700, 800, 900, 1000]
spin2_c_10_masses_C = [1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 3000]

spin2_c_10_combination_list_A = { 
                                 'A-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                                }

spin2_c_10_combination_list_B = { 
                                 'B-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                                 'B-bbbb_bbtautau_bbWW'      : ['bbbb', 'bbtautau', 'bbWW'],
                                }

spin2_c_10_combination_list_C = { 
                                 'C-bbbb_bbWW'              : ['bbbb',  'bbWW'],
                                }


#combine_list(spin2_c_10_masses_A, spin2_c_10_combination_list_A, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_A, spin2_c_10_combination_list_A, 'spin2_c_1.0', "fullcorr")
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0', "fullcorr")
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0', "fullcorr")


########################################
### --- Spin-0 c=2.0 combination --- ###
#############2##########################

spin2_c_20_masses = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 3000]

spin2_c_20_combination_list = { 
                                'A-bbbb_bbWW'      : ['bbbb', 'bbWW'],
                               }

#combine_list(spin2_c_20_masses, spin2_c_20_combination_list, 'spin2_c_2.0', "nocorr")
#combine_list(spin2_c_20_masses, spin2_c_20_combination_list, 'spin2_c_2.0', "fullcorr")


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

    ls.get_exp_and_obs_limit(rootfiles_dir, scaling=scaling, output_dat=datafile_path, isSM=isSM)   

git.save_hash_to_file(git_stamp_path)
