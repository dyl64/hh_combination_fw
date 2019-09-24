#!/usr/bin/env python

import sys
import os
import csv
import model_scan as ms

print("Running {}".format(sys.argv[0]))
hh_combination_fw_path = os.environ['hh_combination_fw_path']
model = 'hMSSM'

#scan_run_name = 'hMSSM_mA_180-600_tanb_1-4_100_by_100'
#scan_run_name = 'hMSSM_mA_180-600_tanb_1-5_84_by_40_bbbb_bbtautau_bbyy_200jobs_vmem_18G'
#scan_run_name = 'hMSSM_mA_180-600_tanb_1-5_84_by_40_bbbb_bbtautau_200jobs_vmem_18G_with_correct_xsec'
#scan_run_name = 'hMSSM_mA_180-600_tanb_1-5_84_by_40_bbbb_bbtautau_bbyy_200jobs_vmem_18G_with_correct_xsec'
scan_run_name = '2018_06_06_hMSSM_mA_180-600_tanb_1-5_84_by_40_bbbb_bbtautau_bbyy_200jobs_vmem_18G_with_correct_xsec_updated_NP_corr'


scan_run_dir = os.path.join(hh_combination_fw_path, './scans/scan_runs', scan_run_name)
scan_manager_cfg = os.path.join(scan_run_dir, 'job_manager.cfg')

model_scan_mgr = ms.model_scan_manager.from_manager_config(scan_manager_cfg)
model_scan_mgr.pool_results()

