# NP harmonisation

This folder contains sources to generate `schemes` used in the combination step.
Example commands to create the JSON scheme files are:
```
quickstats harmonize_np -i NP_rename/input_list_nonres.json -r NP_rename/reference_list_v2.json -b <ws_input> -o configs/np_map_nonres_v1.json
# e.g.
quickstats harmonize_np -i NP_rename/input_list_nonres.json -r NP_rename/reference_list_v5.json -o configs/np_map_nonres_v5.json -b /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/original/20210914/

quickstats harmonize_np -i NP_rename/input_list_spin0.json -r NP_rename/reference_list_v2.json -b <ws_input> -o configs/np_map_spin0_v1.json
# e.g.
quickstats harmonize_np -i NP_rename/input_list_spin0.json -r NP_rename/reference_list_v5.json -o configs/np_map_spin0_v6.json -b /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/original/20210914/
```

The outputs are used to generate the XML card via `--scheme` option in `HHComb combine_ws`, eg
```
HHComb combine_ws --new_method -i ../output -r nonres -c bbbb,bbtautau,bbyy --scheme config/np_map_nonres_v1.json
```
Default is no correlation.


## History:
- Current default (20210903)
    - `configs/np_map_spin0_v5.json`, `configs/np_map_spin0_v5_FTcor.json`, `configs/np_map_nonres_v4.json`
    - Decorrelated ATLAS_EG_SCALE_ALL by hand
    - Decorrelated `_FTcor` 4b by hand
    - `PS` HH is decorrelated

- `configs/np_map_spin0_v5.json`, `configs/np_map_spin0_v5_FTcor.json`, `configs/np_map_nonres_v3.json`
    - Correlate single Higgs uncertainties
    - Add `"Lumi": "fix_Lumi"` for bbbb by hand (?)


- `configs/np_map_spin0_v4.json`, `configs/np_map_spin0_v4_FTcor.json`, `configs/np_map_nonres_v3.json` (20210723)
    - Generated from `NP_rename/reference_list_v4.json`
    - Correlate theory uncertainties
    - Included `_FTcor` version for Spin0 for study while the nominal is uncorrelated due to different NP schemes implemented in 4b.

- `configs/np_map_spin0_v3.json, configs/np_map_nonres_v2.json`
    - EPS21 bbtautau final ws, draft 1 4b ws (hand editing for TFag decorrelation of 4b due to its unique loose scheme)
    - Generated from `NP_rename/reference_list_v3.json`

- `configs/np_map_spin0_v2.json, configs/np_map_nonres_v1.json`
    - Draft 1 bbtautau and Moriond bbyy, draft 1 4b resonant (for combination EB request 09.07.2021)
