import os
import json

dataset = "observed_data"

np_map = {
    "nonres": "/Users/zhangrui//Work/Code/HHcomb/hh_combination_fw/configs/np_map_nonres_v4.json",
    "spin0": "/Users/zhangrui//Work/Code/HHcomb/hh_combination_fw/configs/np_map_spin0_v5.json"
}

CURRENT_DIR = os.getcwd()
OUTNAME = {
    "nonres": "NP_ranking_nonres_{channel}",
    "spin0": "NP_ranking_spin0_{channel}_{mass}"}
POI_NAME = "xsec_br"

ANALYSES = ["nonres", "spin0"]


CHANNELS = {
    "nonres": ["bbyy", "bbtautau"],
    "spin0": ["bbbb", "bbtautau", "bbyy"]
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

from pdb import set_trace
for analysis in ANALYSES:
    rename_map = json.load(open(np_map[analysis], 'r'))
    for channel in CHANNELS[analysis]:
        for mass in MASSES[analysis][channel]:
            if analysis == "nonres":
                input_path = os.path.join(CURRENT_DIR, dataset, analysis, channel, "pulls")
                for k, v in rename_map[channel].items():
                    if k == v: continue
                    old_name = f'{input_path}/{k}.json'
                    try:
                        cmd = f'sed -i -- s/{k}/{v}/g {old_name}'
                        #print(cmd)
                        os.system(cmd)
                    except:
                        pass
            else:
                input_path = os.path.join(CURRENT_DIR, dataset, analysis, channel, mass, "pulls")
                for k, v in rename_map[channel].items():
                    if k == v: continue
                    old_name = f'{input_path}/{k}.json'
                    try:
                        cmd = f'sed -i -- s/{k}/{v}/g {old_name}'
                        #print(cmd)
                        os.system(cmd)
                    except:
                        pass
