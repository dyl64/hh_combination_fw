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

@click.command(name='best_fit')
@click.option('-i', '--input_path', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-p', '--parallel', required=False, type=int, default=-1, help='number of parallel jobs')
@click.option('-s', '--snapshot', required=False, type=str, default=None, help='number of parallel jobs')
def best_fit(input_path, poi_name, dataset, parallel, snapshot):
    input_files = []
    if input_path.endswith('.root'):
        input_files.append(input_path)
    else:
        input_files = glob(input_path + '/*[0-9].root')
    if len(input_files) == 0:
        assert(0), 'no input found'
    if parallel == 0:
        for input_file in input_files:
            _best_fit(input_file, poi_name, dataset, snapshot)
    else:
        if parallel == -1:
            max_workers = min(multiprocessing.cpu_count(), len(input_files))
        else:
            max_workers = parallel

        arguments = (input_files, repeat(poi_name), repeat(dataset), repeat(snapshot))
        utils.parallel_run(_best_fit, *arguments, max_workers=max_workers)

def _best_fit(input_file, poi_name, dataset, snapshot, uncap=True):
    poi_val = 0
    result_free = evaluate_nll(input_file, poi_val, poi_name, strategy = 1, print_level = 1, unconditional=True, data=dataset, offset=False, detailed_output=True, snapshot=snapshot)
    nll_mu_free = result_free['nll']
    poi_free = result_free['poi_bestfit']

    dic = {
        'best_mu': poi_free,
        }
    print(dic)

