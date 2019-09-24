#!/usr/bin/env python

import sys
import os
import csv
import model_scan as ms
import aux_utils as utils
import shell as sh

print("Running {}".format(sys.argv[0]))
hh_combination_fw_path = os.environ['hh_combination_fw_path']
model = 'hMSSM'

scan_run_name = 'hMSSM_mA_180-600_tanb_1-4_100_by_100'
original_workspaces_dir = '/.data/englert/projects/hh_combination/workspaces/2017_11_27/rescaled/spin0/'
scan_run_dir = os.path.join(hh_combination_fw_path, './scans/scan_runs', scan_run_name)
job_task_path = os.path.join(hh_combination_fw_path, './scans/job_script/task_with_lock.sh')

scan_points_path = os.path.join(hh_combination_fw_path, './submodules/ModelTools/ascii/hMSSM_scan_pts_mA_180-600_tanb_1-4_100_by_100.dat')

machines = "SL6@heppc300.ph.qmul.ac.uk,SL6@heppc301.ph.qmul.ac.uk,SL6@heppc302.ph.qmul.ac.uk,SL6@heppc303.ph.qmul.ac.uk,SL6@heppc400.ph.qmul.ac.uk,SL6@heppc401.ph.qmul.ac.uk,SL6@heppc402.ph.qmul.ac.uk,SL6@heppc403.ph.qmul.ac.uk,SL6@heppc404.ph.qmul.ac.uk,SL6@heppc405.ph.qmul.ac.uk,SL6@heppc406.ph.qmul.ac.uk,SL6@heppc407.ph.qmul.ac.uk,SL6@heppc500.ph.qmul.ac.uk,SL6@heppc501.ph.qmul.ac.uk,SL6@heppc502.ph.qmul.ac.uk,SL6@heppc503.ph.qmul.ac.uk,SL6@heppc504.ph.qmul.ac.uk"

# job_options = {'resources': 'h_rss=12G,h_vmem=12G'}
resources = 'h_rss=15G,h_vmem=15G'
#resources = None

model_scan_mgr = ms.model_scan_manager(
                                      scan_run_dir = scan_run_dir,
                                      model = 'hMSSM',
                                      type = 'spin0',
                                      channels = ['bbbb', 'bbtautau'],
                                      scan_points_path = scan_points_path,
                                      original_workspaces_dir = original_workspaces_dir,
                                      nJobs = 500,
                                      job_options = {'resources': resources, 'machines': machines},
                                      job_task_path = job_task_path,
                                      correlation_scheme_version = 'fullcorr',
                                      init=True
                                      )

model_scan_mgr.append_with_mass_pt_neighbours()
model_scan_mgr.distribute_scan_pts_among_jobs()
model_scan_mgr.write_process_pts_list()
model_scan_mgr.submit_jobs_sge()
