import os
import sys
from pdb import set_trace

if sys.argv[1] not in ['nonres', 'spin0']:
    print('Usage: python', sys.argv[0], 'nonres|spin0', '0|1|2')
    exit()
if sys.argv[1] == 'spin0' and sys.argv[2] not in ['0', '1', '2']:
    print('Usage: python', sys.argv[0], 'nonres|spin0', '0|1|2')
    exit()

dataset = "asimov_data"

CURRENT_DIR = os.getcwd() + '/../../NP_ranking/'
OUTNAME = {
    "nonres": "NP_ranking_nonres_{channel}",
    "spin0": "NP_ranking_spin0_{channel}_{mass}"}
POI_NAME = "xsec_br"

ANALYSES = ["nonres", "spin0"] if len(sys.argv) == 1 else [sys.argv[1]]

CHANNELS = {
    "nonres": ["bbyy", "bbtautau", "combined"],
    "spin0": ["bbbb", "bbtautau", "bbyy", "combined"]
}
MASSES = {
    "nonres":{
        "bbyy": ["0"],
        "bbtautau": ["0"],
        "bbbb": ["0"],
        "combined": ["0"],
    },
    "spin0": {
        "bbyy":     ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"],
        "bbtautau": ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"],
        "bbbb":     ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"],
        "combined": ["251", "260", "280", "300", "350", "400", "500", "600", "700", "800", "900", "1000"]
    }
}


for analysis in ANALYSES:
    for channel in CHANNELS[analysis]:
        for mass in MASSES[analysis][channel]:
            print("INFO: Plotting analysis={}, channel={}, mass={}".format(analysis, channel, mass))
            if analysis == "nonres":
                input_path = os.path.join(CURRENT_DIR, dataset, analysis, channel, "pulls")
                outdir = os.path.join(CURRENT_DIR, dataset, analysis, channel, "plots")
            else:
                input_path = os.path.join(CURRENT_DIR, dataset, analysis, channel, mass, "pulls")
                outdir = os.path.join(CURRENT_DIR, dataset, analysis, channel, mass, "plots")
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            outname = OUTNAME[analysis].format(channel=channel, mass=mass)
            outpath = os.path.join(outdir, outname)
            cmd = "quickstats plot_pulls -i {} -p {} -o {}".format(input_path, POI_NAME, outpath)
            #os.system(cmd)
            print(cmd)
