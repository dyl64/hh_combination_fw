#!/usr/bin/env python

import os
import shutil
import glob
import re



def extract_parameter_from_path_bbbb(path):

    basename = os.path.basename(path)
    basename_splitted = basename.split('_')
    value = basename_splitted[4][1:]
    msg = "par value {0} extracted from {1}".format(value, path)
    #print(msg)
    return value


def extract_parameter_from_path_bbbb_lambda(path):

    basename = os.path.basename(path)
    basename_splitted = basename.split('_')
    print(basename_splitted[2])
    value = basename_splitted[2][3:]
    value = int(value)
    msg = "par value {0} extracted from {1}".format(value, path)
    #print(msg)
    return value


def extract_parameter_from_path_bbtautau(path):

    basename = os.path.basename(path)
    basename_splitted = basename.split('_')
    value = basename_splitted[8]
    msg = "par value {0} extracted from {1}".format(value, path)
    #print(msg)
    return value


def extract_parameter_from_path_bbtautau_lambda(path):

    basename = os.path.basename(path)
    basename_splitted = basename.split('_')
    string = basename_splitted[9]
    if 'm' in string:
        sign = -1
        string = string.replace('m', '')
    else:
        sign = 1
    value = sign*int(string[3:5])
    msg = "par value {0} extracted from {1}".format(value, path)
    #print(msg)
    return value


def extract_parameter_from_path_WWyy(path):

    basename = os.path.basename(path)
    basename_splitted = basename.split('.')
    filename = basename_splitted[0]
    mX_index = filename.find('mX')
    value = filename[mX_index+2:]

    msg = "par value {0} extracted from {1}".format(value, path)
    print(msg)
    return value



def extract_parameter_from_root_filename(path):

    basename = os.path.basename(path)
    basename_splitted = basename.split('.')
    value = basename_splitted[0]
    msg = "par value {0} extracted from {1}".format(value, path)
    print(msg)
    return value


def standardise_workspaces(input_dir, token, output_prepath, parameter_value_extractor_function, subdir=None):
    
    path_token = os.path.join(input_dir, token)
    hits = glob.glob(path_token)


    # - Extract parameter value (mass, kappa_lambda, etc.)
    for hit in hits:

        if subdir is None:
            par_value  = parameter_value_extractor_function(hit)
            original_file = hit
        else:
            par_value  = parameter_value_extractor_function(hit)
            subdir_path = os.path.join(hit, subdir)
            root_files_token = os.path.join(subdir_path, '*.root')
            root_files_in_subdir = glob.glob(root_files_token)
            original_file = root_files_in_subdir[0]


        output_filename = "{0}.root".format(par_value)
        output_path = os.path.join(output_prepath, output_filename)
        msg = "Copying {0} to {1}".format(original_file, output_path)
        print(msg)
        
        shutil.copy2(original_file, output_path)

########################################################################################################


####################
### --- bbbb --- ###
####################


bbbb_path = '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbbb/'


# - Non-res
#shutil.copy2('/.data/englert/projects/hh_combination/workspaces/eos_mirror_most_up_to_date_unsorted/bbbb/smrwMhh_hh_resolved_4b_AllSyst_combined_hh4b_model.root',
#               '/.data/englert/projects/hh_combination/workspaces/current/bbbb/nonres/0.root')
    
# - Varied lambda
standardise_workspaces(bbbb_path+"lambda_140invfb_original/",
                       'sm_hh_lhh*',
                       '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbbb/lambda_140invfb',
                       extract_parameter_from_path_bbbb_lambda)


# - Spin 0
#standardise_workspaces(bbbb_path,
#                       's_hh*',
#                       '/.data/englert/projects/hh_combination/workspaces/current/bbbb/spin0',
#                       extract_parameter_from_path_bbbb)

# - Spin 2, c=1
#standardise_workspaces(bbbb_path,
#                       'g10_hh*',
#                       '/.data/englert/projects/hh_combination/workspaces/current/bbbb/spin2_c_1.0/',
#                       extract_parameter_from_path_bbbb)

# - Spin 2, c=1
#standardise_workspaces(bbbb_path,
#                       'g20_hh*',
#                       '/.data/englert/projects/hh_combination/workspaces/current/bbbb/spin2_c_2.0/',
#                       extract_parameter_from_path_bbbb)

########################
### --- bbtautau --- ###
########################

bbtatau_path = '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbtautau/lambda_300invfb_statOnly_original'


# - Non-res
#shutil.copy2('/.data/englert/projects/hh_combination/workspaces/eos_mirror_most_up_to_date_unsorted/bbtautau/HHCombo080318.080318HH_HH_13TeV_080318HH_Systs_tautau_SMRW_BDT_0/combined/0.root',
#            '/.data/englert/projects/hh_combination/workspaces/current/bbtautau/nonres/0.root')

# - Varied lambda
#standardise_workspaces(bbtatau_path,
#                       '*VariedLambda*',
#                       '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbtautau/lambda_300invfb_statOnly',
#                       extract_parameter_from_path_bbtautau_lambda,
#                       subdir='combined')


# - Spin 0
#standardise_workspaces(bbtatau_path,
#                       '*2HDM_BDT*',
#                       '/.data/englert/projects/hh_combination/workspaces/current/bbtautau/spin0/',
#                       extract_parameter_from_path_bbtautau,
#                       subdir='combined')


# - Spin 2, c=1
#standardise_workspaces(bbtatau_path,
#                       '*RSGc1*',
#                       '/.data/englert/projects/hh_combination/workspaces/current/bbtautau/spin2_c_1.0/',
#                       extract_paramete_from_path_bbtautau,
#                       subdir='combined')

# - Spin 2, c=2
#standardise_workspaces(bbtatau_path,
#                          '*RSGc2*',
#                          '/.data/englert/projects/hh_combination/workspaces/current/bbtautau/spin2_c_2.0/',
#                          extract_parameter_from_path_bbtautau,
#                          subdir='combined')


####################
### --- bbyy --- ###
####################

bbyy_path = '/.data/englert/projects/hh_combination/workspaces/eos_mirror_most_up_to_date_unsorted/bbyy'


# - Non-res
#shutil.copy2('/.data/englert/projects/hh_combination/workspaces/eos_mirror_most_up_to_date_unsorted/bbyy/1265_ggbb_nonres_unblinded_tH.root',
#            '/.data/englert/projects/hh_combination/workspaces/current/bbyy/nonres/0.root')

# - Spin-0
#standardise_workspaces(bbyy_path,
#                          '*.root',
#                          '/.data/englert/projects/hh_combination/workspaces/current/bbyy/spin0/',
#                          extract_parameter_from_root_filename)

####################
### --- bbWW --- ###
####################


bbWW_path = '/.data/englert/projects/hh_combination/workspaces/eos_mirror_most_up_to_date_unsorted/bbWW/resolved/spin0/'

#standardise_workspaces(bbWW_path,
#                          '*.root',
#                          '/.data/englert/projects/hh_combination/workspaces/current/bbWW/spin0/',
#                          extract_parameter_from_root_filename)

####################################################################################################################

#extract_parameter_from_path_bbbb('/.data/englert/projects/hh_combination/workspaces/eos_mirror_most_up_to_date_unsorted/bbbb/g10_hh_combined_AllSyst_M1000_combined_hh4b_model.root')
#
#extract_parameter_from_path_WWyy('/.data/englert/projects/hh_combination/workspaces/eos_mirror_most_up_to_date_unsorted/WWyy/WSOneLepmX260.root')

#print('test'.index('est'))


#dir = './'
#
####
#
#os.chdir(dir)
#files = glob.glob('*s_hh*')
#
#for f in files:
#
#    splitted_filename = f.split('_')
#    m = re.findall(r'\d+' ,splitted_filename[4][1:])
#    m = m[0]
#
#    # - Format might behave in an unexpected way in python 2.*
#    out_file_name = "{0}.root".format( m )
#    print(out_file_name)
#    shutil.move(f , out_file_name)

#for f in glob.glob('*Hhhbbtautau*'):
#
#    mH = re.findall(r'\d+' , f)
#
#    out_file_name = 'Hhhbbtautau{}.root'.format(mH[0])
#    shutil.move(f , out_file_name)
