#!/usr/bin/env python

import workspaceCombiner as wsc
import aux_utils as utils
import correlation_scheme as cs
import LimitSetting as ls
import os
import git
import sys

############################################
##### ----- Combination settings ----- #####
############################################

batch_tag = [s for s in sys.argv if 'batch_tag=' in s]
if batch_tag:
  batch_tag = batch_tag[0].split('=')[-1]
  batch_tag = "output/v140invfb_"+batch_tag
else:
  batch_tag = "output/v140invfb_20210309"
print(batch_tag)

# - Number of processes to run in parallel
nProc = 14

# - Input folder where the regularised and rescaled workspaces are found:
rescaled_ws_prepath = ('{0}/rescaled/' if len(sys.argv) > 1 and 'gitlabci' in sys.argv[1] else "../{0}/rescaled/").format(batch_tag)

# - Config folder where the the .xml config files are placed
config_file_prepath = ('{0}/cfg/combination/' if len(sys.argv) > 1 and 'gitlabci' in sys.argv[1] else "../{0}/cfg/combination/").format(batch_tag)

# - Output folder where the combined workspaces will be placed:
output_ws_prepath = ('{0}/combined/' if len(sys.argv) > 1 and 'gitlabci' in sys.argv[1] else "../{0}/combined/").format(batch_tag)

# - Git stamp path
git_stamp_path     = os.path.join(output_ws_prepath, "git.stamp")

# - Fit option
fit_option = -1

exp_or_obs     = "obs"
doBetterBands  = "true"   
dataName       = 'combData'
asimovDataName = 'asimovData_0'
CL             = 0.95

POI_name = 'xsec_br'

blind = True

# - List containing all pt_config`s
all_pt_configs = []

datafile_arg_list = []


prep_pts = wsc.prepare_pts_short(fit_option,
                                 exp_or_obs, 
                                 doBetterBands,    
                                 dataName,
                                 asimovDataName,
                                 CL,
                                 blind,
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
        if 'nonres' in type:
            isSM = True
        else:
            isSM = False

        datafile_arg_list.append( (rootfiles_dir, 'no', datafile_path, isSM)  )


###################################
### --- Non-res combination --- ###
###################################

nonres_combination_list = {
                            # 'A-bbyy'                : ['bbyy'],
                            # 'A-bbbb'                : ['bbbb'],
                            # 'A-bbtautau'                : ['bbtautau'],
                            # 'A-bbbb_bbtautau'                     : ['bbbb', 'bbtautau'],
                            # 'A-bbbb_bbyy'                         : ['bbbb', 'bbyy'],
                            # 'A-bbtautau_bbyy'                     : ['bbtautau', 'bbyy'],
                            # 'A-bbbb_bbtautau_bbyy'                : ['bbbb', 'bbtautau', 'bbyy'],
                            'A-bbbb_bbtautau_bbyy_WWWW'           : ['bbbb', 'bbtautau', 'bbyy', 'WWWW'],
                            #'A-bbbb_bbtautau_WWyy_bbWW'           : ['bbbb', 'bbtautau', 'WWyy', 'bbWW'],
                            #'A-bbbb_bbtautau_bbyy_WWyy_bbWW'      : ['bbbb', 'bbtautau', 'bbyy', 'WWyy', 'bbWW'],
                            # 'A-bbbb_bbtautau_bbyy_WWyy_bbWW_WWWW' : ['bbbb', 'bbtautau', 'bbyy', 'WWyy', 'bbWW', 'WWWW']
                          }
# Test 4b Lumi 15+16 correlation
nonres_combination_list_B = { 
                             'B-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],
                             'B-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'],
                            }
nonres_combination_list_C = { 
                             'C-bbtautau_bbyy'           : ['bbtautau', 'bbyy'],
                            }

nonrespt = [s for s in sys.argv if 'nonrespt=' in s]
if nonrespt: # split job behaviour
  nonres_pts = [nonrespt[0].split('=')[-1]]
  nonres_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy':'fullcorr' }
  combine_list(nonres_pts, nonres_combination_list, 'nonres',  nonres_scheme, 'fullcorr', same_scheme_for_all_channels=False)
elif len(sys.argv) < 2 or 'gitlabci' not in sys.argv[1]: # default behaviour
  nonres_pts = [0]


  # nonres_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy':'fullcorr', 'WWyy':'fullcorr', 'bbWW':'fullcorr', 'WWWW':'fullcorr' }
  # nonres_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy':'fullcorr' }
  #nonres_scheme = {'bbbb' : 'fullcorr_test', 'bbtautau' : 'fullcorr_test', 'bbyy':'fullcorr_test', 'WWyy':'fullcorr_test', 'bbWW':'fullcorr_test', 'WWWW':'fullcorr_test' }

  # combine_list(nonres_pts, nonres_combination_list, 'nonres',  nonres_scheme, 'fullcorr', same_scheme_for_all_channels=False)
  combine_list(nonres_pts, nonres_combination_list, 'nonres',  "nocorr"  )
  #combine_list(nonres_pts, nonres_combination_list_B, 'nonres',  nonres_scheme, 'fullcorr', same_scheme_for_all_channels=False)
  # combine_list(nonres_pts, nonres_combination_list, 'nonres',  "nocorr"  )

  #STAT-ONLY
  # combine_list(nonres_pts, nonres_combination_list, 'nonres_statOnly',  nonres_scheme, 'fullcorr', same_scheme_for_all_channels=False)
  # combine_list(nonres_pts, nonres_combination_list, 'nonres_statOnly',  "nocorr"  )

  #End of run 2 and 3 extrapolations
  #combine_list(nonres_pts, nonres_combination_list_C, 'nonres_140invfb',  nonres_scheme, 'fullcorr', same_scheme_for_all_channels=False)
  #combine_list(nonres_pts, nonres_combination_list_C, 'nonres_140invfb',  "nocorr"  )
  #combine_list(nonres_pts, nonres_combination_list_C, 'nonres_440invfb',  nonres_scheme, 'fullcorr', same_scheme_for_all_channels=False)
  #combine_list(nonres_pts, nonres_combination_list_C, 'nonres_440invfb',  "nocorr"  )


##################################
### --- Spin-0 combination --- ###
##################################

spin0_combination_list_AB = { 
                             'AB-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                             'AB-bbbb_bbtautau_WWyy' : ['bbbb', 'bbtautau', 'WWyy']
                            }

spin0_combination_list_A = {
                            # 'A-bbtautau'           : ['bbtautau'], #
                            # 'A-bbtautau'           : ['bbtautau'], #
                            # 'A-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],#
                            'A-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'], #
                            #'A-bbbb_bbtautau_bbyy_WWyy'      : ['bbbb', 'bbtautau', 'bbyy', 'WWyy'],
                            #'A-bbbb_bbtautau_bbyy_WWyy_WWWW' : ['bbbb', 'bbtautau', 'bbyy', 'WWyy', 'WWWW'],
                            # 'A-bbbb_bbyy'                    : ['bbbb', 'bbyy'],
                           }

spin0_combination_list_B = { 
                            'B-bbbb_bbtautau'                     : ['bbbb', 'bbtautau'],#
                            # 'B-bbbb_bbtautau_bbyy'                : ['bbbb', 'bbtautau', 'bbyy'],#
                            # 'B-bbbb_bbtautau_bbyy_WWyy'           : ['bbbb', 'bbtautau', 'bbyy', 'WWyy'],
                            # 'B-bbbb_bbtautau_bbyy_WWyy_bbWW'      : ['bbbb', 'bbtautau', 'bbyy', 'WWyy', 'bbWW'],
                            # 'B-bbbb_bbtautau_bbyy_WWyy_bbWW_WWWW' : ['bbbb', 'bbtautau', 'bbyy', 'WWyy', 'bbWW', 'WWWW'],
                           }

spin0_combination_list_C = { 
                            'C-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],#
                            'C-bbbb_bbtautau_bbyy'      : ['bbbb', 'bbtautau', 'bbyy'],#
                            'C-bbbb_bbtautau_bbyy_bbWW' : ['bbbb', 'bbtautau', 'bbyy', 'bbWW'],
                            ##'C-bbbb_bbWW'               : ['bbbb', 'bbWW'],
                           }

spin0_combination_list_D = { 
                            'D-bbbb_bbWW' : ['bbbb', 'bbWW']
                           }

spin0_combination_list_E = { 
                            'E-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],#
                            'E-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'],#
                            'E-bbbb_bbtautau_bbyy_WWyy'      : ['bbbb', 'bbtautau', 'bbyy', 'WWyy'],
                            'E-bbbb_bbtautau_bbyy_WWyy_WWWW' : ['bbbb', 'bbtautau', 'bbyy', 'WWyy', 'WWWW'],
                           }

spin0_combination_list_F = { 
                            'F-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],#
                            'F-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'],#
                            'F-bbbb_bbtautau_bbyy_bbWW'      : ['bbbb', 'bbtautau', 'bbyy', 'bbWW']
                           }

spin0_combination_list_G = { 
                            'G-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],
                            'G-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy']
                           }

spin0_combination_list_H = { 
                            'H-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],     # H6 is latest version for vfinal_04
                            #'H-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy'],
                           }
spin0_combination_list_I = { 
                            'I-bbbb_bbtautau'      : ['bbbb', 'bbtautau']
                           }
spin0_combination_list_J = { 
                            'J-bbbb_bbWW'      : ['bbbb', 'bbWW']
                           }
spin0_combination_list_K = { 
                            'K-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],
                            'K-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy']
                           }
spin0_combination_list_L = { 
                            #'L-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],#
                            #'L-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'],#
                            #'L-bbbb_bbtautau_bbyy_WWyy'      : ['bbbb', 'bbtautau', 'bbyy', 'WWyy'],
                            'L-bbbb_bbtautau_bbyy_WWyy_WWWW' : ['bbbb', 'bbtautau', 'bbyy', 'WWyy', 'WWWW'],
                           }

# for DPG plots
spin0_combination_list_Z = { 
                            'Z-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
#                            'Z-bbbb_bbtautau_bbWW' : ['bbbb', 'bbtautau', 'bbWW']
                           }


spin0_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy' : 'fullcorr', 'WWyy' : 'fullcorr', 'bbWW' : 'fullcorr', 'WWWW' : 'fullcorr'}

spin0pt = [s for s in sys.argv if 'spin0pt=' in s]
if spin0pt: # split job behaviour
  spin0pt = [spin0pt[0].split('=')[-1]]
  spin0_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy' : 'fullcorr', 'WWyy' : 'fullcorr', 'bbWW' : 'fullcorr', 'WWWW' : 'fullcorr'}
  combine_list(spin0pt, spin0_combination_list_A,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
elif len(sys.argv) < 2 or 'gitlabci' not in sys.argv[1]: # default behaviour
  spin0pt = [260, 300, 400, 500, 600, 700, 800, 900, 1000]
  # spin0_masses    = [260, 300, 400, 500, 600, 700, 800, 900, 1000]
  # #spin0_masses_A  = [260, 275, 300, 325, 350, 400, 450]#
  # #spin0_masses_A  = [260, 280, 300]
  # spin0_masses_A  = [300]
  # spin0_masses_AB = [260, 300, 400, 500]
  # spin0_masses_B  = [400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000]
  # spin0_masses_C  = [550, 600, 700, 800, 900, 1000]
  # #spin0_masses_C  = [1000]
  # spin0_masses_D  = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
  # spin0_masses_E  = [260, 275, 300, 325, 350, 400, 450, 500]
  # spin0_masses_F  = [500, 550, 600, 700, 800, 900, 1000]
  # spin0_masses_G  = [260, 275, 300, 325, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000]
  # spin0_masses_H  = [275, 325, 350, 450, 550]
  # spin0_masses_I  = [260, 1000]
  # spin0_masses_J  = [500, 1000, 2000]
  # spin0_masses_K  = [800]
  # spin0_masses_L  = [260, 275, 280, 300, 325, 350, 400, 450, 500] # for interpolation at 280 GeV to account for 4b excess
  #spin0_masses_L  = [280] # for interpolation at 280 GeV to account for 4b excess
  #spin0_masses_Z  = [500, 600, 700, 800, 900, 1000] #DPG plots


  #combine_list(spin0_masses_AB, spin0_combination_list_AB, 'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_AB, spin0_combination_list_AB, 'spin0', "nocorr")
  #
  # combine_list(spin0_masses_B, spin0_combination_list_B,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  # combine_list(spin0_masses_B, spin0_combination_list_B,   'spin0', "nocorr")
  #combine_list(spin0_masses_C, spin0_combination_list_C,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_C, spin0_combination_list_C,   'spin0', "nocorr")
  #combine_list(spin0_masses_D, spin0_combination_list_D,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_D, spin0_combination_list_D,   'spin0', "nocorr")
  #combine_list(spin0_masses_E, spin0_combination_list_E,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_E, spin0_combination_list_E,   'spin0', "nocorr")
  #combine_list(spin0_masses_F, spin0_combination_list_F,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_F, spin0_combination_list_F,   'spin0', "nocorr")
  #combine_list(spin0_masses_G, spin0_combination_list_G,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_G, spin0_combination_list_G,   'spin0', "nocorr")
  #combine_list(spin0_masses_H, spin0_combination_list_H,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_H, spin0_combination_list_H,   'spin0', "nocorr")
  #combine_list(spin0_masses_I, spin0_combination_list_I,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_I, spin0_combination_list_I,   'spin0', "nocorr")
  #combine_list(spin0_masses_K, spin0_combination_list_K,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_K, spin0_combination_list_K,   'spin0', "nocorr")

  #STAT-ONLY
  #combine_list(spin0_masses_D, spin0_combination_list_D,   'spin0_statOnly', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_D, spin0_combination_list_D,   'spin0_statOnly', "nocorr")
  #combine_list(spin0_masses_E, spin0_combination_list_E,   'spin0_statOnly', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_E, spin0_combination_list_E,   'spin0_statOnly', "nocorr")
  #combine_list(spin0_masses_F, spin0_combination_list_F,   'spin0_statOnly', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_F, spin0_combination_list_F,   'spin0_statOnly', "nocorr")
  #combine_list(spin0_masses_G, spin0_combination_list_G,   'spin0_statOnly', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_G, spin0_combination_list_G,   'spin0_statOnly', "nocorr")

  #interpolation in bbtautau from 275 and 300 GeV to account for excess in 4b at 280 GeV
  #combine_list(spin0_masses_L, spin0_combination_list_L,   'spin0_interp275', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_L, spin0_combination_list_L,   'spin0_interp275', "nocorr")
  #combine_list(spin0_masses_L, spin0_combination_list_L,   'spin0_interp300', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(spin0_masses_L, spin0_combination_list_L,   'spin0_interp300', "nocorr")



########################################
### --- Spin-2 c=1.0 combination --- ###
########################################

spin2_c_10_masses_A = [260, 300, 400]
spin2_c_10_masses_B = [500, 600, 700, 800, 900, 1000]
#spin2_c_10_masses_B = [500]
spin2_c_10_masses_C = [1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
spin2_c_10_masses_D = [260, 300, 400, 500]
spin2_c_10_masses_E = [500, 600, 700, 800, 900, 1000]
spin2_c_10_masses_F = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
spin2_c_10_masses_G = [260, 270, 280, 290, 300, 400]  #for bbtautau interpolation between 260 and 300 GeV
spin2_c_10_masses_H = [260, 270, 280, 290, 300, 400, 500]  #for bbtautau interpolation between 260 and 300 GeV

spin2_c_10_combination_list_A = { 
                                 'A-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                                }

spin2_c_10_combination_list_B = { 
                                 'B-bbbb_bbtautau'           : ['bbbb', 'bbtautau'], #
                                 'B-bbbb_bbtautau_bbWW'      : ['bbbb', 'bbtautau', 'bbWW'],
                                }

spin2_c_10_combination_list_C = { 
                                 'C-bbbb_bbWW'              : ['bbbb',  'bbWW']
                                }

spin2_c_10_combination_list_D = { 
                                 'D-bbbb_bbtautau'           : ['bbbb', 'bbtautau']
                                }

spin2_c_10_combination_list_E = { 
                                 'E-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                                 'E-bbbb_bbtautau_bbWW'      : ['bbbb', 'bbtautau', 'bbWW'],
                                }

spin2_c_10_combination_list_F = { 
                                 'F-bbbb_bbWW'      : ['bbbb', 'bbWW']
                                }

spin2_c10_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy' : 'fullcorr', 'WWyy' : 'fullcorr', 'bbWW' : 'fullcorr' }

#combine_list(spin2_c_10_masses_A, spin2_c_10_combination_list_A, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_A, spin2_c_10_combination_list_A, 'spin2_c_1.0', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_D, spin2_c_10_combination_list_D, 'spin2_c_1.0', "nocorr)
#combine_list(spin2_c_10_masses_D, spin2_c_10_combination_list_D, 'spin2_c_1.0', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_E, spin2_c_10_combination_list_E, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_E, spin2_c_10_combination_list_E, 'spin2_c_1.0', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_F, spin2_c_10_combination_list_F, 'spin2_c_1.0', "nocorr")
#combine_list(spin2_c_10_masses_F, spin2_c_10_combination_list_F, 'spin2_c_1.0', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)

#STAT-ONLY
#combine_list(spin2_c_10_masses_A, spin2_c_10_combination_list_A, 'spin2_c_1.0_statOnly', "nocorr")
#combine_list(spin2_c_10_masses_A, spin2_c_10_combination_list_A, 'spin2_c_1.0_statOnly', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0_statOnly', "nocorr")
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0_statOnly', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0_statOnly', "nocorr")
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0_statOnly', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_D, spin2_c_10_combination_list_D, 'spin2_c_1.0_statOnly', "nocorr)
#combine_list(spin2_c_10_masses_D, spin2_c_10_combination_list_D, 'spin2_c_1.0_statOnly', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_E, spin2_c_10_combination_list_E, 'spin2_c_1.0_statOnly', "nocorr")
#combine_list(spin2_c_10_masses_E, spin2_c_10_combination_list_E, 'spin2_c_1.0_statOnly', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_F, spin2_c_10_combination_list_F, 'spin2_c_1.0_statOnly', "nocorr")
#combine_list(spin2_c_10_masses_F, spin2_c_10_combination_list_F, 'spin2_c_1.0_statOnly', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)

#bbtautau interpolation from 260 and 300 GeV (change 3rd argument accordingly)
#combine_list(spin2_c_10_masses_G, spin2_c_10_combination_list_A, 'spin2_c_1.0_interp260', "nocorr")
#combine_list(spin2_c_10_masses_G, spin2_c_10_combination_list_A, 'spin2_c_1.0_interp260', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0_interp260', "nocorr")
#combine_list(spin2_c_10_masses_B, spin2_c_10_combination_list_B, 'spin2_c_1.0_interp260', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0_interp260', "nocorr")
#combine_list(spin2_c_10_masses_C, spin2_c_10_combination_list_C, 'spin2_c_1.0_interp260', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_H, spin2_c_10_combination_list_D, 'spin2_c_1.0_interp260', "nocorr)
#combine_list(spin2_c_10_masses_H, spin2_c_10_combination_list_D, 'spin2_c_1.0_interp260', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_E, spin2_c_10_combination_list_E, 'spin2_c_1.0_interp260', "nocorr")
#combine_list(spin2_c_10_masses_E, spin2_c_10_combination_list_E, 'spin2_c_1.0_interp260', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_10_masses_F, spin2_c_10_combination_list_F, 'spin2_c_1.0_interp260', "nocorr")
#combine_list(spin2_c_10_masses_F, spin2_c_10_combination_list_F, 'spin2_c_1.0_interp260', spin2_c10_scheme, "fullcorr", same_scheme_for_all_channels=False)


########################################
### --- Spin-2 c=2.0 combination --- ###
########################################

spin2_c_20_masses_A = [260, 300, 400, 500]
spin2_c_20_masses_B = [500, 600, 700, 800, 900, 1000]
spin2_c_20_masses_C = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 3000]

spin2_c_20_combination_list_A = { 
                                 'A-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                                }
spin2_c_20_combination_list_B = { 
                                 'B-bbbb_bbtautau'           : ['bbbb', 'bbtautau'],
                                 'B-bbbb_bbtautau_bbWW'      : ['bbbb', 'bbtautau', 'bbWW'],
                                }
spin2_c_20_combination_list_C = { 
                                 'C-bbbb_bbWW'               : ['bbbb', 'bbWW'],
                                }

spin2_c20_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy' : 'fullcorr', 'WWyy' : 'fullcorr', 'bbWW' : 'fullcorr' }

#combine_list(spin2_c_20_masses_A, spin2_c_20_combination_list_A, 'spin2_c_2.0', "nocorr")
#combine_list(spin2_c_20_masses_A, spin2_c_20_combination_list_A, 'spin2_c_2.0', spin2_c20_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_20_masses_B, spin2_c_20_combination_list_B, 'spin2_c_2.0', "nocorr")
#combine_list(spin2_c_20_masses_B, spin2_c_20_combination_list_B, 'spin2_c_2.0', spin2_c20_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_20_masses_C, spin2_c_20_combination_list_C, 'spin2_c_2.0', "nocorr")
#combine_list(spin2_c_20_masses_C, spin2_c_20_combination_list_C, 'spin2_c_2.0', spin2_c20_scheme, "fullcorr", same_scheme_for_all_channels=False)

#STAT-ONLY
#combine_list(spin2_c_20_masses_A, spin2_c_20_combination_list_A, 'spin2_c_2.0_statOnly', "nocorr")
#combine_list(spin2_c_20_masses_A, spin2_c_20_combination_list_A, 'spin2_c_2.0_statOnly', spin2_c20_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_20_masses_B, spin2_c_20_combination_list_B, 'spin2_c_2.0_statOnly', "nocorr")
#combine_list(spin2_c_20_masses_B, spin2_c_20_combination_list_B, 'spin2_c_2.0_statOnly', spin2_c20_scheme, "fullcorr", same_scheme_for_all_channels=False)
#combine_list(spin2_c_20_masses_C, spin2_c_20_combination_list_C, 'spin2_c_2.0_statOnly', "nocorr")
#combine_list(spin2_c_20_masses_C, spin2_c_20_combination_list_C, 'spin2_c_2.0_statOnly', spin2_c20_scheme, "fullcorr", same_scheme_for_all_channels=False)


##################################
### --- Lambda combination --- ###
##################################

### There is in principal no difference between regions A, B, C and D. Only the masses are split for performance reasons.

lambda_values_B = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1]
lambda_values_C = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lambda_values_D = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

lambda_combination_list_A = { 
                              'A-bbyy'      : ['bbyy'],
                              # 'A-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              # 'A-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy'],
                              ##'A-bbbb_bbyy'          : ['bbbb', 'bbyy'],
                              ##'A-bbtautau_bbyy'      : ['bbtautau', 'bbyy'],
                            }
lambda_combination_list_B = { 
                              'B-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'B-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy'],
                              ##'B-bbbb_bbyy'          : ['bbbb', 'bbyy'],
                              ##'B-bbtautau_bbyy'      : ['bbtautau', 'bbyy'],
                            }
lambda_combination_list_C = { 
                              'C-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'C-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy'],
                              ##'C-bbbb_bbyy'          : ['bbbb', 'bbyy'],
                              ##'C-bbtautau_bbyy'      : ['bbtautau', 'bbyy'],
                            }
lambda_combination_list_D = { 
                              'D-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'D-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy'],
                              ##'D-bbbb_bbyy'          : ['bbbb', 'bbyy'],
                              ##'D-bbtautau_bbyy'      : ['bbtautau', 'bbyy'],
                            }
lambda_combination_list_F = { 
                            #'F-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],#
                            'F-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'],#
                            #'F-bbbb_bbtautau_bbyy_bbWW'      : ['bbbb', 'bbtautau', 'bbyy', 'bbWW']
                           }
lambda_combination_list_G = { 
                              'G-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'G-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy']
                            }
lambda_combination_list_H = { 
                              'H-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'H-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy']
                            }
lambda_combination_list_I = { 
                              'I-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'I-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy']
                            }
lambda_combination_list_J = { 
                              'J-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'J-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy']
                            }
lambda_combination_list_K = { 
                              'K-bbtautau_bbyy' : ['bbtautau', 'bbyy']
                            }
lambda_combination_list_L = { 
                              'L-bbtautau_bbyy' : ['bbtautau', 'bbyy']
                            }
lambda_combination_list_M = { 
                              'M-bbtautau_bbyy' : ['bbtautau', 'bbyy']
                            }
lambda_combination_list_N = { 
                              'N-bbtautau_bbyy' : ['bbtautau', 'bbyy']
                            }


lambdapt = [s for s in sys.argv if 'lambdapt=' in s]
if lambdapt: # split job behaviour
  lambdapt = [lambdapt[0].split('=')[-1]]
  lambda_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy' : 'fullcorr', 'WWyy' : 'fullcorr', 'bbWW' : 'fullcorr' }
  combine_list(lambdapt, lambda_combination_list_A, 'lambda', "nocorr")
elif len(sys.argv) < 2 or 'gitlabci' not in sys.argv[1]: # default behaviour
  lambdapt = [10.0, 9.8, 9.6, 9.4, 9.2, 9.0, 8.8, 8.6, 8.4, 8.2, 8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8, 6.6, 6.4, 6.2, 6.0, 5.8, 5.6, 5.4, 5.2, 5.0, 4.8, 4.6, 4.4, 4.2, 4.0, 3.8, 3.6, 3.4, 3.2, 3.0, 2.8, 2.6, 2.4, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0, -0.2, -0.4, -0.6, -0.8, -1.0, -1.2, -1.4, -1.6, -1.8, -2.0, -2.2, -2.4, -2.6, -2.8, -3.0, -3.2, -3.4, -3.6, -3.8, -4.0, -4.2, -4.4, -4.6, -4.8, -5.0, -5.2, -5.4, -5.6, -5.8, -6.0, -6.2, -6.4, -6.6, -6.8, -7.0, -7.2, -7.4, -7.6, -7.8, -8.0, -8.2, -8.4, -8.6, -8.8, -9.0, -9.2, -9.4, -9.6, -9.8]
  # combine_list(lambdapt, lambda_combination_list_A, 'lambda', "nocorr")

  #combine_list(lambda_values_A, lambda_combination_list_A, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_B, lambda_combination_list_B, 'lambda', "nocorr")
  #combine_list(lambda_values_B, lambda_combination_list_B, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_C, lambda_combination_list_C, 'lambda', "nocorr")
  #combine_list(lambda_values_C, lambda_combination_list_C, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_D, lambda_combination_list_D, 'lambda', "nocorr")
  #combine_list(lambda_values_D, lambda_combination_list_D, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  # combine_list(lambda_values_A+lambda_values_B+lambda_values_C+lambda_values_D, lambda_combination_list_F, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)

  # old version before 
  #combine_list(lambda_values_A, lambda_combination_list_G, 'lambda', "nocorr")
  #combine_list(lambda_values_A, lambda_combination_list_G, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_B, lambda_combination_list_H, 'lambda', "nocorr")
  #combine_list(lambda_values_B, lambda_combination_list_H, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_C, lambda_combination_list_I, 'lambda', "nocorr")
  #combine_list(lambda_values_C, lambda_combination_list_I, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_D, lambda_combination_list_J, 'lambda', "nocorr")
  #combine_list(lambda_values_D, lambda_combination_list_J, 'lambda', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)

  # STAT-ONLY
  #combine_list(lambda_values_A, lambda_combination_list_A, 'lambda_statOnly', "nocorr")
  #combine_list(lambda_values_A, lambda_combination_list_A, 'lambda_statOnly', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_B, lambda_combination_list_B, 'lambda_statOnly', "nocorr")
  #combine_list(lambda_values_B, lambda_combination_list_B, 'lambda_statOnly', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_C, lambda_combination_list_C, 'lambda_statOnly', "nocorr")
  #combine_list(lambda_values_C, lambda_combination_list_C, 'lambda_statOnly', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_D, lambda_combination_list_D, 'lambda_statOnly', "nocorr")
  #combine_list(lambda_values_D, lambda_combination_list_D, 'lambda_statOnly', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  # combine_list(lambda_values_A+lambda_values_B+lambda_values_C+lambda_values_D, lambda_combination_list_F, 'lambda_statOnly', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)


  #End of run 2 and 3 extrapolations
  #combine_list(lambda_values_A, lambda_combination_list_K, 'lambda_140invfb', "nocorr")
  #combine_list(lambda_values_A, lambda_combination_list_K, 'lambda_140invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_B, lambda_combination_list_L, 'lambda_140invfb', "nocorr")
  #combine_list(lambda_values_B, lambda_combination_list_L, 'lambda_140invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_C, lambda_combination_list_M, 'lambda_140invfb', "nocorr")
  #combine_list(lambda_values_C, lambda_combination_list_M, 'lambda_140invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_D, lambda_combination_list_N, 'lambda_140invfb', "nocorr")
  #combine_list(lambda_values_D, lambda_combination_list_N, 'lambda_140invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)

  #combine_list(lambda_values_A, lambda_combination_list_K, 'lambda_440invfb', "nocorr")
  #combine_list(lambda_values_A, lambda_combination_list_K, 'lambda_440invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_B, lambda_combination_list_L, 'lambda_440invfb', "nocorr")
  #combine_list(lambda_values_B, lambda_combination_list_L, 'lambda_440invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_C, lambda_combination_list_M, 'lambda_440invfb', "nocorr")
  #combine_list(lambda_values_C, lambda_combination_list_M, 'lambda_440invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)
  #combine_list(lambda_values_D, lambda_combination_list_N, 'lambda_440invfb', "nocorr")
  #combine_list(lambda_values_D, lambda_combination_list_N, 'lambda_440invfb', lambda_scheme, "fullcorr", same_scheme_for_all_channels=False)



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

    ls.get_exp_and_obs_limit(rootfiles_dir, scaling=scaling, output_dat=datafile_path, isSM=isSM, blind=blind)   

git.save_hash_to_file(git_stamp_path)
