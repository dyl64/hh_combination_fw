# Di-Higgs combination framework
This is the framework for di-Higgs combination.
The latest workspaces to use are documented in [HHcomb Twiki](https://twiki.cern.ch/twiki/bin/view/AtlasProtected/DiHiggsCombination).

Current relevant folders are:

    |-- scripts
    |-- python_modules
    |-- README.md
    |-- setup.sh
    |-- compile.sh
    |-- doc
    |-- submodules
        |-- RooFitExtensions
        |-- workspaceCombiner
        |-- quickstats

Caveats:
- Currently stuck at some commit on workspaceCombiner:development branch.
## How to run (on lxplus)
### Check out the packages
```
git clone --recursive ssh://git@gitlab.cern.ch:7999/atlas-physics/HDBS/DiHiggs/combination/hh_combination_fw.git
```
Make sure all folders in submodules are not empty.
### Patch `workspaceCombiner`
The dataset name is not customisable in `workspaceCombiner` and the [TList indexing bug](https://indico.cern.ch/event/1025636/contributions/4311962/attachments/2222485/3763797/HHcomb20210408.pdf) needs a fix.
Apply the patch:
```
cd submodules/workspaceCombiner
git apply --whitespace=nowarn ../../workspaceCombiner.patch
```
### For the first time (need a compilation)
```
source compile.sh
source setup.sh
HHComb process_channels -i <input> -c <channel> -r nonres -o <output> --config configs/regularization_nonres_v3.yaml
...
HHComb combine_ws -i <output> -c bbbb,bbtautau,bbyy,WWWW,bbll,bbVV
...

```
You need to make sure the workspace can be found in `<input>/<channel>/nonres`.

### For the future time
```
source setup.sh
HHComb process_channels -i <input> -c <channel> -r nonres -o <output> --config configs/regularization_nonres_v3.yaml
...
HHComb combine_ws -i <output> -c bbbb,bbtautau,bbyy,WWWW,bbll,bbVV
...
```

### Plotting
Plot for non-resonant and spin0:
```
# export PATH=/afs/cern.ch/work/c/chlcheng/public/local/conda/miniconda/envs/ml-base/bin:$PATH
python plotting/xsection/combination_plotting.py nonres  --logx --dat_list $input_dir/limits/root-files/nonres/*/*[0-9].json $input_dir/limits/root-files/nonres/combined/A-bbtautau_bbyy-fullcorr/0.json --stat $input_dir_stat/limits/root-files/nonres/*/*[0-9].json $input_dir_stat/limits/root-files/nonres/combined/A-bb*/0.json --unblind

python plotting/xsection/combination_plotting.py spin0  --logx --dat_list $input_dir/limits/root-files/spin0/*/*[0-9].json --com_list $input_dir/limits/root-files/spin0/combined/A-*-nocorr/*[0-9].json --unblind

```
## Check and download results from gitlab CI
The whole workflow is running on gitlab CI.
Go to `CI/CD > Pipelines` and click on any of the recent `passed` task, then you will see the following display:
![alt text](.CI.jpg "Title")

To check the final result, click on the `Plotting` jobs and click on the `Browser` button on the right.

You can download the whole output from the `Download` button.

## Run kappa-lambda xsec scan (on individual input workspaces, with names `0_kl_1p0.root`, `0_kl_n1p0.root`)
To run xsec limit for each kl value, two input formats are supported.
The first format is a workspace file per each kl value.
This is useful when channels do not have parametrised single workspace.
```
# HHComb process_channels -i ~/work/HHcomb/FullRun2Workspaces/original/20210922/ -o output_directory_v4 -r nonres -c bbtautau  --config configs/regularization_nonres_v6_mH125p09.yaml --file_format "<mass[F]>_kl_1p0" --unblind

HHComb process_channels -i <input_ws_directory> -o <output_directory> -r nonres -c bbyy,bbtautau --minimizer_options configs/minimizer_options_robust.json --config configs/regularization_nonres_v6_mH125.yaml --file_format "<mass[F]>_kl_<kl[P]>" --unblind

HHComb combine_ws -i <output_directory> -r nonres -c bbyy,bbtautau --minimizer_options configs/minimizer_options_robust.json --scheme configs/np_map_kl_v10.json --file_format "<mass[F]>_kl_<kl[P]>" --unblind
```

## Run kappa-lambda xsec scan (on parametrised input workspaces, with a name `0_kl.root`)
```
The second format is more preferred that has a single workspace with `klambda` as an additional POI.
Following is to run the combination on this format.
HHComb process_channels -i <input_ws_directory> -c bbyy,bbtautau  -r nonres --minimizer_options configs/minimizer_options_robust.json --config configs/regularization_kl.yaml --skip-limit --no-cache --file_format "<mass[F]>_kl" -o <output_directory>

HHComb combine_ws -i <output_directory> -r nonres -c bbyy,bbtautau --minimizer_options configs/minimizer_options_robust.json --config configs/regularization_kl.yaml --scheme configs/np_map_kl_v10.json --file_format "<mass[F]>_kl" --skip-limit --no-cache

```

## Run kappa-lambda likelihood scan (on parametrised input workspaces, with a name `0_kl.root`)
```
HHComb process_channels -i <input_ws_directory> -c bbyy -r nonres --minimizer_options configs/minimizer_options_robust.json --config configs/regularization_kl.yaml --skip-limit --no-cache --file_format "<mass[F]>_kl" --param_expr "klambda=-10_10_0.2" -o <output_directory>

HHComb combine_ws -i <output_directory> -r nonres -c bbyy,bbtautau --minimizer_options configs/minimizer_options_robust.json --scheme configs/np_map_kl_v10.json --param klambda=<-low>_<high>_<step> --file_format "<mass[F]>_kl" --param_expr "klambda=-10_10_0.2"

HComb kl_likelihood -i <output_directory> -c bbyy,bbtautau --min=-2 --max=10 --step=0.2 --no-cache
python likelihood_plotting.py -a nonres -i <output_directory>/output/likelihood/ -c combined_klambda.json -t bbtautau_klambda.json -y bbyy_klambda.json -o <output_directory>/figure --threshold 12
```

## Run pulls and impact

Perform ranking with:
```
quickstats run_pulls --batch_mode --poi xsec_br -i <workspace_file> --parallel -1 --exclude gamma_*,nbkg_* -o <output_directory>
```
Then plot ranking plot with
- `matplotlib` shipped with LCG release is not compatible with what we need. To get a newer versioin, do
- `export PATH=/afs/cern.ch/work/c/chlcheng/public/local/conda/miniconda/envs/ml-base/bin:$PATH`
```
quickstats plot_pulls --style trex --poi xsec_br -i pulls/ -o rank_plot
```

## Run pulls and impact in batch
```
cd NP_ranking
# if you want to generate an asimov instead of using obs (for nonres it is true due to deficit of bbyy obs)
source get_profiled_asimov.sh

# run all pulls
python run_ranking.py nonres <input_folder>

# harmonise NP names for individual channels to match the combined
python harmonise_name.py nonres <input_folder>
```

## Run p-value
*important note*
If running on rescaled nonres workspace, require a caution on what the POI was scaled to during the rescaling step (check `regularization.yaml`, eg for Run2 CONF note, -n=0.032776 and for projection and spin0, -n=1)
```
# 
HHComb pvalue -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210924_CI/output/combined/spin0/A-bbbb_bbtautau_bbyy-fullcorr/1100.root
## to run all *.root files in parallel:
HHComb pvalue -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210924_CI/output/combined/spin0/A-bbbb_bbtautau_bbyy-fullcorr
```
To run expected p-value (but profiled to obs data):
```
## (obselete) profile NP to POI=0 or 1 or float (-1), then generate asimov; then set the global observable to the fitted NP values and calculate the pvalue
#HHComb pvalue -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output/combined/spin0/A-bbbb_bbtautau_bbyy-fullcorr --expected [0|1]

# use type=2 to profile best-fit NPs with POI floated and generate asimov; then load the best-fit NP values to globs via `conditionalGlobs_None` and calculate p-value
quickstats generate_standard_asimov -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210924_CI/output_mu_unblind/rescaled/nonres/bbtautau/0.root -o /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210924_CI/output_mu_unblind/rescaled/nonres/bbtautau/asimov2_0.root --poi xsec_br --poi_scale 0.032776 --asimov_types 2
HHComb pvalue -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210924_CI/output_mu_unblind/rescaled/nonres/bbtautau/asimov2_0.root -d asimovData_muhat_NP_Profile  -s conditionalGlobs_None
```
To run blinded p-value:
```
HHComb pvalue -i ../output/v3000invfb_20211106_CI/NR/rescaled/nonres/bbyy/0.root --blind
```

## Quick fit
```
# useful to use -d <dataset> -s <snapshot> on profiled asimov to load globs
HHComb best_fit -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output/combined/spin0/A-bbbb_bbtautau_bbyy-fullcorr/0.root -d <dataset> -s <snapshot>
```

## Run likelihood scan
```
cd v140invfb_20210821_CI/output
mkdir likelihood_scan
quickstats likelihood_scan --min -0.2 --max 1.0 --step 0.01 -i combined/spin0/A-bbbb_bbtautau_bbyy-fullcorr/<Mass>.root -o <Mass>
```

## Generate scheme files for NP correlation

Refer to [NP_rename/README.md](NP_rename/README.md) for details.


## Some useful tips
### Run limit on a workspace
```
quickstats cls_limit --batch_mode -i <input_root_file> --poi xsec_br --print_level 1 --strategy 1 --snapshot nominalNuis
```

### Inspect workspaces
```
quickstats inspect_ws -i <input_root_file>
```

### Generate Asimov
CLI tool (if you check `python_modules/gen_asimov.py`, two asimov workspaces will be created:
- POI=0, do_conditional=True:
- POI=1, do_conditional=True:
```
HHComb gen_asimov -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output_unblind/combined/nonres/A-bbtautau_bbyy-fullcorr/0.root
HHComb gen_asimov -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output_unblind/combined/nonres/A-bbtautau_bbyy-fullcorr/
```

</p>
</details>
<details><summary>Old README</summary>
<p>
## Description

A python and C++ based software framework developed for the di-Higgs combination effort.

**Features:**
- Regularisation of [`RooFit::RooWorkspaces`][RooWorkspace] (workspaces), i.e. standardising the
    workspace, modelconfig, datanames.
- Rescaling of workspaces
    - specifying custom scaling factors for each production mode, channel and mass point
- Combination of workspaces
    - combine multiple workspaces at once
    - specifying custom correlations schemes
- Calculating limits
    - expected and/or observed
    - nominal and/or profiled NPs
- Parallel processing with the `multiprocessing` module.
- Scans in models with varying branching fractions (e.g. hMSSM)

Studies on the combined results (model intrepretation, sanity checks, etc.) is maintained in a
separate repository at:
- https://gitlab.cern.ch/atlasHBSM/atlas-phys-higgs-dihiggs-combteam/hh_studies

**For any questions please contact:**
- david.englert@cern.ch

## Dependencies

- [`ROOT`][ROOT]
- [`workspaceCombiner`][workspaceCombiner]
    - `boost`
- `python`
- `gcc/g++`

The framework also have the following packages as `git` `submodules`:
- [`RooStatTools`][RooStatTools]
- [`ModelTools`][ModelTools]
- [`PhysicsLib`][PhysicsLib]
- [`UtilTools`][UtilTools]

These packages should be automatically checked out if you are cloning with the `--recursive` flag
(see below for setup instructions).

## Setup instructions

Please see detailed setup instructions in [./doc/setup.md](./doc/setup.md).

## Usage instructions

### Tests

Reference test scripts can be found in the `./tests/` directory.
Documentation of the tests: [./doc/tests.md][tests]

### Scripts

Live scripts use for the combination can be found in the [`./scripts`](./scripts) directory.
Please do not edit these scripts, but use these as a template for your own ones.

- [`./scripts/pipeline/processChannels.py`](./scripts/pipeline/processChannels.py): Handles the regularisation and rescaling of the
    workspaces. Please [see the associated documentation here.][processChannels_doc]
- [`./scripts/combination/auto/combine_ws.py`](./scripts/combination/auto/combine_ws.py): Combines the workspaces.
    Please [see the associated documentation here.][combine_ws_doc]
- [`./scripts/hMSSM_scan/setup_scan.py`](./scripts/hMSSM_scan/setup_scan.py),
    [`./scripts/hMSSM_scan/pool_processed_scan_pts.py`](./scripts/hMSSM_scan/pool_processed_scan_pts.py),
    model scan example scripts. Please [see the associated documentation here.][model_scan_doc]

### UNIX style commands

Such as `quickLimit`, `wscontent`, `runNPranking`.
More info within [RootStatTools command documentation](https://gitlab.cern.ch/atlasHBSM/atlas-phys-higgs-dihiggs-combteam/RooStatTools/blob/master/doc/cmd/commands.md)

### Naming conventions for input/output

The framework uses some conventions for the naming of the input workspaces, to identify the
production mode, channels, mass points, which you can find here:
[./doc/conventions.md][conventions].

## Combination details

Please [find the details of the combination here.][combination_details]

## Model scans

Please [see the associated documentation here.][model_scan_doc]

### hMSSM

Associated scripts:
- [`./scripts/hMSSM_scan/setup_scan.py`](./scripts/hMSSM_scan/setup_scan.py)
- [`./scripts/hMSSM_scan/pool_processed_scan_pts.py`](./scripts/hMSSM_scan/pool_processed_scan_pts.py)

### Singlet model

Done in jupyter notebooks (to be uploaded later on).

## Documentation

You can find more documentation on the package [`./doc`](./doc) folder.


[combination_details]: ./doc/combination_details.md
[tests]: ./doc/tests.md
[hh_combination_fw]: https://gitlab.cern.ch/atlasHBSM/atlas-phys-higgs-dihiggs-combteam/hh_combination_fw
[workspaceCombiner]: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner
[workspaceCombiner_install]: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner#Installation
[workspaceCombiner_combination]: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner#Workspace_combination
[ROOT]: https://root.cern.ch/ 
[RooWorkspace]: https://root.cern.ch/doc/master/classRooWorkspace.html
[RooStatTools]: https://gitlab.cern.ch/atlasHBSM/atlas-phys-higgs-dihiggs-combteam/RooStatTools
[ModelTools]: https://gitlab.cern.ch/atlasHBSM/atlas-phys-higgs-dihiggs-combteam/ModelTools
[UtilTools]: https://gitlab.cern.ch/atlasHBSM/atlas-phys-higgs-dihiggs-combteam/UtilTools
[PhysicsLib]: https://gitlab.cern.ch/atlasHBSM/atlas-phys-higgs-dihiggs-combteam/PhysicsLib
[how_to_update]: ./doc/for_analysis_contacts.md
[conventions]: ./doc/conventions.md
[processChannels_doc]: ./doc/processChannels.md
[combine_ws_doc]: ./doc/combine_ws.md
[model_scan_doc]: ./doc/model_scan.md

</p>
</details>
