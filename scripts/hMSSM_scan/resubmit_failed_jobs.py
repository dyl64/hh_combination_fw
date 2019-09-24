#!/usr/bin/env python

import sys
import os
import model_scan as ms


hh_combination_fw_path = os.environ['hh_combination_fw_path']

scan_run_name = "hMSSM_mA_180-600_tanb_1-5_84_by_40_bbbb_bbtautau_bbyy_200jobs_vmem_18G_with_correct_xsec"
scan_run_dir = os.path.join(hh_combination_fw_path, './scans/scan_runs/', scan_run_name )


previous_job_manager_config_path = os.path.join(scan_run_dir, './job_manager.cfg')
new_job_manager_config_path = os.path.join(scan_run_dir,  './job_manager_resubmitted.cfg')
new_set_of_points_path = os.path.join(scan_run_dir, './resubmitted_pts.dat')

machines = "SL6@heppc300.ph.qmul.ac.uk,SL6@heppc301.ph.qmul.ac.uk,SL6@heppc302.ph.qmul.ac.uk,SL6@heppc303.ph.qmul.ac.uk,SL6@heppc400.ph.qmul.ac.uk,SL6@heppc401.ph.qmul.ac.uk,SL6@heppc402.ph.qmul.ac.uk,SL6@heppc403.ph.qmul.ac.uk,SL6@heppc404.ph.qmul.ac.uk,SL6@heppc405.ph.qmul.ac.uk,SL6@heppc406.ph.qmul.ac.uk,SL6@heppc407.ph.qmul.ac.uk,SL6@heppc500.ph.qmul.ac.uk,SL6@heppc501.ph.qmul.ac.uk,SL6@heppc502.ph.qmul.ac.uk,SL6@heppc503.ph.qmul.ac.uk,SL6@heppc504.ph.qmul.ac.uk"
resources = 'h_rss=18G,h_vmem=18G'


ms.resubmit_failed_jobs(previous_job_manager_config_path, new_job_manager_config_path,
        new_set_of_points_path, machines, resources)
