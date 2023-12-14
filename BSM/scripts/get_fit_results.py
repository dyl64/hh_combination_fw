import pandas as pd
import json

points=pd.read_csv("scan_points.csv")
point_list=points['r_br_yy_bb']
# masslist=[251,260,280,300,350,400,500,600,700,800,900,1000]
masslist=[450]
output = open("summary1017.txt","w")
print("mass,r_br_yy_bb,exp_limit,obs_limit",file=output)
for mass in masslist:
    for point in point_list:
        filename=str(mass)+"_"+str(point)+".txt"
        filepath="/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/BSM/20230912/BSM_limits/"+filename
        with open(filepath, "r") as f:
                result = json.load(f)
                exp=result['0']
                obs=result['obs']
                print("%d,%.4f,%f,%f"%(mass,point,exp,obs),file=output)

output.close()