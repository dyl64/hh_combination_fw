#!/usr/bin/env python

import os
import LimitSetting as ls

hh_combination_fw_path = os.environ['hh_combination_fw_path']

pt = 500.0
input_workspace = os.path.join(hh_combination_fw_path, './tests/reference_workspaces/bbbb/spin0/500.root')
output_limit_dir = os.path.join(hh_combination_fw_path, './tests/test_getLimit/')
exp_or_obs = 'exp'
doBetterBands = 'false'
dataName = 'obsData'
asimovDataName = 'combined'
CL = 0.95

ls.CalcLimit(pt, input_workspace, output_limit_dir, exp_or_obs, doBetterBands, dataName, asimovDataName, CL)
