from math import sqrt, fabs, erf
import click
import json
from quickstats.components.likelihood import evaluate_nll

@click.command(name='pvalue')
@click.option('-i', '--input_file', required=True, help='path to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='path to the processed workspaces')
@click.option('-d', '--dataset', required=False, default='combData', help='path to the processed workspaces')
def pvalue(input_file, poi_name, dataset):
    poi_val = 0
    nll_mu_free = evaluate_nll(input_file, poi_val, poi_name , unconditional=True, data=dataset)
    nll_mu_0 = evaluate_nll(input_file, poi_val, poi_name , unconditional=False, data=dataset)
    q0 = 2*(nll_mu_0 -nll_mu_free)
    
    sign = 0 if q0 == 0 else q0 / fabs(q0)
    q0 = fabs(q0)
    
    significance = sign*sqrt(q0)
    pvalue = (1-erf(significance/sqrt(2)))/2;
    # Equivalent to:
    # pvalue = 1-ROOT.Math.normal_cdf(sqrt(q0 ),1,0)
    # significance = ROOT.RooStats.PValueToSignificance(pvalue)
    
    dic = {
        'nll_mu_0': nll_mu_0,
        'nll_mu_free': nll_mu_free,
        'q0': q0,
        'pvalue': pvalue,
        'significance': significance
        }
    # Write out results next to the input file
    output_file = input_file[::-1].replace('.root'[::-1], '_pvalue.json'[::-1], 1)[::-1]
    with open(output_file, 'w') as f:
        json.dump(dic, f, indent=4)
    print('Save to', output_file)
    print(dic)
