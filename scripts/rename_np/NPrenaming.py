#!/usr/bin/env python
# Rui Zhang 4.2021
# rui.zhang@cern.ch

import os
import ROOT
import difflib
from argparse import ArgumentParser
from datetime import datetime
from os import makedirs, path, remove
import sys

'''
    This is a script to list the Nuisance Parameters names in a workspace and perform a smart guess on the meaning of it by mapping to the standard naming.
    Documents (by descending importance):
    - https://social.cern.ch/me/xiaohu/_layouts/15/WopiFrame.aspx?sourcedoc=/me/xiaohu/Documents/HH_FullRun2/NP_name_experimental.xlsx&action=default
    - https://indico.cern.ch/event/900373/contributions/3794076/attachments/2009448/3356947/HH-XiaohuSUN-2020-03-26-HHNP.pdf
    - https://indico.cern.ch/event/830934/contributions/3483158/attachments/1874779/3086593/HHComb-XiaohuSUN-2019-07-04-Systematics-1.pdf
'''

def get_nuisance_parameter_names(fname:str, ws_name:str, model_config_name:str, syst:bool = False):
    if not os.path.exists(fname):
        raise FileNotFoundError('workspace file {} does not exist'.format(fname))
    file = ROOT.TFile(fname)
    if (not file):
        raise RuntimeError("Something went wrong while loading the root file: {}".format(fname))
    ws = file.Get(ws_name)
    if not ws:
        raise RuntimeError("Something went wrong while loading the workspace: '{}', found {}".format(ws_name, [k.GetName() for k in file.GetListOfKeys() if k.GetClassName() == 'RooWorkspace']))
    model_config = ws.obj(model_config_name)
    if not model_config:
        raise RuntimeError('ERROR: Failed to load model config {}'.format(model_config_name))
    nuisance_parameters = model_config.GetNuisanceParameters()
    if not nuisance_parameters:
        raise RuntimeError('ERROR: No nuisance parameters found')
    return [nuis.GetName() for nuis in nuisance_parameters if not nuis.GetName().startswith('gamma_')] if syst else [nuis.GetName() for nuis in nuisance_parameters]

def get_nuisance_parameter_harmonised_names():
    '''
    >>> import pandas
    >>> df = pandas.read_excel('NP_name_experimental.xlsx')
    >>> from pprint import pprint
    >>> pprint([string.replace(u'(added by C. Deutsch May 15)', u'').replace(u'\xa0', u' ').replace(u' ', u'') for string in df['NP name']])
    '''
    return ['ATLAS_EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR',
            'ATLAS_EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR',
            'ATLAS_EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR',
            'ATLAS_EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR',
            'ATLAS_MUON_EFF_TrigStatUncertainty',
            'ATLAS_MUON_EFF_TrigSystUncertainty',
            'ATLAS_MUON_EFF_RECO_STAT',
            'ATLAS_MUON_EFF_RECO_SYS',
            'ATLAS_MUON_EFF_RECO_STAT_LOWPT',
            'ATLAS_MUON_EFF_RECO_SYS_LOWPT',
            'ATLAS_MUON_EFF_ISO_STAT',
            'ATLAS_MUON_EFF_ISO_SYS',
            'ATLAS_MUON_EFF_TTVA_STAT',
            'ATLAS_MUON_EFF_TTVA_SYS',
            'ATLAS_MUON_ID',
            'ATLAS_MUON_MS',
            'ATLAS_MUON_SCALE',
            'ATLAS_MUON_SAGITTA_RHO',
            'ATLAS_MUON_SAGITTA_RESBIAS',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA161718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA1718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2016',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2018',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2018AFTTS1',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC161718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC1718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2016',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2018',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2018AFTTS1',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYST161718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYST1718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2016',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2018',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2018AFTTS1',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYSTMU161718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYSTMU1718',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYSTMU2016',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYSTMU2018',
            'ATLAS_TAUS_TRUEHADTAU_EFF_TRIGGER_SYSTMU2018AFTTS1',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RECO_HIGHPT',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RECO_TOTAL',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_1PRONGSTATSYSTPT2025',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_1PRONGSTATSYSTPT2530',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_1PRONGSTATSYSTPT3040',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_1PRONGSTATSYSTPTGE40',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_3PRONGSTATSYSTPT2025',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_3PRONGSTATSYSTPT2530',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_3PRONGSTATSYSTPT3040',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_3PRONGSTATSYSTPTGE40',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_HIGHPT',
            'ATLAS_TAUS_TRUEHADTAU_EFF_RNNID_SYST',
            'ATLAS_TAUS_TRUEHADTAU_SME_TES_INSITUEXP',
            'ATLAS_TAUS_TRUEHADTAU_SME_TES_INSITUFIT',
            'ATLAS_TAUS_TRUEHADTAU_SME_TES_MODEL_CLOSURE',
            'ATLAS_TAUS_TRUEHADTAU_SME_TES_PHYSICSLIST',
            'ATLAS_TAUS_TRUEELECTRON_EFF_ELEBDT_STAT',
            'ATLAS_TAUS_TRUEELECTRON_EFF_ELEBDT_SYST',
            'ATLAS_TAUS_TRUEHADTAU_EFF_ELEOLR_TOTAL',
            'ATLAS_EG_RESOLUTION_ALL',
            'ATLAS_EG_SCALE_ALL',
            'ATLAS_EG_SCALE_AF2',
            'ATLAS_PH_EFF_TRIGGER',
            'ATLAS_PH_EFF_ID',
            'ATLAS_PH_EFF_ISO',
            'ATLAS_JET_EtaIntercalibration_Modelling',
            'ATLAS_JET_EtaIntercalibration_TotalStat',
            'ATLAS_JET_EtaIntercalibration_NonClosure_highE',
            'ATLAS_JET_EtaIntercalibration_NonClosure_negEta',
            'ATLAS_JET_EtaIntercalibration_NonClosure_posEta',
            'ATLAS_JET_Pileup_OffsetMu',
            'ATLAS_JET_Pileup_OffsetNPV',
            'ATLAS_JET_Pileup_PtTerm',
            'ATLAS_JET_Pileup_RhoTopology',
            'ATLAS_JET_Flavor_Composition',
            'ATLAS_JET_Flavor_Response',
            'ATLAS_JET_PunchThrough_MC16',
            'ATLAS_JET_PunchThrough_AFII',
            'ATLAS_JET_EffectiveNP_1',
            'ATLAS_JET_EffectiveNP_2',
            'ATLAS_JET_EffectiveNP_3',
            'ATLAS_JET_EffectiveNP_4',
            'ATLAS_JET_EffectiveNP_5',
            'ATLAS_JET_EffectiveNP_6',
            'ATLAS_JET_EffectiveNP_7',
            'ATLAS_JET_EffectiveNP_8restTerm',
            'ATLAS_JET_EffectiveNP_Detector1',
            'ATLAS_JET_EffectiveNP_Detector2',
            'ATLAS_JET_EffectiveNP_Mixed1',
            'ATLAS_JET_EffectiveNP_Mixed2',
            'ATLAS_JET_EffectiveNP_Mixed3',
            'ATLAS_JET_EffectiveNP_Mixed4',
            'ATLAS_JET_EffectiveNP_Modelling1',
            'ATLAS_JET_EffectiveNP_Modelling2',
            'ATLAS_JET_EffectiveNP_Modelling3',
            'ATLAS_JET_EffectiveNP_Modelling4',
            'ATLAS_JET_EffectiveNP_Statistical1',
            'ATLAS_JET_EffectiveNP_Statistical2',
            'ATLAS_JET_EffectiveNP_Statistical3',
            'ATLAS_JET_EffectiveNP_Statistical4',
            'ATLAS_JET_EffectiveNP_Statistical5',
            'ATLAS_JET_EffectiveNP_Statistical6',
            'ATLAS_JET_SingleParticle_HighPt',
            'ATLAS_JET_RelativeNonClosure_MC16',
            'ATLAS_JET_RelativeNonClosure_AFII',
            'ATLAS_JET_BJES_Response',
            'ATLAS_JET_EtaIntercalibration_NonClosure_2018data',
            'ATLAS_JET_JER_DataVsMC_MC16',
            'ATLAS_JET_JER_DataVsMC_AFII',
            'ATLAS_JET_JER_EffectiveNP_1',
            'ATLAS_JET_JER_EffectiveNP_2',
            'ATLAS_JET_JER_EffectiveNP_3',
            'ATLAS_JET_JER_EffectiveNP_4',
            'ATLAS_JET_JER_EffectiveNP_5',
            'ATLAS_JET_JER_EffectiveNP_6',
            'ATLAS_JET_JER_EffectiveNP_7',
            'ATLAS_JET_JER_EffectiveNP_8',
            'ATLAS_JET_JER_EffectiveNP_9',
            'ATLAS_JET_JER_EffectiveNP_10',
            'ATLAS_JET_JER_EffectiveNP_11',
            'ATLAS_JET_JER_EffectiveNP_12restTerm',
            'ATLAS_JET_JvtEfficiency',
            'ATLAS_JET_fJvtEfficiency',
            'ATLAS_Boosted_JET_Flavor_Composition',
            'ATLAS_Boosted_JET_Flavor_Response',
            'ATLAS_Boosted_JET_EtaIntercalibration_Modelling',
            'ATLAS_Boosted_JET_EtaIntercalibration_TotalStat',
            'ATLAS_Boosted_JET_EtaIntercalibration_NonClosure_highE',
            'ATLAS_Boosted_JET_EtaIntercalibration_NonClosure_negEta',
            'ATLAS_Boosted_JET_EtaIntercalibration_NonClosure_posEta',
            'ATLAS_Boosted_JET_EtaIntercalibration_NonClosure_2018data',
            'ATLAS_Boosted_JET_EffectiveNP_Detector1',
            'ATLAS_Boosted_JET_EffectiveNP_Detector2',
            'ATLAS_Boosted_JET_EffectiveNP_Mixed1',
            'ATLAS_Boosted_JET_EffectiveNP_Mixed2',
            'ATLAS_Boosted_JET_EffectiveNP_Mixed3',
            'ATLAS_Boosted_JET_EffectiveNP_Mixed4',
            'ATLAS_Boosted_JET_EffectiveNP_Modelling1',
            'ATLAS_Boosted_JET_EffectiveNP_Modelling2',
            'ATLAS_Boosted_JET_EffectiveNP_Modelling3',
            'ATLAS_Boosted_JET_EffectiveNP_Modelling4',
            'ATLAS_Boosted_JET_EffectiveNP_Statistical1',
            'ATLAS_Boosted_JET_EffectiveNP_Statistical2',
            'ATLAS_Boosted_JET_EffectiveNP_Statistical3',
            'ATLAS_Boosted_JET_EffectiveNP_Statistical4',
            'ATLAS_Boosted_JET_EffectiveNP_Statistical5',
            'ATLAS_Boosted_JET_EffectiveNP_Statistical6',
            'ATLAS_Boosted_JET_SingleParticle_HighPt',
            'ATLAS_Boosted_JET_LargeR_TopologyUncertainty_V',
            'ATLAS_Boosted_JET_LargeR_TopologyUncertainty_top',
            'ATLAS_Boosted_JET_MassRes_Hbb_comb',
            'ATLAS_Boosted_JET_MassRes_Top_comb',
            'ATLAS_Boosted_JET_CombMass_TotalStat',
            'ATLAS_Boosted_JET_CombMass_Tracking1',
            'ATLAS_Boosted_JET_CombMass_Tracking2',
            'ATLAS_Boosted_JET_CombMass_Tracking3',
            'ATLAS_Boosted_JET_CombMass_Baseline',
            'ATLAS_Boosted_JET_CombMass_Modelling',
            'ATLAS_FT_EFF_Eigen_B_0',
            'ATLAS_FT_EFF_Eigen_B_1',
            'ATLAS_FT_EFF_Eigen_B_2',
            'ATLAS_FT_EFF_Eigen_B_3',
            'ATLAS_FT_EFF_Eigen_B_4',
            'ATLAS_FT_EFF_Eigen_B_5',
            'ATLAS_FT_EFF_Eigen_B_6',
            'ATLAS_FT_EFF_Eigen_B_7',
            'ATLAS_FT_EFF_Eigen_B_8',
            'ATLAS_FT_EFF_Eigen_C_0',
            'ATLAS_FT_EFF_Eigen_C_1',
            'ATLAS_FT_EFF_Eigen_C_2',
            'ATLAS_FT_EFF_Eigen_C_3',
            'ATLAS_FT_EFF_Eigen_Light_0',
            'ATLAS_FT_EFF_Eigen_Light_1',
            'ATLAS_FT_EFF_Eigen_Light_2',
            'ATLAS_FT_EFF_Eigen_Light_3',
            'ATLAS_FT_EFF_Eigen_Light_4',
            'ATLAS_FT_EFF_extrapolation',
            'ATLAS_FT_EFF_extrapolation_from_charm',
            'ATLAS_MET_SoftTrk_ResoPara',
            'ATLAS_MET_SoftTrk_ResoPerp',
            'ATLAS_MET_SoftTrk_ScaleDown',
            'ATLAS_MET_SoftTrk_ScaleUp',
            'ATLAS_LUMI_Run2',
            'ATLAS_PU_PRW_DATASF',
            'ATLAS_TTBAR_FSR',
            'ATLAS_TTBAR_ME',
            'ATLAS_TTBAR_PS',
            'ATLAS_TTBAR_hdamp',
            'ATLAS_TTBAR_muF',
            'ATLAS_TTBAR_muR',
            ]

def filtered(harmonised_names_all, identity):
    return [f for f in harmonised_names_all if identity in f]


''' Known names that do not need to suggest new names '''
def known_unchange(channel, nuis_name):
    identified_channel_name = {
        'bbbb': [],
        'bbtautau': [],
        'bbyy': ['SPURIOUS_SM_1', 'SPURIOUS_SM_2', 'SPURIOUS_BSM_1', 'SPURIOUS_BSM_2',
                'BKG_p0_SM_1', 'BKG_p0_SM_2', 'BKG_p0_BSM_1', 'BKG_p0_BSM_2',
                'nbkg_SM_1', 'nbkg_SM_2', 'nbkg_BSM_1', 'nbkg_BSM_2',
                'ATLAS_LHCmass', 'ATLAS_HF_ggH', 'ATLAS_HF_VBF', 'ATLAS_HF_WH',],
    }

    return nuis_name in identified_channel_name[channel]

# def resolve_unknown(channel):
#     if channel == 'bbbb':
#         return {
#         }
#     elif channel == 'bbtautau':
#         pass
#     elif channel == 'bbyy':
#         pass

_UNKNOW = 'UNKNOW'

def values_are_uniq(nuis_dict, silence=False):
    values = list(nuis_dict.values())
    values = [value for value in values if value != _UNKNOW]
    if not silence and (len(values) != len(set(values))):
        assert(len(values) == len(set(values))), f'{len(values)} new names but {len(set(values))} identical: multiple old names are mapped to {set([x for x in values if values.count(x) > 1])}.'

def rename_nuisance_parameter(fname, ws_name, channel=None):
    model_config_name = 'ModelConfig'
    nuis_list = get_nuisance_parameter_names(fname, ws_name, model_config_name, syst=True)

    harmonised_names_all = get_nuisance_parameter_harmonised_names()
    nuis_dict = {}
    for nuis_name in nuis_list:
        ''' Reduce the list of harmonised_names_all if certain parttens are found in original nuis_name to avoid mismatch across categories '''
        for identity in ['_LUMI_', '_EL_', '_MUON_', '_EG_', '_TAUS_', '_JET_', '_FT_', '_MET_', '_PH_', '_PRW_', 'THEO_', '_Boosted_', '_HF_']:
            if identity in nuis_name:
                harmonised_names = filtered(harmonised_names_all, identity)
                break # This is important to break from for-else
        else:
            harmonised_names = harmonised_names_all

        ''' Find the closest match '''
        suggested_names = difflib.get_close_matches(nuis_name, harmonised_names, n=1)

        ''' Worth to have a special treatment for lumi '''
        if (not suggested_names) and ('lumi' in nuis_name.lower()):
            suggested_names = difflib.get_close_matches('LUMI', harmonised_names, n=1, cutoff=0.4)

        if suggested_names:
            ''' Find the longest matched sequence '''
            sequence = difflib.SequenceMatcher(None, nuis_name, suggested_names[0])
            match = sequence.find_longest_match(0, len(nuis_name), 0, len(suggested_names[0]))
            match.a, match.b, match.size
            ahead = nuis_name[ : match.a]
            atail = nuis_name[match.a+match.size : ]
            bhead = suggested_names[0][ : match.b]
            btail = suggested_names[0][match.b+match.size : ]
            common1 = nuis_name[match.a : match.a+match.size]
            common2 = suggested_names[0][match.b : match.b+match.size]
            assert(common1 == common2)
            print(f'{ahead}\033[91m{common1}\033[0m{atail}'.rjust(80, ' '), '->', f'{bhead}\033[92m{common1}\033[0m{btail}')
            # print(nuis_name.rjust(80, ' '), '->', suggested_names[0])
        else:
            ''' Does not find any overlap with conventional names
                - If 'THEO/theo': theory related, no correlation
                - Elif endswith '_b2b' '_b3b' or '_b4b': 4b 
            '''
            if 'theo' in nuis_name.lower():
                suggested_names = ['THEO_' + nuis_name.replace('alpha_', '').replace('THEO_', '').replace('THEO', '').replace('theo_', '').replace('theo', '')]
                print(f'\033[91m{nuis_name}\033[0m'.rjust(80, ' '), '->', f'\033[92m{suggested_names[0]}\033[0m')
            elif nuis_name.endswith('_b2b') or nuis_name.endswith('_b3b') or nuis_name.endswith('_b4b'):
                assert(channel == 'bbbb'), 'Expect 4b channel for *_b?b'
                suggested_names = ['THEO_' + nuis_name.replace('alpha_', '').replace('MODEL_', '').replace('THEO', '').replace('theo_', '').replace('theo', '')]
                print(f'\033[91m{nuis_name}\033[0m'.rjust(80, ' '), '->', f'\033[92m{suggested_names[0]}\033[0m')
            elif '_ttbar_' in nuis_name.lower():
                suggested_names = ['THEO_XS_' + nuis_name.replace('alpha_', '')]
                print(f'\033[91m{nuis_name}\033[0m'.rjust(80, ' '), '->', f'\033[92m{suggested_names[0]}\033[0m')
            elif channel and known_unchange(channel, nuis_name):
                suggested_names = [nuis_name.replace('alpha_', '')]
            else:
                suggested_names = [_UNKNOW]
                print(nuis_name.rjust(80, ' '), '->', f'\033[91m{suggested_names[0]}\033[0m')
        nuis_dict[nuis_name] = suggested_names[0]
    return nuis_dict


def _head(channel, ws_name):
    return f'''
  <!-- ***************** -->
  <!-- Channel: {channel} -->
  <!-- ***************** -->

  <Channel Name="{channel}">

    <File Name="{channel}_INPUT_WS"/>
    <Workspace Name="{ws_name}"/>
    <ModelConfig Name="ModelConfig"/>
    <ModelPOI Name="POINAME"/>
    <ModelData Name="combData"/>
   <!-- {channel} systematics rename map -->
   <RenameMap>
    <!-- Format: -->
    <!-- OldName="PDFname_old( NPname_old, GlobalObs_old)" NewName="NPname_new" -->
    '''

def _tail(channel):
    return f'''
    <!-- {channel} category renaming -->
    <Syst OldName="channelCat" NewName="Cat_{channel}"/> 
   </RenameMap>

  </Channel>
'''

def _syst(old_names, new_names, category):
    def item(old_name, new_names):
        return f'''     <Syst OldName="{old_name}Constraint( {old_name}, nom_{old_name})" NewName="{new_names}" />'''
    
    items = []
    for old_name, new_name in zip(old_names, new_names):
        items.append(item(old_name, new_name))

    return f'''
    <!-- {category} -->
''' + '\n'.join(items)

def main(args):
    channel = args.channel

    fname = f'{args.path}/{channel}/{args.process}/{args.mass}.root'
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mWorkspace file\033[0m'.rjust(40, ' '), fname)
    ws_names = {'bbbb': 'w', 'bbyy': 'combWS', 'bbtautau': 'combined',
    }
    ws_name = args.workspace if args.workspace else ws_names[channel]
    xml_name = 'fullcorr.xml'

    contents = []

    ''' Write head '''
    contents.append(_head(channel, ws_name, ))

    ''' Write body '''
    categories = {
        'Luminosity': '_LUMI_',
        'Electron': '_EL_',
        'Muon': '_MUON_',
        'EG': '_EG_',
        'Tau': '_TAUS_',
        'Jet': '_JET_',
        'FTag': '_FT_',
        'MET': '_MET_',
        'Photon': '_PH_',
        'Pile-up': '_PRW_',
        'Theory': 'THEO_',
        'HeavyFlavour': '_HF_',
    }


    nuis_dict = rename_nuisance_parameter(fname, ws_name, channel)
    values_are_uniq(nuis_dict, silence=args.allow_same_new)
    new_NP = list(nuis_dict.values())
    old_NP = list(nuis_dict.keys())

    for category in categories:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mProcess category\033[0m'.rjust(40, ' '), category)
        new_np = [np for np in new_NP if categories[category] in np]
        old_np = [old_NP[new_NP.index(value)] for value in new_np]
        contents.append(_syst(old_np, new_np, category))
        for i in old_np:
            if args.allow_same_new:
                nuis_dict.pop(i, None)
            else:
                nuis_dict.pop(i)

    if nuis_dict.keys(): # For reminders that cannot categorised and not unknown
        new_NP = list(nuis_dict.values())
        old_NP = list(nuis_dict.keys())
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mProcess category\033[0m'.rjust(40, ' '), 'Uncategorised')
        new_np = [np for np in new_NP if _UNKNOW != np]
        old_np = [old_NP[new_NP.index(value)] for value in new_np]

        contents.append(_syst(old_np, new_np, 'Uncategorised'))
        for i in old_np:
            if args.allow_same_new:
                nuis_dict.pop(i, None)
            else:
                nuis_dict.pop(i)

    if not nuis_dict.keys():
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mAll NPs are resolved\033[0m'.rjust(40, ' '))
    else:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[1;40mRemaining NPs\033[0m'.rjust(40, ' '), list(nuis_dict.keys()))

    ''' Write tail '''
    contents.append(_tail(channel))

    ''' Save XML card '''
    makedirs(f'schemes/{channel}', exist_ok=True)
    with open(f'schemes/{channel}/{xml_name}', 'w') as f:
        for content in contents:
            print(content, file=f)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mSave\033[0m'.rjust(40, ' '), f'schemes/{channel}/{xml_name}')


if __name__ == '__main__':
    
    """Get arguments from command line."""
    parser = ArgumentParser(description="\033[92mCreate templates and configuration files for TRExFitter.\033[0m")
    parser.add_argument('--allow-same-new', action='store_true', default=False, help='Allow different old names to map to the same new name. \033[92mUse it with Caution; should by default turned off. This is a walkaround for typos of channels.\033[0m (default: %(default)s)')
    parser.add_argument('-c', '--channel', type=str, default='bbtautau', choices=['bbbb', 'bbyy', 'bbtautau'], help='Channel of workspace (example: %(default)s)')
    parser.add_argument('-p', '--process', type=str, default='nonres', choices=['non-res', 'spin0', 'spin2'], help='Signal process of workspace (example: %(default)s)')
    parser.add_argument('--path', type=str, default='../../input/20210309/', help='Path to workspace up to the parent of process folder (example: %(default)s)')
    parser.add_argument('-m', '--mass', type=str, default='0', help='Mass point of workspace (example: %(default)s)')
    parser.add_argument('-w', '--workspace', type=str, default=None, help='Name of workspace (example: %(default)s)')

    args = parser.parse_args()
    if args.channel == 'bbyy':
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92mLoad RooTwoSidedCBShape for\033[0m'.rjust(40, ' '), args.channel)
        from quickstats.components import ExtendedModel
        ExtendedModel.load_extension()
    main(args)
