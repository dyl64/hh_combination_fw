import pandas as pd
import os
import subprocess

points=pd.read_csv("scan_points.csv")
point_list=points['r_br_yy_bb']
output_dir='/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/BSM/20230912'
# masslist=[251,260,280,300,350,400,500,600,700,800,900,1000]
masslist=[450]
dirs=[output_dir+'/scanjobs',output_dir+'/BSM_limits']
for dirname in dirs:
    abs_dirname = os.path.abspath(dirname)
    if not os.path.exists(abs_dirname):
        os.makedirs(abs_dirname)
nfold=5

def writeShell(output_dir,job_name,inputfile,fold):
    fsh = open(output_dir+'/scanjobs/'+job_name+'_'+str(fold)+'.sh', 'w')
    print('Writing '+output_dir+'/scanjobs/'+job_name+'_'+str(fold)+'.sh...')
    fsh.write("#!/bin/bash\n")
    fsh.write('cd '+os.getenv('hh_combination_fw_path')+'\n')
    fsh.write('source setup.sh\n')
    npoints=len(point_list)
    npoints_fold=npoints//nfold+1
    for i_point in range(fold*npoints_fold, (fold+1)*npoints_fold):
        if(i_point>=npoints): break
        point = point_list[i_point]
        fsh.write('quickstats cls_limit --CL 0.95 -i '+inputfile+' -f br_h_bb=0.5809,r_br_yy_bb='+str(point)+',r_br_tautau_bb=0.1077 --unblind -o '+output_dir+'/BSM_limits/'+job_name+'_'+str(point)+'.txt\n')
    fsh.close()
    subprocess.check_call(["chmod","u+x",output_dir+'/scanjobs/'+job_name+'_'+str(fold)+'.sh' ])
    # subprocess.check_call(["sh",output_dir+'/scanjobs/'+job_name+'.sh'])

def writeSubmit(output_dir,job_name,fold):
    fsubmit = open(output_dir+'/scanjobs/'+job_name+'_'+str(fold)+'.submit', 'w')
    print('Writing '+output_dir+'/scanjobs/'+job_name+'_'+str(fold)+'.submit...')
    fsubmit.write("executable     = "+output_dir+'/scanjobs/'+job_name+'_'+str(fold)+".sh\n")
    fsubmit.write("output         = "+output_dir+'/scanjobs/'+job_name+'_'+str(fold)+".out\n")
    fsubmit.write("error          = "+output_dir+'/scanjobs/'+job_name+'_'+str(fold)+".error\n")
    fsubmit.write("log            = "+output_dir+'/scanjobs/'+job_name+'_'+str(fold)+".log\n")
    fsubmit.write("RequestCpus = 4\n")
    fsubmit.write("+JobFlavour = \"workday\" \n")
    fsubmit.write("queue 1 \n")
    fsubmit.close()
    print('Submitting '+output_dir+'/scanjobs/'+job_name+'_'+str(fold)+'.submit...')
    subprocess.check_call(["condor_submit", output_dir+'/scanjobs/'+job_name+'_'+str(fold)+'.submit'])

def writeSubmit_AIO(output_dir):
    fsubmit = open(output_dir+'/scanjobs/AIO.submit', 'w')
    print('Writing '+output_dir+'/scanjobs/AIO.submit...')
    fsubmit.write("executable     = $(filename)\n")
    fsubmit.write("arguments      = $(ClusterId)$(ProcId)$Fnx(filename)\n")
    fsubmit.write("output         = $(filename).out\n")
    fsubmit.write("error          = $(filename).err\n")
    fsubmit.write("log            = $(filename).log\n")
    fsubmit.write("RequestCpus = 4\n")
    fsubmit.write("+JobFlavour = \"workday\" \n")
    fsubmit.write("queue filename matching *.sh \n")
    fsubmit.close()
    print('Submitting '+output_dir+'/scanjobs/AIO.submit...')
    subprocess.check_call(["condor_submit", output_dir+'/scanjobs/AIO.submit'])



for mass in masslist:
    # inputfile=output_dir+'/combined_BSM/spin0/A-bbbb_bbtautau_bbyy-fullcorr/'+str(mass)+'.root'
    inputfile=output_dir+'/combined_BSM/spin0/A-bbtautau_bbyy-fullcorr/'+str(mass)+'.root'
    for fold in range(0,nfold):
        writeShell(output_dir,str(mass),inputfile,fold)
        # writeSubmit(output_dir,str(mass),fold)
writeSubmit_AIO(output_dir)

# for point in point_list:
    
