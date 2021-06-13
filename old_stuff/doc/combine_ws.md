# `combine_ws`

## Settings

**Variables you should modify or make sure they are the ones you actually want:**

- `batch_tag`: Name of the folder containing all the regularised, rescaled, combined workspaces,
    aka. a batch.
- `rescaled_ws_prepath`: pre-path to the rescaled workspaces
- `config_file_prepath`: pre-path to the worksapceCombiner `.xml` config files
- `output_ws_prepath`: output prepath
- `fit_option`: fit option, look at the `cmd_combination` function in
    [./submodules/RooStatTools/python_modules/workspaceCombiner.py](../submodules/RooStatTools/python_modules/workspaceCombiner.py)
- `nProc`: Number of processes you'd like to use in parallel.
- combination varations: `nonres_combination_list`, `spin0_combination_list_A`, ... 
- mass points: `spin0_masses`, `spin2_c_10_masses_A`, ...


**Auxiliary variables:**
- `exp_or_obs`: obsolete - both exp and observed limits are calculated
- `doBetterBands`: doBetterBands flag inside `runAsymptoticsCLs`
- `dataName`: name of the observed data within the workspace. Default: combData
- `asimovDataName`: name of the asimovData
- `CL`: confidence level
- `POI_name`: name of the POI


## How it works in a nutshell

The different combination variations specifying what to include in the combination is stored as a
dictionary, e.g.:

~~~~
spin0_combination_list_AB = { 
                             'AB-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                             'AB-bbbb_bbtautau_WWyy' : ['bbbb', 'bbtautau', 'WWyy']
                            }
~~~~
The above will create two different combinations one with two channels, (bbbb,bbtautau) and another
with three channels (bbbb,bbtautau,WWyy).

The mass points are stored in a list, e.g.:
~~~~
spin0_masses    = [260, 300, 400, 500, 600, 700, 800, 900, 1000]
~~~~

The `combine_list(masses, combination_list, type, scheme, extratag=False)` function appends the
combinations pts, to the complete set of pts, `all_pt_config`, and also appends to `datafile_arg_list`,
which extract the limits from the `.root` files and stores these in plain ASCII format (`.dat`).

The complete task list is created at the end: `task_list =
wsc.create_combination_task_list_from_pt_config_list(all_pt_configs, fit_option)`.
Finally the set of tasks is processed my the job manager, `manager`.

## Source code 

~~~~
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
batch_tag = "2017_12_18_without_bbyy"

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
#                            'A-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],
#                            'A-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'],
#                            'A-bbbb_bbtautau_bbyy_WWyy'      : ['bbbb', 'bbtautau', 'bbyy', 'WWyy'],
                             'A-bbbb_bbtautau_WWyy_bbWW' : ['bbbb', 'bbtautau', 'WWyy', 'bbWW']
                          }

nonres_pts = [0]

combine_list(nonres_pts, nonres_combination_list, 'nonres',  "fullcorr")
combine_list(nonres_pts, nonres_combination_list, 'nonres',  "nocorr"  )

##################################
### --- Spin-0 combination --- ###
##################################

spin0_combination_list_AB = { 
                             'AB-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                             'AB-bbbb_bbtautau_WWyy' : ['bbbb', 'bbtautau', 'WWyy']
                            }

spin0_combination_list_A = { 
                           'A-bbbb_WWyy'          : ['bbbb', 'WWyy'],
                           'A-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                           'A-bbbb_bbtautau_WWyy' : ['bbbb', 'bbtautau', 'WWyy']
                           }

spin0_combination_list_B = { 
                            'B-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                            'B-bbbb_bbtautau_WWyy'      : ['bbbb', 'bbtautau', 'WWyy'],
                            'B-bbbb_bbtautau_WWyy_bbWW' : ['bbbb', 'bbtautau', 'WWyy', 'bbWW']
                           }

spin0_combination_list_C = { 
                            'C-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                            'C-bbbb_bbtautau_bbWW' : ['bbbb', 'bbtautau', 'bbWW']
                           }


spin0_masses    = [260, 300, 400, 500, 600, 700, 800, 900, 1000]
spin0_masses_A  = [260, 300, 400]
#spin0_masses_A  = [300]
spin0_masses_AB = [260, 300, 400, 500]
spin0_masses_B  = [500]
spin0_masses_C  = [600, 700, 800, 900, 1000]



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
### --- Spin-0 c=1.0 combination --- ###
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
########################################

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
~~~~
