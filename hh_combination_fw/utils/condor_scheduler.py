#!/usr/bin/env python

import os

def submit_job(task, job_name, task_args, log_dir):
# on lxplus, when using condor
# eos for the running dir
# afs for the log dir
# condor time limit http://batchdocs.web.cern.ch/batchdocs/tutorial/exercise6b.html
# my default setting:
# workday: 8 hours
# request_cpus: 4 (4 CPUS = 8G RAM, as 2G RAM per CPU)
# 8G is enough for 17 pts per job using popen that has mem serious leackage
    
    cmd = "condor_submit"
    config = '''
executable            = {0}
arguments             = {1}
output                = {2}/stdout.{3}
error                 = {2}/stderr.{3}
log                   = {2}/condor.{3}
request_cpus          = 4
+JobFlavour           = "workday"
queue
    '''.format( task, task_args, log_dir, job_name )

    file_sub = '{0}/condor_submit.{1}'.format(log_dir, job_name)
    with open( file_sub , 'w') as _file_sub:
        _file_sub.write( config )

    cmd = cmd + ' < ' + file_sub
    print(cmd)
    os.system( 'cat {0}'.format(file_sub) )
    print ('Condor does not support EOS for log and err. Use AFS.')
    os.system(cmd)

