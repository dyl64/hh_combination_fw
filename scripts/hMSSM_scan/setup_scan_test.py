#!/usr/bin/env python

import sys
import os
import csv
import model_scan as ms
import aux_utils as utils
#import shell as sh

print("Running {}".format(sys.argv[0]))
hh_combination_fw_path = os.environ['hh_combination_fw_path']
model = 'hMSSM'

scan_run_name = 'hMSSM_test'
original_workspaces_dir = '/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/output/rescaled/spin0/'
scan_run_dir = os.path.join(hh_combination_fw_path, './scans/scan_runs', scan_run_name)
job_task_path = os.path.join(hh_combination_fw_path, './scans/job_script/task_with_lock.sh')

scan_points_path = os.path.join(hh_combination_fw_path, './scripts/hMSSM_scan/hMSSM_scan_point_test.dat')


# job_options = {'resources': 'h_rss=12G,h_vmem=12G'}
resources = 'h_rss=15G,h_vmem=15G'
#resources = None

model_scan_mgr = ms.model_scan_manager(
                                      scan_run_dir = scan_run_dir,
                                      model = 'hMSSM',
                                      type = 'spin0',
                                      channels = ['bbbb','bbtautau'],
                                      scan_points_path = scan_points_path,
                                      original_workspaces_dir = original_workspaces_dir,
                                      nJobs = 5,
                                      job_options={},
                                      job_task_path = job_task_path,
                                      correlation_scheme_version = 'nocorr',
                                      init=True
                                      )

model_scan_mgr.append_with_mass_pt_neighbours()
model_scan_mgr.distribute_scan_pts_among_jobs()
model_scan_mgr.write_process_pts_list()
model_scan_mgr.submit_jobs_condor()
