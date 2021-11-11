import json
from math import sqrt, fabs, erf
import quickstats
from quickstats.components import AnalysisBase

def _pvalue(delta_nll, poi_free, uncap, output_file='pvalue.json'):
    q0 = 2*delta_nll

    if uncap and poi_free < 0:
        q0 = -q0

    sign = 0 if q0 == 0 else q0 / fabs(q0)
    q0 = fabs(q0)

    significance = sign*sqrt(q0)
    pvalue = (1-erf(significance/sqrt(2)))/2;

    dic = {
        'q0_orig': 2*delta_nll,
        'best_mu': poi_free,
        'q0': q0,
        'pvalue': pvalue,
        'significance': significance
        }
    with open(output_file, 'w') as f:
        json.dump(dic, f, indent=4)
    print('Save to', output_file)
    print(dic)


#fname = "../../output/v3000invfb_20211106_CI/NR/regularised/nonres/bbtautau/0.root"
#fname2 = "../../output/v3000invfb_20211106_CI/NR/rescaled/nonres/bbtautau/0.root"
#fname = "../../output/v3000invfb_20211106_CI/NR/regularised/nonres/bbyy/0.root"
#fname2 = "../../output/v3000invfb_20211106_CI/NR/rescaled/nonres/bbyy/0.root"
fname = "../../output/v3000invfb_20211106_CI/NR/combined/nonres/A-bbtautau_bbyy-fullcorr/0.root"



analysis = AnalysisBase(fname, data_name="combData", config={"snapshot_name":"nominalNuis"})
analysis.generate_standard_asimov(quickstats.AsimovType.S_NP_Nom)
analysis.model.workspace.writeToFile('temp_combined.root')
analysis.set_data("asimovData_1_NP_Nominal")
nll = analysis.evaluate_nll(poi_val = 0, mode=0)
poi_free = analysis.poi.getVal()
analysis.model.workspace.writeToFile('temp_combined.root')

#analysis2 = AnalysisBase(fname2, data_name="combData", config={"snapshot_name":"nominalNuis"})
#analysis2.generate_standard_asimov(quickstats.AsimovType.S_NP_Nom)
#analysis2.set_data("asimovData_1_NP_Nominal")
#nll2 = analysis2.evaluate_nll(poi_val = 0, mode=0)
#print('regular', nll)
#print('rescale', nll2)
#poi_free2 = analysis2.poi.getVal()
uncap = True

# Write out results next to the input file
_pvalue(nll, poi_free, uncap, )
#_pvalue(nll2, poi_free2, uncap,)

