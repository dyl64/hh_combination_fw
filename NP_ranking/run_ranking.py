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

dataset = "profiled_asimov_data" if analysis == 'nonres' else "observed_data"
profiled_snapshot = 'conditionalGlobs_0.032776' if analysis == 'nonres' else ''

extra_options = {
    "exclude": "\"gamma_*,nbkg*,BKG*,xi*,ATLAS_norm*,NORM_*\"",
#    "fix": "\"THEO_XS_fixmu_*=0, alpha_THEO_XS_PDFalphas_VBFSMHH=0,"
#           " alpha_THEO_XS_PDFalphas_ggFSMHH=0, alpha_THEO_XS_SCALEMTop_ggFSMHH=0,"
#           " THEO_XS_COMBINED_HH_ggF=0, THEO_XS_PDFalphas_HH_VBF=0,"
#           " THEO_XS_PDFalphas_HH_ggF=0, THEO_XS_SCALE_HH_VBF=0\""
}

POI_NAME = "xsec_br"
DATASET_NAMES = {
    "observed_data": "combData",
    "asimov_data": "asimovData_1_None",
    "profiled_asimov_data": "cond_1_asimov_1",
}
WS_BASE_PATH = {
    "nonres": "/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/",
    "spin0": "/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210903_CI/output/"
}

CURRENT_DIR = 'NP_ranking'

WS_SUB_PATH = {
    "nonres": {
        "bbyy": "rescaled/nonres/bbyy/cond_1_asimov_1.{mass}.root",
        "bbtautau": "rescaled/nonres/bbtautau/cond_1_asimov_1.{mass}.root",
        "bbbb": "rescaled/nonres/bbbb/cond_1_asimov_1.{mass}.root",
        "combined": "combined/nonres/A-bbtautau_bbyy-fullcorr/cond_1_asimov_1.{mass}.root"
    },
    "spin0": {
        "bbyy": "rescaled/spin0/bbyy/{mass}.root",
        "bbtautau": "rescaled/spin0/bbtautau/{mass}.root",
        "bbbb": "rescaled/spin0/bbbb/{mass}.root",
        "combined": "combined/spin0/A-bbbb_bbtautau_bbyy-fullcorr/{mass}.root"
    }
}
CHANNELS = {
    "nonres": ["bbyy", "bbtautau", "combined"],
    "spin0": ["combined", "bbbb", "bbtautau", "bbyy"]
}
MASSES = {
    "nonres":{
        "bbyy": ["0"],
        "bbtautau": ["0"],
        "combined": ["0"],
    },
    "spin0": {
        "bbyy":     ["300", "500", "1000"],
        "bbtautau": ["300", "500", "1000"],
        "bbbb":     ["300", "500", "1000"],
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
            output_path = os.path.join(WS_BASE_PATH[analysis], CURRENT_DIR, dataset, analysis, channel, "pulls")
        else:
            output_path = os.path.join(WS_BASE_PATH[analysis], CURRENT_DIR, dataset, analysis, channel, mass, "pulls")
        cmd = "quickstats run_pulls -i {} -d {} -x {} -o {} --parallel 10 --cache --batch_mode ".format(
            ws_path, data_name, POI_NAME, output_path)
        cmd += " ".join(["--{} {}".format(k,v) for k,v in extra_options.items()])
        if analysis == 'nonres':
            cmd += ' -s {}'.format(profiled_snapshot)
        #os.system(cmd)
        print(cmd)
