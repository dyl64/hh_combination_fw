import sys
import os
import re
import git
import click

import workspaceCombiner as wsc
import aux_utils as utils
import correlation_scheme as cs
import LimitSetting as ls


###################################
### --- Non-res combination --- ###
###################################

nonres_combination_list = {
                            # 'A-bbtautau'                : ['bbtautau'],
                            # 'A-bbbb_bbtautau'                     : ['bbbb', 'bbtautau'],
                            # 'A-bbbb_bbyy'                         : ['bbbb', 'bbyy'],
                            # 'A-bbtautau_bbyy'                     : ['bbtautau', 'bbyy'],
                            'A-bbbb_bbtautau_bbyy'                : ['bbbb', 'bbtautau', 'bbyy'],
                            #'A-bbbb_bbtautau_bbyy_WWyy'           : ['bbbb', 'bbtautau', 'bbyy', 'WWyy'],
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

nonres_pts = [0]

# nonres_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy':'fullcorr', 'WWyy':'fullcorr', 'bbWW':'fullcorr', 'WWWW':'fullcorr' }
nonres_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy':'fullcorr' }
#nonres_scheme = {'bbbb' : 'fullcorr_test', 'bbtautau' : 'fullcorr_test', 'bbyy':'fullcorr_test', 'WWyy':'fullcorr_test', 'bbWW':'fullcorr_test', 'WWWW':'fullcorr_test' }

# combine_list(nonres_pts, nonres_combination_list, 'nonres',  nonres_scheme, 'fullcorr', same_scheme_for_all_channels=False)
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
                            'A-bbbb_bbtautau'                : ['bbbb', 'bbtautau'],#
                            # 'A-bbbb_bbtautau_bbyy'           : ['bbbb', 'bbtautau', 'bbyy'], #
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

spin0_masses    = [260, 300, 400, 500, 600, 700, 800, 900, 1000]
#spin0_masses_A  = [260, 275, 300, 325, 350, 400, 450]#
#spin0_masses_A  = [260, 280, 300]
spin0_masses_A  = [300]
spin0_masses_AB = [260, 300, 400, 500]
spin0_masses_B  = [400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000]
spin0_masses_C  = [550, 600, 700, 800, 900, 1000]
#spin0_masses_C  = [1000]
spin0_masses_D  = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000]
spin0_masses_E  = [260, 275, 300, 325, 350, 400, 450, 500]
spin0_masses_F  = [500, 550, 600, 700, 800, 900, 1000]
spin0_masses_G  = [260, 275, 300, 325, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000]
spin0_masses_H  = [275, 325, 350, 450, 550]
spin0_masses_I  = [260, 1000]
spin0_masses_J  = [500, 1000, 2000]
spin0_masses_K  = [800]
spin0_masses_L  = [260, 275, 280, 300, 325, 350, 400, 450, 500] # for interpolation at 280 GeV to account for 4b excess
#spin0_masses_L  = [280] # for interpolation at 280 GeV to account for 4b excess

#spin0_masses_Z  = [500, 600, 700, 800, 900, 1000] #DPG plots


# combine_list(spin0_masses_A, spin0_combination_list_A,   'spin0', spin0_scheme,  "fullcorr", same_scheme_for_all_channels=False)
# combine_list(spin0_masses_A, spin0_combination_list_A,   'spin0', "nocorr")
#
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

lambda_values_A = [-20, -19, -18, -17, -16, -15, -14, -13, -12, -11]
lambda_values_B = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1]
lambda_values_C = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lambda_values_D = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

lambda_combination_list_A = { 
                              'A-bbbb_bbtautau'      : ['bbbb', 'bbtautau'],
                              'A-bbbb_bbtautau_bbyy' : ['bbbb', 'bbtautau', 'bbyy'],
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

lambda_scheme = {'bbbb' : 'fullcorr_allinone', 'bbtautau' : 'fullcorr', 'bbyy' : 'fullcorr', 'WWyy' : 'fullcorr', 'bbWW' : 'fullcorr' }

#combine_list(lambda_values_A, lambda_combination_list_A, 'lambda', "nocorr")
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
def mass_point_exists(mass, channel, input_path, resonant_type):
    path = os.path.join(input_path, 'rescaled', resonant_type, channel, '{}_with_Asimov_POI_0_NP_nom.root'.format(mass))
    return os.path.exists(path)

def combine_list(masses, combination_list, resonant_type, scheme, pts_func, input_path,
                 scheme_tag=None, same_scheme_for_all_channels=True, extratag=False):
    pt_configs = []
    datafile_args = []

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
        for mass in masses:
            valid_channels = [c for c in channels if mass_point_exists(mass, c, input_path, resonant_type)]
            valid_scheme_dict = {k:v for k,v in scheme_dict.items() if k in valid_channels}
            pt = pts_func([mass], resonant_type, tag, valid_scheme_dict)
            pt_configs += pt
        rootfiles_dir = os.path.join(input_path, 'limits', 'root-files',  resonant_type, 'combined', tag)

        datafile_name = "{0}-combined-{1}.dat".format(resonant_type, tag)
        datafile_path = os.path.join(input_path, 'limits', 'data-files', datafile_name)
        if 'nonres' in resonant_type:
            isSM = True
        else:
            isSM = False

        datafile_args.append( (rootfiles_dir, 'no', datafile_path, isSM) )
        
    return pt_configs, datafile_args


@click.command(name='combine_ws')
@click.option('-i', '--input_path', required=True, help='path to the processed workspaces')
@click.option('-p', '--poi', default='xsec_br', help='new poi name')
@click.option('-r', '--resonant_type', default='nonres', help='resonant or non-resonant analysis')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', help='channels combine')
@click.option('-m', '--mass_points', default='0', help='mass points to combine')
@click.option('-f', '--fit_option', type=int, default=-1, help='fit option')
@click.option('-x', '--prefix', default='A', help='output directory prefix')
@click.option('--exp_or_obs', default='obs')
@click.option('--do_better_bands', default="true")
@click.option('--data_name', default="combData", help='dataset name in workspace')
@click.option('--asimov_data_name', default="asimovData_0", help='asimov dataset name in workspace')
@click.option('--cl', default="0.95", help='confidence level')
@click.option('--blind/--unblind', default=True, help='blind analysis')
@click.option('-n', 'n_proc', type=int, default=16, help='number of concurrent processes')
def combine_ws(input_path, poi, resonant_type, channels, mass_points, prefix,
               fit_option, exp_or_obs, do_better_bands, data_name, 
               asimov_data_name, cl, blind, n_proc):
    rescaled_ws_path = os.path.join(input_path, 'rescaled')
    config_file_path = os.path.join(input_path, 'cfg', 'combination')
    output_ws_path   = os.path.join(input_path, 'combined')
    git_stamp_path   = os.path.join(output_ws_path, 'git.stamp')
    
    # - List containing all pt_config`s
    all_pt_configs = []
    datafile_arg_list = []

    prep_pts = wsc.prepare_pts_short(fit_option,
                                     exp_or_obs, 
                                     do_better_bands,    
                                     data_name,
                                     asimov_data_name,
                                     cl,
                                     blind,
                                     poi,
                                     rescaled_ws_path,
                                     config_file_path,
                                     output_ws_path)
    combine_pts = [int(i.strip()) for i in mass_points.split(',')]
    combination_list = {}
    combination_list['{}-{}'.format(prefix, '_'.join(channels.split(',')))] = channels.split(',')
    pt_configs, datafile_args = combine_list(combine_pts, combination_list, 
                                             resonant_type,  "nocorr", prep_pts, input_path)
    
    #############################
    ### ----- Task list ----- ###
    #############################

    task_list = wsc.create_combination_task_list_from_pt_config_list(pt_configs, fit_option)

    ##############################
    ### -----  Execution ----- ###
    ##############################

    print("##########################")
    utils.prog_info()
    print("##########################")

    # - Create a job manager
    #manager = utils.job_manager(func=wsc.task_combine_and_calc_limit, nProc=nProc)
    manager = utils.job_manager(func=wsc.task_combine_calc_limit_and_generate_asimov, nProc=n_proc)

    manager.set_task_args(task_list)
    manager.submit()

    
    for rootfiles_dir, scaling, datafile_path, isSM in datafile_args:

        ls.get_exp_and_obs_limit(rootfiles_dir, scaling=scaling, output_dat=datafile_path, isSM=isSM, blind=blind)   

    git.save_hash_to_file(git_stamp_path)

    







