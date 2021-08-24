from math import sqrt, fabs, erf
import click
import json
from quickstats.components.likelihood import evaluate_nll
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import aux_utils as utils
from itertools import repeat
from glob import glob
from pdb import set_trace

@click.command(name='pvalue')
@click.option('-i', '--input_path', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-p', '--parallel', required=False, type=int, default=-1, help='number of parallel jobs')
def pvalue(input_path, poi_name, dataset, parallel):
    input_files = []
    if input_path.endswith('.root'):
        input_files.append(input_path)
    else:
        input_files = glob(input_path + '/*.root')
    if len(input_files) == 0:
        assert(0), 'no input found'
    if parallel == -1:
        max_workers = min(multiprocessing.cpu_count(), len(input_files))
    else:
        max_workers = parallel

    arguments = (input_files, repeat(poi_name), repeat(dataset))
    utils.parallel_run(_pvalue, *arguments, max_workers=max_workers)

def _pvalue(input_file, poi_name, dataset, uncap=True):
    poi_val = 0
    nll_mu_0 = evaluate_nll(input_file, poi_val, poi_name, strategy = 1, unconditional=False, data=dataset, offset=False)
    result_free = evaluate_nll(input_file, poi_val, poi_name, strategy = 1, unconditional=True, data=dataset, offset=False, detailed_output=True)
    nll_mu_free = result_free['nll']
    poi_free = result_free['poi_bestfit']
    q0 = 2*(nll_mu_0 -nll_mu_free)

    if uncap and poi_free < 0:
        q0 = -q0
    
    sign = 0 if q0 == 0 else q0 / fabs(q0)
    q0 = fabs(q0)
    
    significance = sign*sqrt(q0)
    pvalue = (1-erf(significance/sqrt(2)))/2;
    # Equivalent to:
    # import ROOT
    # pvalue = 1-ROOT.Math.normal_cdf(sqrt(q0 ),1,0)
    # significance = ROOT.RooStats.PValueToSignificance(pvalue)
    
    dic = {
        'nll_mu_0': nll_mu_0,
        'nll_mu_free': nll_mu_free,
        'q0_orig': 2*(nll_mu_0 -nll_mu_free),
        'best_mu': poi_free,
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

