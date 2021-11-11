import json
from pdb import set_trace
import click
from math import sqrt, fabs, erf
import quickstats
from quickstats.components import AnalysisBase

@click.command(name='pvalue_new')
@click.option('-i', '--input_file', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-o', '--output', required=False, default=None, help='file to store asimov')
def pvalue_new(input_file, poi_name, dataset, output):
    uncap=True
    
    analysis = AnalysisBase(input_file, data_name=dataset, config={"snapshot_name":"nominalNuis"})
    analysis.generate_standard_asimov(quickstats.AsimovType.S_NP_Nom)
    if output:
        analysis.model.workspace.writeToFile(output)
    analysis.set_data("asimovData_1_NP_Nominal")
    nll = analysis.evaluate_nll(poi_val = 0, mode=0)
    poi_free = analysis.poi.getVal()
    
    # Write out results next to the input file
    output_file = input_file[::-1].replace('.root'[::-1], '_pvalue_expblind.json'[::-1], 1)[::-1]
    set_trace()
    _pvalue(nll, poi_free, uncap, output)

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
