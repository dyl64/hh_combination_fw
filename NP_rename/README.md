# NP harmonisation

This folder contains sources to generate `schemes` used in the combination step.
Example commands to create the JSON scheme files are:
```
quickstats harmonize_np -i NP_rename/input_list_nonres.json -r NP_rename/reference_list_v2.json -b ../input/20210531/ -o configs/np_map_nonres_v1.json
quickstats harmonize_np -i NP_rename/input_list_spin0.json -r NP_rename/reference_list_v2.json -b ../input/20210531/ -o configs/np_map_spin0_v1.json
```

The outputs are used to generate the XML card via `--scheme` option in `HHComb combine_ws`, eg
```
HHComb combine_ws --new_method -i ../output -r nonres -c bbbb,bbtautau,bbyy --scheme config/np_map_nonres_v1.json
```
Default is no correlation.
