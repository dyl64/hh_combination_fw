#!/usr/bin/env python

import sys
import os
import model_scan as ms


hh_combination_fw_path = os.environ['hh_combination_fw_path']

scan_run_name = "hMSSM_mA_180-600_tanb_1-5_84_by_40_bbbb_bbtautau_bbyy_200jobs_vmem_18G_with_correct_xsec"
scan_run_dir = os.path.join(hh_combination_fw_path, './scans/scan_runs/', scan_run_name )

job_manager_config_path = os.path.join(scan_run_dir, './job_manager.cfg')

failed_jobs = ms.get_failed_jobs_from_config_file_path(job_manager_config_path)
print(failed_jobs)
