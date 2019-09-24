#!/usr/bin/env python

NP_dictionary = {}

channels = ['bbbb', 'bbyy', 'bbtautau']

def addNP(name_ws, name_short="n.a.", name_long="n.a.", label=None, channel="infer", category="unknown"):

    # - Infer channel
    if channel == "infer":

        channels = ["bbbb", "bbtautau", "bbyy"]

        for ch in channels:
            if ch in name_ws:
                channel = ch

#   if label is None:
#       label = name_short

    entry = {
            'name_short' : name_short,
            'name_long'  : name_long,
            'label'      : label,
            'channel'    : channel,
            'category'   : category,
            }

    NP_dictionary[name_ws] = entry



def list_unknown_NPs(outfile_path=None, channels=channels):

    if outfile_path is not None:
        f_out = open(outfile_path, 'w')
    
    for ch in channels:
        for NP_key, entry in NP_dictionary.items():
        
            if ch == entry['channel'] and entry['label'] is None: 
                print(NP_key)
        
                if outfile_path is not None:
                    row = "{:8s}: {}\n".format(ch, NP_key)
                    f_out.write(row)
        
    if outfile_path is not None:
        f_out.close()


##############################
#####                    #####
##### ----- Common ----- #####
#####                    #####
##############################

#####################
## -- Electrons -- ##
#####################
# - Ref:
# - https://twiki.cern.ch/twiki/bin/view/AtlasProtected/ElectronEfficiencyCorrelationModel
addNP("ATLAS_EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR",   "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR",   "n.a.", "$e$ $\epsilon_{\mathrm{ID}}$ ",                 "common", "experimental:electron")
addNP("ATLAS_EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR",  "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR",  "n.a.", "$e$ $\epsilon_{\mathrm{Iso}}$ ",                "common", "experimental:electron")
addNP("ATLAS_EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR", "n.a.", "$e$ $\epsilon_{\mathrm{Reco}}$ ",               "common", "experimental:electron")

#################
## -- Muons -- ##
#################
# - Ref:
# - https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MuonPerformance
# - https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MCPAnalysisGuidelinesMC16

addNP("ATLAS_MUON_EFF_STAT",                       "MUON_EFF_STAT",                       "n.a.", r"$\mu$ $\epsilon$ stat",        "common", "experimental:muon")
addNP("ATLAS_MUON_EFF_SYS",                        "MUON_EFF_SYS",                        "n.a.", r"$\mu$ $\epsilon$ sys",         "common", "experimental:muon")
addNP("ATLAS_MUON_EFF_TrigSystUncertainty",        "MUON_EFF_TrigSystUncertainty",        "n.a.", r"$\mu$ $\epsilon$ TrigSyst",    "common", "experimental:muon")
addNP("ATLAS_MUON_TTVA_STAT",                      "MUON_TTVA_STAT",                      "n.a.", r"$\mu$ $\epsilon$ track-to-vertex stat",   "common", "experimental:muon")


#################
## -- Taus -- ##
#################
# - Ref:
addNP("alpha_SysTAUS_TRUEELECTRON_EFF_ELEOLR_TOTAL_bbtautau",       "n.a", "n.a.", r"$\tau$ $\epsilon$",                                         "common", "experimental:tau")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_ELEOLR_TOTAL_bbtautau",         "n.a", "n.a.", r"$\tau$ Electron OR",                                        "common", "experimental:tau")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_JETID_HIGHPT_bbtautau",         "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{ID}}$ (high $p_{\mathrm{T}}$)",   "common", "experimental:tau:id")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_JETID_TOTAL_bbtautau",          "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{ID}}$ (total)",                   "common", "experimental:tau:id")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_RECO_HIGHPT_bbtautau",          "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{reco}}$ (high $p_{\mathrm{T}}$)", "common", "experimental:tau:reco")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_RECO_TOTAL_bbtautau",           "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{reco}}$ (total)",                 "common", "experimental:tau:reco")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2015_bbtautau", "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{trigger}}$ statdata2015",         "common", "experimental:tau:trigger")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2016_bbtautau", "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{trigger}}$ statdata2016",         "common", "experimental:tau:trigger")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2016_bbtautau",   "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{trigger}}$ statmc2016",           "common", "experimental:tau:trigger")
addNP("alpha_SysTAUS_TRUEHADTAU_EFF_TRIGGER_SYST2016_bbtautau",     "n.a", "n.a.", r"$\tau$ $\epsilon_{\mathrm{trigger}}$ syst2016",             "common", "experimental:tau:trigger")
addNP("alpha_SysTAUS_TRUEHADTAU_SME_TES_DETECTOR_bbtautau",         "n.a", "n.a.", r"$\tau$ E smearing & scale (detector)",                      "common", "experimental:tau:energy_scale")
addNP("alpha_SysTAUS_TRUEHADTAU_SME_TES_INSITU_bbtautau",           "n.a", "n.a.", r"$\tau$ E smearing & scale (insitu"),                        "common", "experimental:tau:energy_scale")
addNP("alpha_SysTAUS_TRUEHADTAU_SME_TES_MODEL_bbtautau",            "n.a", "n.a.", r"$\tau$ E smearing & scale (model)",                         "common", "experimental:tau:energy_scale")

###################
## -- Photons -- ##
###################
# - Ref:
addNP("ATLAS_EG_SCALE_ALL",                        "EG_SCALE_ALL",                        "n.a.", "$\gamma$ scale",                    "common", "experimental:photon")

###########################
## -- Flavour tagging -- ##
###########################
# - Ref:
addNP("ATLAS_FT_EFF_Eigen_B_0",                    "FT_EFF_Eigen_B_0",                    "n.a.", "FT $\epsilon$ $b$ eigen-0",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_B_1",                    "FT_EFF_Eigen_B_1",                    "n.a.", "FT $\epsilon$ $b$ eigen-1",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_B_2",                    "FT_EFF_Eigen_B_2",                    "n.a.", "FT $\epsilon$ $b$ eigen-2",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_B_3",                    "FT_EFF_Eigen_B_3",                    "n.a.", "FT $\epsilon$ $b$ eigen-3",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_C_0",                    "FT_EFF_Eigen_C_0",                    "n.a.", "FT $\epsilon$ $c$ eigen-0",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_C_1",                    "FT_EFF_Eigen_C_1",                    "n.a.", "FT $\epsilon$ $c$ eigen-1",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_C_2",                    "FT_EFF_Eigen_C_2",                    "n.a.", "FT $\epsilon$ $c$ eigen-2",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_Light_0",                "FT_EFF_Eigen_Light_0",                "n.a.", "FT $\epsilon$ $l$ eigen-0",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_Light_1",                "FT_EFF_Eigen_Light_1",                "n.a.", "FT $\epsilon$ $l$ eigen-1",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_Light_2",                "FT_EFF_Eigen_Light_2",                "n.a.", "FT $\epsilon$ $l$ eigen-2",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_Light_3",                "FT_EFF_Eigen_Light_3",                "n.a.", "FT $\epsilon$ $l$ eigen-3",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_Eigen_Light_4",                "FT_EFF_Eigen_Light_4",                "n.a.", "FT $\epsilon$ $l$ eigen-4",         "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_extrapolation",                "FT_EFF_extrapolation",                "n.a.", "FT $\epsilon$ extrapol.",           "common", "experimental:flavour_tagging")
addNP("ATLAS_FT_EFF_extrapolation_from_charm",     "FT_EFF_extrapolation_from_charm",     "n.a.", "FT $\epsilon$ extrapol from charm", "common", "experimental:flavour_tagging")

################
## -- Jets -- ##
################
# - Ref:
addNP("ATLAS_JET_EtaIntercalib_Nonclos",           "JET_EtaIntercalib_Nonclos",           "n.a.", "Jet $\eta$ intercalib nonclosure",  "common", "experimental:jet")
addNP("ATLAS_JET_GroupedNP_1",                     "JET_GroupedNP_1",                     "n.a.", "Jet NP2",                           "common", "experimental:jet")
addNP("ATLAS_JET_GroupedNP_2",                     "JET_GroupedNP_2",                     "n.a.", "Jet NP3",                           "common", "experimental:jet")
addNP("ATLAS_JET_GroupedNP_3",                     "JET_GroupedNP_3",                     "n.a.", "Jet JER",                           "common", "experimental:jet")
addNP("ATLAS_JET_JER",                             "JET_JER",                             "n.a.", "Jet JER",                           "common", "experimental:jet")

######################
## -- Luminosity -- ##
######################
# - Ref:
addNP("ATLAS_LUMI_15_16",                          "LUMI_15_16",                          "n.a.", "$\mathcal{L}$",                     "common", "experimental:luminosity")

###############
## -- MET -- ##
###############
# - Ref:
addNP("ATLAS_MET_SoftTrk_ResoPara",                "MET_SoftTrk_ResoPara",                "n.a.", "$\E_{T}^{\text{miss}}$",            "common", "experimental:MET")
addNP("ATLAS_MET_SoftTrk_ResoPerp",                "MET_SoftTrk_ResoPerp",                "n.a.", "$\E_{T}^{\text{miss}$",             "common", "experimental:MET")
addNP("ATLAS_MET_SoftTrk_Scale",                   "MET_SoftTrk_Scale",                   "n.a.", "$\E_{T}^{\text{miss}$",             "common", "experimental:MET")

##################
## -- Pileup -- ##
##################
# - Ref:
addNP("ATLAS_PRW_DATASF",                          "PRW_DATASF",                          "n.a.", "Pile-up",                           "common", "experimental:pileup")


#############################
#####                   #####
##### ----- bbbbb ----- #####
#####                   #####
#############################


# - Experimental
addNP("alpha_Signal_FT_EFF_Eigen_B_4_bbbb", "FT_EFF_Eigen_B_4", "n.a.", "FT $\epsilon $b$$ 4",  "bbbb", "experimental:flavour_tagging")
addNP("alpha_2015_Luminosity_bbbb",         "LUMI_2015",        "n.a.", "$\mathcal{L}$ (2015)", "bbbb", "experimental:luminosity")
addNP("alpha_2016_Luminosity_bbbb",         "LUMI_2016",        "n.a.", "$\mathcal{L}$ (2016)", "bbbb", "experimental:luminosity")
addNP("alpha_2015_Signal_trig_bbbb",        "Signal trigger",   "Uncertainty on the emulated trigger scale factors (2015)", "Trigger 2015",         "bbbb", "experimental:trigger")
addNP("alpha_2016_Signal_trig_bbbb",        "Signal trigger",   "Uncertainty on the emulated trigger scale factors (2016)", "Trigger 2016",         "bbbb", "experimental:trigger")

# - shape - #
addNP("alpha_2015_HighHtCR_bbbb", "HighHtCR_2015", "Background shape variation determined by the non-closure between SB and CR", "High $H_{T}$ CR (2015)", "bbbb", "shape")
addNP("alpha_2016_HighHtCR_bbbb", "HighHtCR_2016", "Background shape variation determined by the non-closure between SB and CR", "High $H_{T}$ CR (2015)", "bbbb", "shape")
addNP("alpha_2015_LowHtCR_bbbb",  "LowHtCR_2015",  "Background shape variation determined by the non-closure between SB and CR", "High $H_{T}$ CR (2015)", "bbbb", "shape")
addNP("alpha_2016_LowHtCR_bbbb",  "LowHtCR_2016",  "Background shape variation determined by the non-closure between SB and CR", "High $H_{T}$ CR (2016)", "bbbb", "shape")

# - Theory - #
addNP("alpha_#mu_R_and_#mu_F_bbbb",              "muR_muF",         "n.a.", "$\mu_{R}$ and $\mu_{F}$ variations", "bbbb", "theory:scale")
addNP("alpha_Shower_and_hadronisation_bbbb",     "Shower and hadronisation", "Shower and hadronisation, POWHEG+Pythia vs. aMC@NLO+Herwig", "Shower and hadronisation", "bbbb", "theory:signal:shower")
addNP("alpha_Theoretical_bbbb",                  "n.a",             "n.a.", None, "bbbb", "theory:signal")

# - Background normalisation - #
addNP("alpha_2015_norm_NP0_bbbb",                "norm NP0 (2015)", "n.a.", "Normalisation 0 (2015)", "bbbb", "normalisation:CR")
addNP("alpha_2015_norm_NP1_bbbb",                "norm NP1 (2015)", "n.a.", "Normalisation 1 (2015)", "bbbb", "normalisation:CR")
addNP("alpha_2015_norm_NP2_bbbb",                "norm NP2 (2015)", "n.a.", "Normalisation 2 (2015)", "bbbb", "normalisation:CR")
addNP("alpha_2016_norm_NP0_bbbb",                "norm NP0 (2016)", "n.a.", "Normalisation 0 (2016)", "bbbb", "normalisation:CR")
addNP("alpha_2016_norm_NP1_bbbb",                "norm NP1 (2016)", "n.a.", "Normalisation 1 (2016)", "bbbb", "normalisation:CR")
addNP("alpha_2016_norm_NP2_bbbb",                "norm NP2 (2016)", "n.a.", "Normalisation 2 (2016)", "bbbb", "normalisation:CR")

# - gamma - #
addNP("gamma_stat_resolved_4b_2015_bin_22_bbbb", "gamma_stat_2015_bin_22", "n.a.", "$\gamma$ bin 22 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_23_bbbb", "gamma_stat_2015_bin_23", "n.a.", "$\gamma$ bin 23 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_24_bbbb", "gamma_stat_2015_bin_24", "n.a.", "$\gamma$ bin 24 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_25_bbbb", "gamma_stat_2015_bin_25", "n.a.", "$\gamma$ bin 25 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_26_bbbb", "gamma_stat_2015_bin_26", "n.a.", "$\gamma$ bin 26 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_27_bbbb", "gamma_stat_2015_bin_27", "n.a.", "$\gamma$ bin 27 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_28_bbbb", "gamma_stat_2015_bin_28", "n.a.", "$\gamma$ bin 28 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_29_bbbb", "gamma_stat_2015_bin_29", "n.a.", "$\gamma$ bin 29 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_30_bbbb", "gamma_stat_2015_bin_30", "n.a.", "$\gamma$ bin 30 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_31_bbbb", "gamma_stat_2015_bin_31", "n.a.", "$\gamma$ bin 31 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_32_bbbb", "gamma_stat_2015_bin_32", "n.a.", "$\gamma$ bin 32 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_33_bbbb", "gamma_stat_2015_bin_33", "n.a.", "$\gamma$ bin 33 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_34_bbbb", "gamma_stat_2015_bin_34", "n.a.", "$\gamma$ bin 34 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_35_bbbb", "gamma_stat_2015_bin_35", "n.a.", "$\gamma$ bin 35 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_36_bbbb", "gamma_stat_2015_bin_36", "n.a.", "$\gamma$ bin 36 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_37_bbbb", "gamma_stat_2015_bin_37", "n.a.", "$\gamma$ bin 37 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_38_bbbb", "gamma_stat_2015_bin_38", "n.a.", "$\gamma$ bin 38 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_39_bbbb", "gamma_stat_2015_bin_39", "n.a.", "$\gamma$ bin 39 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_40_bbbb", "gamma_stat_2015_bin_40", "n.a.", "$\gamma$ bin 40 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2015_bin_41_bbbb", "gamma_stat_2015_bin_41", "n.a.", "$\gamma$ bin 41 (2015)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_27_bbbb", "gamma_stat_2016_bin_27", "n.a.", "$\gamma$ bin 27 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_28_bbbb", "gamma_stat_2016_bin_28", "n.a.", "$\gamma$ bin 28 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_30_bbbb", "gamma_stat_2016_bin_30", "n.a.", "$\gamma$ bin 29 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_31_bbbb", "gamma_stat_2016_bin_31", "n.a.", "$\gamma$ bin 30 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_32_bbbb", "gamma_stat_2016_bin_32", "n.a.", "$\gamma$ bin 31 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_33_bbbb", "gamma_stat_2016_bin_33", "n.a.", "$\gamma$ bin 32 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_34_bbbb", "gamma_stat_2016_bin_34", "n.a.", "$\gamma$ bin 33 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_35_bbbb", "gamma_stat_2016_bin_35", "n.a.", "$\gamma$ bin 34 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_36_bbbb", "gamma_stat_2016_bin_36", "n.a.", "$\gamma$ bin 35 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_37_bbbb", "gamma_stat_2016_bin_37", "n.a.", "$\gamma$ bin 36 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_38_bbbb", "gamma_stat_2016_bin_38", "n.a.", "$\gamma$ bin 37 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_39_bbbb", "gamma_stat_2016_bin_39", "n.a.", "$\gamma$ bin 38 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_40_bbbb", "gamma_stat_2016_bin_40", "n.a.", "$\gamma$ bin 39 (2016)", "bbbb", "gamma")
addNP("gamma_stat_resolved_4b_2016_bin_41_bbbb", "gamma_stat_2016_bin_41", "n.a.", "$\gamma$ bin 40 (2016)", "bbbb", "gamma")

# - Unsorted - #


#################################
#####                       #####
##### ----- bbbtautau ----- #####
#####                       #####
#################################


## -- Theory -- ##
addNP("alpha_SigAcc_bbtautau",                                                                               "n.a", "n.a.", None, "bbtautau", "unknown")


## -- Experimental -- ##
addNP("alpha_SysEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR_bbtautau",                                            "n.a", "n.a.", None, "bbtautau", "unknown")

## -- Shape -- ##
addNP("alpha_Sys1tag2tagTF_bbtautau",                                                                        "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysCPVarFakes_bbtautau",                                                                        "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysCompFakes_SpcTauHH_bbtautau",                                                                "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysCompFakes_SpcTauLH_bbtautau",                                                                "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysFFStatQCD_SpcTauHH_bbtautau",                                                                "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysFFStatQCD_SpcTauLH_bbtautau",                                                                "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysFFStatTtbar_bbtautau",                                                                       "n.a", "n.a.", None, "bbtautau", "unknown")

# - 
addNP("alpha_SysTTBAR_NNLO_bbtautau", "ttbar_NNLO", "n.a.", r"$t\bar{t}$ bkgr. NNLO modelling",                  "bbtautau", "shape:background:ttbar")
addNP("alpha_SysTTbarMBB_bbtautau",   "ttbar_mbb",  "n.a.", r"$t\bar{t}$ bkgr. modelling in $m_{bb}$",           "bbtautau", "shape:background:ttbar")
addNP("alpha_SysTTbarPTH_bbtautau",   "ttbar_pTh",  "n.a.", r"$t\bar{t}$ bkgr. modelling in $p_{\mathrm{T},h}$", "bbtautau", "shape:background:ttbar")
addNP("alpha_SysTTbarPTV_bbtautau",   "ttbar_pTV",  "n.a.", r"$t\bar{t}$ bkgr. modelling in $p_{\mathrm{T},V}$", "bbtautau", "shape:background:ttbar")

# - Fake  - #
addNP("alpha_SysFF_MTW_bbtautau",                                                                            "n.a", "n.a.", None, "bbtautau", "unknown")

addNP("alpha_SysFR_MTW_CUT_bbtautau",                                                                        "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysFR_STTfraction_bbtautau",                                                                    "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysFR_Stat_bbtautau",                                                                           "n.a", "n.a.", None, "bbtautau", "unknown")

## -- Normalisation -- ##
addNP("ATLAS_norm_Zbb_bbtautau",                                                                             "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("ATLAS_norm_ttbar_bbtautau",                                                                           "n.a", "n.a.", None, "bbtautau", "unknown")

addNP("alpha_FR_ttbarNorm_bbtautau",                                                                         "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysDibosonNorm_bbtautau",                                                                       "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysHiggsNorm_bbtautau",                                                                         "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysWNorm_bbtautau",                                                                             "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysZNorm_bbtautau",                                                                             "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysZttNorm_bbtautau",                                                                           "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysstopWtNorm_bbtautau",                                                                        "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysstoptNorm_bbtautau",                                                                         "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysttHNorm_bbtautau",                                                                           "n.a", "n.a.", None, "bbtautau", "unknown")

# - Background normalisation extrapolation factors from control region to signal region
# - for ttbar and Z+hHF in bb̄ττ
addNP("alpha_SysRatioHHSRTtbarAcc2Tag_bbtautau",                                                             "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysRatioHHSRZhfAcc2Tag_bbtautau",                                                               "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysRatioLHSRZhfAcc2Tag_bbtautau",                                                               "n.a", "n.a.", None, "bbtautau", "unknown")




# - gamma
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L0_Y2015_distBDT_DSRSMRW_SpcTauHH_bin_0_bbtautau",       "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L0_Y2015_distBDT_DSRSMRW_SpcTauHH_bin_1_bbtautau",       "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L0_Y2015_distBDT_DSRSMRW_SpcTauHH_bin_2_bbtautau",       "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L0_Y2015_distBDT_DSRSMRW_SpcTauHH_bin_3_bbtautau",       "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L0_Y2015_distBDT_DSRSMRW_SpcTauHH_bin_4_bbtautau",       "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_0_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_10_bbtautau", "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_11_bbtautau", "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_12_bbtautau", "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_13_bbtautau", "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_14_bbtautau", "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_15_bbtautau", "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_1_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_2_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_3_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_4_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_5_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_6_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_7_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_8_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT0_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_9_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT1_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_0_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT1_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_1_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT1_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_2_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT1_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_3_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L1_LTT1_Y2015_distBDT_DSRSMRW_SpcTauLH_bin_4_bbtautau",  "n.a", "n.a.", None, "bbtautau", "gamma")
addNP("gamma_stat_Region_BMin0_incJet1_J2_T2_isMVA0_L2_Y2015_distmLL_DSR_bin_0_bbtautau",                    "n.a", "n.a.", None, "bbtautau", "gamma")

# - Unsorted
addNP("alpha_SysMUON_EFF_TrigStatUncertainty_bbtautau",                                                      "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysOSSS_bbtautau",                                                                              "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysSS_bbtautau",                                                                                "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysSubtraction_bkg_SpcTauHH_bbtautau",                                                          "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysSubtraction_bkg_SpcTauLH_bbtautau",                                                          "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysTTbarGenFakes_bbtautau",                                                                     "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysZtautauMBB_bbtautau",                                                                        "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysZtautauPTH_bbtautau",                                                                        "n.a", "n.a.", None, "bbtautau", "unknown")
addNP("alpha_SysRatioZCRTtbarAcc2Tag_bbtautau",                                                              "n.a", "n.a.", None, "bbtautau", "unknown")



############################
#####                  #####
##### ----- bbyy ----- #####
#####                  #####
############################


addNP("dFT_EFF_Eigen_B_bbyy",     "n.a", "n.a", None, "bbyy", "experimental:flavour_tagging")
addNP("dFT_EFF_Eigen_C_bbyy",     "n.a", "n.a", None, "bbyy", "experimental:flavour_tagging")
addNP("dFT_EFF_Eigen_Light_bbyy", "n.a", "n.a", None, "bbyy", "experimental:flavour_tagging")

addNP("dJES_bbyy",                "n.a", "n.a", None, "bbyy", "experimental:jet")

addNP("BRbb_bbyy",                "n.a", "n.a", None, "bbyy", "theory:branching_fraction")
addNP("BRgg_bbyy",                "n.a", "n.a", None, "bbyy", "theory:branching_fraction")

addNP("Iso_bbyy",                 "n.a", "n.a", None, "bbyy")

addNP("bias_bb_bbyy",             "n.a", "n.a", None, "bbyy", "spurious_signal")
addNP("bias_bj_bbyy",             "n.a", "n.a", None, "bbyy", "spurious_signal")

addNP("dBBHStat_bb_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dBBHStat_bj_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dBBHTh_bbyy",              "n.a", "n.a", None, "bbyy")

addNP("dBSMStat_bb_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dBSMStat_bj_bbyy",         "n.a", "n.a", None, "bbyy")

addNP("dGGFStat_bb_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dGGFStat_bj_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dGGFTh_bbyy",              "n.a", "n.a", None, "bbyy")
addNP("dGGHF_bbyy",               "n.a", "n.a", None, "bbyy")

addNP("dGGPdf_bbyy",              "n.a", "n.a", None, "bbyy")
addNP("dQQPdf_bbyy",              "n.a", "n.a", None, "bbyy")

addNP("dTHTh_bbyy",               "n.a", "n.a", None, "bbyy")

addNP("dTTHStat_bb_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dTTHStat_bj_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dTTHTh_bbyy",              "n.a", "n.a", None, "bbyy")

addNP("dVBFStat_bb_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dVBFStat_bj_bbyy",         "n.a", "n.a", None, "bbyy")
addNP("dVBFTh_bbyy",              "n.a", "n.a", None, "bbyy")

addNP("dVHTh_bbyy",               "n.a", "n.a", None, "bbyy")

addNP("dWHStat_bb_bbyy",          "n.a", "n.a", None, "bbyy")
addNP("dWHStat_bj_bbyy",          "n.a", "n.a", None, "bbyy")

addNP("dZHStat_bb_bbyy",          "n.a", "n.a", None, "bbyy")
addNP("dZHStat_bj_bbyy",          "n.a", "n.a", None, "bbyy")

addNP("nbkg_bb_bbyy",             "n.a", "n.a", None, "bbyy")
addNP("nbkg_bj_bbyy",             "n.a", "n.a", None, "bbyy")

addNP("slope_bb_bbyy",            "n.a", "n.a", None, "bbyy",     "shape")
addNP("slope_bj_bbyy",            "n.a", "n.a", None, "bbyy",     "shape")


############################
#####                  #####
##### ----- bbWW ----- #####
#####                  #####
############################


############################
#####                  #####
##### ----- WWyy ----- #####
#####                  #####
############################

############################
#####                  #####
##### ----- WWWW ----- #####
#####                  #####
############################
