# Di-Higgs combination framework
This is the framework for di-Higgs combination.
The latest workspaces to use are documented in [HHcomb Twiki](https://twiki.cern.ch/twiki/bin/view/AtlasProtected/DiHiggsCombination).

Current relevant folders are:

    |-- scripts
    |-- hh_combination_fw
    |-- README.md
    |-- setup.sh
    |-- compile.sh
    |-- doc
    |-- submodules
        |-- RooFitExtensions
        |-- quickstats

## How to run (on lxplus)
### Check out the packages
```
git clone --recursive ssh://git@gitlab.cern.ch:7999/atlas-physics/HDBS/DiHiggs/combination/hh_combination_fw.git
```
Make sure all folders in submodules are not empty.
### For the first time (need a compilation)
```
source compile.sh
```
### Future use
```
source setup.sh
```

## To use the framework
```
### For non-resonant study
HHComb process_channels -i <input> -c <channel> -n nonres --file_expr '<mX[F]>_kl' -o <output> --config <config_file> --tasks modification,limit,significance,likelihood
HHComb combine_channels -i <output> -n nonres --file_expr '<mX[F]>_kl' -c <channel>  --config <config_file> --tasks combination,limit,significance,likelihood

### For resonant study
HHComb process_channels -i <input> -c <channel> -n spin0 --file_expr '<mX[F]>' -o <output> --config <config_file> --tasks modification,limit,significance
HHComb combine_channels -i <output> -n spin0 --file_expr '<mX[F]>' -c <channel>  --config <config_file> --tasks combination,limit,significance
```
You need to make sure the workspace with naming scheme defined via `file_expr` can be found in `<input>/<channel>/{nonres|spin0}`. The `file_expr` for non-resonant study could be changed regarding to input format, it should be `'<mX[F]>_kl_<klambda[P]>'` if the input file is `0_kl_1p0.root`. 

Attach `--unblind` in each command to analyze real data.

To consider correlation among channels, add `-s <correlation_scheme>` in the line of `HHComb combine_ws`.

The config file and correlation scheme can be found in `${hh_combination_fw_path}/configs/task_options` and `${hh_combination_fw_path}/configs/correlation_schemes` respectively.

You can specify the task option in config file to do different kind of scan, for example, you can add following lines to get two extra CLs limits.
```
tasks:
  limit:
    - scenario: nominal
      channels:
       - bbbb
       - bbtautau
       - bbyy
       - combination
    - scenario: mu_HH_ggF_limit
      channels:
       - bbyy
      options:
       poi_name: mu_HH_ggF
   - scenario: kl_scan
      channels:
       - bbyy
      options:
       poi_name: mu_HH
       param_expr: kl=-10_10_0.1
```

### Help
```
Usage: HHComb process_channels [OPTIONS]

Options:
  -i, --input_dir TEXT            Path to the input workspaces.  [required]
  -n, --analysis TEXT             Name of analysis (e.g. resonant or non-
                                  resonant).  [required]
  -c, --channels TEXT             analysis channels (separated by commas)
                                  [default: bbbb,bbtautau,bbyy]
  -o, --outdir TEXT               output directory  [default: ./output]
  --file_expr TEXT                File name expression describing the external parameterisation.
                                  Example: "<mX[F]>_kl_<klambda[P]>"
                                  Refer to documentation for more information  [default: <mX[F]>]
  --param_expr TEXT               Parameter name expression describing the internal parameterisation.
                                  Example: "klambda=-10_10_0.2,k2v=(0, 1)"
                                  Refer to documentation for more information
  -f, --filter TEXT               Filter parameter points by expression.
                                  Example: "mX=(2*,350,400,450)"
                                  Refer to documentation for more information
  -e, --exclude TEXT              Exclude parameter points by expression.
                                  Example: "mX=(2*,350,400,450)"
                                  Refer to documentation for more information
  --blind / --unblind             Perform blind or unblind analysis.
                                  [default: blind]
  --config TEXT                   configuration file for task options
  --minimizer_options TEXT        configuration file for minimizer options
  -t, --tasks TEXT                Tasks to perform (separated by commas). Available options:
                                  modification  : modify workspaces
                                  limit         : upper limit scans
                                  likelihood    : likelihood scans
                                  significance  : significance scans  [default: modification]
  --cache / --no-cache            Cache existing results.  [default: cache]
  --parallel INTEGER              Parallelize job across the N workers.
                                  Case  0: Jobs are run sequentially (for debugging).
                                  Case -1: Jobs are run across N_CPU workers.  [default: -1]
  -v, --verbosity [DEBUG|INFO|WARNING|ERROR]
                                  Verbosity level.  [default: INFO]
  --help                          Show this message and exit.
```
```
Usage: HHComb combine_channels [OPTIONS]

Options:
  -i, --input_dir TEXT            Path to the processed workspaces.
                                  [required]
  -n, --analysis TEXT             Name of analysis (e.g. resonant or non-
                                  resonant).  [required]
  -c, --channels TEXT             Channels to combine (separated by commas).
                                  [default: bbbb,bbtautau,bbyy]
  --file_expr TEXT                File name expression describing the external parameterisation.
                                  Example: "<mX[F]>_kl_<klambda[P]>"
                                  Refer to documentation for more information  [default: <mX[F]>]
  --param_expr TEXT               Parameter name expression describing the internal parameterisation.
                                  Example: "klambda=-10_10_0.2,k2v=(0, 1)"
                                  Refer to documentation for more information
  -f, --filter TEXT               Filter parameter points by expression.
                                  Example: "mX=(2*,350,400,450)"
                                  Refer to documentation for more information
  -e, --exclude TEXT              Exclude parameter points by expression.
                                  Example: "mX=(2*,350,400,450)"
                                  Refer to documentation for more information
  -s, --scheme TEXT               Configuration file for the correlation
                                  scheme.
  -t, --tag TEXT                  Pattern for the output name tag.
  --blind / --unblind             Perform blind or unblind analysis.
                                  [default: blind]
  --config TEXT                   Configuration file (yaml) for task options.
  --minimizer_options TEXT        configuration file (json) for minimizer
                                  options
  -t, --tasks TEXT                Tasks to perform (separated by commas). Available options:
                                  combination  : combine workspaces
                                  limit        : upper limit scans
                                  likelihood   : likelihood scans
                                  significance : significance scans  [default: combination]
  --cache / --no-cache            Cache existing results.  [default: cache]
  --parallel INTEGER              Parallelize job across the N workers.
                                  Case  0: Jobs are run sequentially (for debugging).
                                  Case -1: Jobs are run across N_CPU workers.  [default: -1]
  -v, --verbosity [DEBUG|INFO|WARNING|ERROR]
                                  Verbosity level.  [default: INFO]
  --help                          Show this message and exit.
```

## Plotting
Original script:
```
### For non-resonant study
python plotting/xsection/combination_plotting.py nonres  --logx --dat_list $input_dir/limits/root-files/nonres/*/*[0-9].json $input_dir/limits/root-files/nonres/combined/A-bbtautau_bbyy-fullcorr/0.json --stat $input_dir_stat/limits/root-files/nonres/*/*[0-9].json $input_dir_stat/limits/root-files/nonres/combined/A-bb*/0.json --unblind

### For resonant study
python plotting/xsection/combination_plotting.py spin0  --logx --dat_list $input_dir/limits/root-files/spin0/*/cache/*[0-9].json --com_list $input_dir/limits/root-files/spin0/combined/A-*-nocorr/cache/*[0-9].json --unblind
python plotting/pvalue/plotting_pvalue.py -i $input_dir/pvalues/ -a spin0 -o $input_dir/figures/
```
However, writing your own code in Jupyter Notebook is recommended because you can freely adjust the style according to the needs of different analyses. You can find some examples in [tutorials/HHH2022/GenPlots_new.ipynb](tutorials/HHH2022/GenPlots_new.ipynb) and [tutorials/LegacyHHResonant/tutorial.ipynb](tutorials/LegacyHHResonant/tutorial.ipynb).

## Check and download results from gitlab CI
The whole workflow is running on gitlab CI.
Go to `CI/CD > Pipelines` and click on any of the recent `passed` task, then you will see the following display:
![alt text](.CI.jpg "Title")

To check the final result, click on the `Plotting` jobs and click on the `Browser` button on the right.

You can download the whole output from the `Download` button.

## Some useful tips
### Inspect workspaces
```
quickstats inspect_ws -i <input_root_file>
```

### Generate scheme files for NP correlation
Refer to [NP_rename/README.md](NP_rename/README.md) for details.

### Run best fit on a workspace
```
quickstats likelihood_fit -i <input_root_file> --poi xsec_br --print_level 1 --strategy 1 --snapshot nominalNuis
```

### Run limit on a workspace
```
quickstats cls_limit -i <input_root_file> --poi xsec_br --print_level 1 --strategy 1 --snapshot nominalNuis
```

## Run likelihood scan
```
# 1D scan
quickstats likelihood_scan -i <input_root_file> --outdir <output_path> --param_expr "klambda=-15_20_0.2" --snapshot muhatSnapshot_kl --uncond_snapshot muhatSnapshot_kl

# 2D scan
quickstats likelihood_scan -i <input_root_file> --outdir <output_path> --param_expr "klambda=-15_20_0.2,kt=0.6_1.6_0.1" --snapshot muhatSnapshot_kl_kt --uncond_snapshot muhatSnapshot_kl_kt
```

### Generate Asimov
```
quickstats generate_standard_asimov -i <input_root_file> -o <output_path> --asimov_types 1,2,-2 --asimov_snapshots asimovtype_1_mu1_mu1,asimovtype_2_muprof_mu1,asimovtype_n2_prefit_mu1 --asimov_names combData_asimovtype_1_mu1_mu1,combData_asimovtype_2_muprof_mu1,combData_asimovtype_n2_prefit_mu1 -p xsec_br
```
You are able to generate Asimov dataset on the fly if there is a `gen_asimov` action in your config
``````
gen_asimov:
  bbll: 2,-2
  bbbb: 2,-2
  bbyy: 2,-2
  bbtautau: 2,-2
  combination: 2,-2
``````

## Run p-value
*important note*
If running on rescaled nonres workspace, require a caution on what the POI was scaled to during the rescaling step (check `regularization.yaml`, eg for Run2 CONF note, -n=0.032776 and for projection and spin0, -n=1)
```
quickstats significance_scan -i <workspace_file> -p xsec_br --mu_exp 1
```

## Run pulls (best fit), plotting and correlation matrix

```
quickstats likelihood_fit -i <workspace_file> -d combData --save_log --export_as_np_pulls
quickstats plot_pulls -i pulls/ --sigma_bands --hide_prefit --hide_postfit --theta_max 3 --padding 4 --hide_sigma  --no_sigma_lines --no_ranking_label
quickstats np_correlation -i <workspace_filename> --save_json --save_plot
```

## Run ranking and impact

Perform ranking with:
```
quickstats run_pulls --batch_mode --poi xsec_br -i <workspace_file> --parallel -1 --exclude gamma_*,nbkg_* -o <output_directory>
```
Then plot ranking plot with
- `matplotlib` shipped with LCG release is not compatible with what we need. To get a newer versioin, do
- `export PATH=/afs/cern.ch/work/c/chlcheng/public/local/conda/miniconda/envs/ml-base/bin:$PATH`
```
quickstats plot_pulls --poi xsec_br -i pulls/ --outdir rank_plot -o channel
```

## ATLAS + CMS Run 2 nonresonant combination

To setup the environment, you need to include the CMS dedicated macros in quickstats:
```
quickstats add_macro -i ${hh_combination_fw_path}/macros/CMSSWCore_HHComb
quickstats compile -m CMSSWCore_HHComb
```
These will add a bunch of files in ${hh_combination_fw_path}/submodules/quickstats/quickstats/macros/CMSSWCore_HHComb/
Note that the above code has been integrated into [compile.sh](compile.sh), so you don't need to do anything additionally.

In case of errors, try recompiling the framework:
```
source ${hh_combination_fw_path}/compile.sh
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
