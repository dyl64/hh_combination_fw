# Framework


## Modules

- `aux_utils`: Contains general auxiliary utility classes and functions.
 
    Examples: `job_manager` class, `mkdir_p()`

- `correlation_scheme`: Contains functions and dictionaries related to correlation scheme.
 
    Examples: `fullcorr_scheme_bbbb_bbtautau_WWyy_bbWW`, `get_same_scheme_for_all_channels()`

- `diagnostics`: Contains functions for statistical diagnostics

    Examples: `makeAsimovData()`, `runFitCrossCheck()`
 
- `fw_utils`: Contains `RooStatTools` specific utility functions
 
    Examples: `get_fullpath_dir()`, `get_fullpath_dir_fixed_prepath()`
 
- `git`: Small wrapper around `git`.

    Examples: `get_git_revision_hash_and_date()`, `get_git_revision_hash()`

- `LimitSetting`: Contains functions and data types used during the limit setting procedure.

    Examples: `runAsymptoticsCLs()`, `LimitPoint = namedtuple(..)`

- `RooStat`: Contains functions and classes interacting with `RooFit` and `RooStats`

    Examples: `GetNamesFromFile()`, `class RooArgSet`

- `scaling`: Contains the scaling factors for the different channels

    Examples: `bbbb_scalings = {}`, `get_scaling()`

- `workspaceCombiner`: Wrapper arround `workspacerCombiner`

    Examples: `generate_tokens_for_pt_config()`, `task_combination()`
