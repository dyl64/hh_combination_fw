from pdb import set_trace
import os, glob, sys

id='7005995'
if len(sys.argv) > 1:
    id=str(sys.argv[1])
    print('test', sys.argv[1])
files = glob.glob(f'log/*/{id}*.err')
failed_jobs = []
for name in files:
    file_size = os.stat(name).st_size
    if file_size > 0:
        with open(name.replace('err', 'out')) as f:
            lines = [i for i in f.readlines() if 'quickstats' in i]
            print(name, lines[0])

            jobs = lines[0].split(' ')
            job = jobs[1]
            key = jobs.index('--param_expr')
            poi = jobs[key+1]
            key = jobs.index('--data')
            dataset = jobs[key+1]
            try:
                key = jobs.index('--input_path')
            except:
                key = jobs.index('--input_file')
            pat = jobs[key+1].split('/')
            chanel = pat[-2]
            folder = pat[-5]
            failed_jobs.append([chanel, folder, poi, dataset])

jdls = glob.glob('job_HHH_quick_*.jdl')
all_lines = []

for jdl in jdls:
    with open(jdl) as f:
        all_lines.extend([i for i in f.readlines() if 'quickstats' in i])

lines = []
for job in failed_jobs:
    lines.extend([i for i in all_lines if '/'+job[0]+'/' in i and job[1] in i and job[2] in i and job[3] in i])
    print([i for i in all_lines if '/'+job[0]+'/' in i and job[1] in i and job[2] in i and job[3] in i])
    #print(job)
assert(len(failed_jobs) == len(lines)), f'{len(failed_jobs)}, {len(lines)}'

for i in failed_jobs:
    print(i)
print()

log_folder = 'llh' if 'likelihood_scan' in lines[0] else 'xsec'
header=f'''#Agent jdl file
Universe        = vanilla
Notification    = Never
initialdir      = /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/condor
Executable      = /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/condor/wrapper_HHH_quick.sh
GetEnv          = True
Error           = /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/condor/log/{log_folder}/$(ClusterId).$(ProcId).err
Log             = /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/condor/log/{log_folder}/$(ClusterId).log
Output          = /afs/cern.ch/user/z/zhangr/work/HHcomb/hh_combination_fw/hh_combination_fw/condor/log/{log_folder}/$(ClusterId).$(ProcId).out
stream_output   = False
stream_error    = False
Requirements = ((Arch == "X86_64") && (regexp("CentOS7",OpSysAndVer)))
WhenToTransferOutput = ON_EXIT_OR_EVICT
OnExitRemove         = TRUE
+JobFlavour = "tomorrow"
+JobType="analysis"
+AccountingGroup ="group_u_ATLASWISC.all"
RequestCpus = 6
Request_memory = 4000 MB
Request_disk   = 4000 MB



'''

set_trace()
original_stdout = sys.stdout
sys.stdout = open(f'{id}.jdl', 'w')
print(header)
for i in lines:
    print(i)
    print('Queue 1')
sys.stdout = original_stdout
