# Tests

## Limit setting

### [`./tests/test_runAsymptoticsCLs/test_getCLsLimit.sh`][test_getCLsLimit]

- Tested features:
    - Asimov limit setting, with `runAsymptoticsCLs` (c++ binary)
    - ASCII (`.dat`) and ROOT (`.root`) outputs

- Test output:
    - `./tests/test_runAsymptoticsCLs/bbbb_500_limits.root`
    - `./tests/test_runAsymptoticsCLs/bbbb_500_limits.dat`

### [`./tests/test_CalcLimit/test_CalcLimit.py`][test_CalcLimit]

- Tested features:
    - Asimov limit setting
    - python wrapper around `runAsymtptoticsCLs`
        - `LimitSetting.CalcLimit()`, `RooStatTools/bin/getLimit`.
    

- Test script: `./tests/test_CalcLimit/test_CalcLimit.py`.
- Test output:
    - `./tests/test_CalcLimit/500.0-exp.root`

## Framework pipeline (regularisation -> rescaling -> combination)


### [`./tests/test_pipeline/test_pipeline.py`][test_pipeline]

- Tested features:
    - regularisation of workspaces
    - rescaling of workspaces

- Test output:
    - `./tests/test_pipeline/test_batch/`

Note that this takes about ~3-4 minutes.

### [`./tests/test_combination/test_combination.py`][test_combination]

- Requirements:
    - Prior to running this test you need to successfully run the `test_pipeline` script, since the
        output of that script (rescaled ws-es) is the input of the combination.

- Tested features:
    - combination

- Test output:
    - `./tests/test_combination/test_combined/`
    - `./tests/test_combination/limits/`

[test_getCLsLimit]: ../tests/test_runAsymptoticsCLs/test_getCLsLimit.sh
[test_CalcLimit]: ../tests/test_CalcLimit/test_CalcLimit.py
[test_pipeline]: ../tests/test_pipeline/test_pipeline.py
[test_combination]: ../tests/test_combination/test_combination.py
