#!/usr/bin/env bash

####################
# - SPECIFY THE `hh_combination_fw path` (MODIFY THIS TO YOUR LOCAL SETUP!)
export hh_combination_fw path="/afs/cern.ch/work/y/yuhao/public/hh_combination_fw/"

to_be_locked()
{
	set -- ""
	
	echo "Starting..."
	date
	uname -n
	
	cd ${hh_combination_fw_path}
	
	source ${hh_combination_fw_path}/setup.sh
}

job()
{
	CONFIG_FILE=$1
	
	cd ${hh_combination_fw_path}
	
	echo "Running ${hh_combination_fw_path}/scans/job_script/scan_job.py ${CONFIG_FILE}"
	${hh_combination_fw_path}/scans/job_script/scan_job.py ${CONFIG_FILE}
	
	exit 0
}

