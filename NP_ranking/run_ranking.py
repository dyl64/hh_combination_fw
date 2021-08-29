import os
import sys
from pdb import set_trace

if sys.argv[1] not in ['nonres', 'spin0']:
    print('Usage: python', sys.argv[0], 'nonres|spin0', '0|1|2')
    exit()
if sys.argv[1] == 'spin0' and sys.argv[2] not in ['0', '1', '2']:
    print('Usage: python', sys.argv[0], 'nonres|spin0', '0|1|2')
    exit()

analysis = sys.argv[1]
total_split = 1 if analysis == 'nonres' else 3
split = 0 if analysis == 'nonres' else int(sys.argv[2])


dataset = "asimov_data"
extra_options = {
    "exclude": "\"gamma_*,nbkg*,BKG*,xi*,ATLAS_norm*,NORM_*\"",
#    "fix": "\"THEO_XS_fixmu_*=0, alpha_THEO_XS_PDFalphas_VBFSMHH=0,"
#           " alpha_THEO_XS_PDFalphas_ggFSMHH=0, alpha_THEO_XS_SCALEMTop_ggFSMHH=0,"
#           " THEO_XS_COMBINED_HH_ggF=0, THEO_XS_PDFalphas_HH_VBF=0,"
#           " THEO_XS_PDFalphas_HH_ggF=0, THEO_XS_SCALE_HH_VBF=0\""
}

CURRENT_DIR = os.getcwd() + '/../../NP_ranking/'
POI_NAME = "xsec_br"
DATASET_NAMES = {
    "observed_data": "combData",
    "asimov_data": "asimovData_1"
}
WS_BASE_PATH = {
    "nonres": "/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output_mu_unblind/",
    "spin0": "/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output/"
}

WS_SUB_PATH = {
    "nonres": {
        "bbyy": "rescaled/nonres/bbyy/asimov1.{mass}.root",
        "bbtautau": "rescaled/nonres/bbtautau/asimov1.{mass}.root",
        "bbbb": "rescaled/nonres/bbbb/asimov1.{mass}.root",
        "combined": "combined/nonres/A-bbtautau_bbyy-fullcorr/asimov1.{mass}.root"
    },
    "spin0": {
        "bbyy": "rescaled/spin0/bbyy/asimov1.{mass}.root",
        "bbtautau": "rescaled/spin0/bbtautau/asimov1.{mass}.root",
        "bbbb": "rescaled/spin0/bbbb/asimov1.{mass}.root",
        "combined": "combined/spin0/A-bbbb_bbtautau_bbyy-fullcorr/asimov1.{mass}.root"
    }
}
CHANNELS = {
    "nonres": ["bbyy", "bbtautau", "combined"],
    #"nonres": ["combined"],
    "spin0": ["bbbb", "bbtautau", "bbyy", "combined"]
}
MASSES = {
    "nonres":{
        "bbyy": ["0"],
        "bbtautau": ["0"],
        "combined": ["0"],
    },
    "spin0": {
        "bbyy":     ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"],
        "bbtautau": ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"],
        "bbbb":     ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"],
        "combined": ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"]
    }
}


for channel in CHANNELS[analysis]:
    masses = MASSES[analysis][channel]
    n_mass_per_split = len(masses)//total_split
    mass_to_run = masses[n_mass_per_split*split:n_mass_per_split*(split+1)]
    for mass in mass_to_run:
        print("INFO: Running analysis={}, channel={}, mass={}".format(analysis, channel, mass))
        ws_path = os.path.join(WS_BASE_PATH[analysis], WS_SUB_PATH[analysis][channel].format(mass=mass))
        data_name = DATASET_NAMES[dataset]
        if analysis == 'nonres':
            output_path = os.path.join(CURRENT_DIR, dataset, analysis, channel, "pulls")
        else:
            output_path = os.path.join(CURRENT_DIR, dataset, analysis, channel, mass, "pulls")
        cmd = "quickstats run_pulls -i {} -d {} -x {} -o {} --parallel 10 --cache ".format(
            ws_path, data_name, POI_NAME, output_path)
        cmd += " ".join(["--{} {}".format(k,v) for k,v in extra_options.items()])
        os.system(cmd)
        #print(cmd)
