from math import sqrt, fabs, erf
import click
import json
from quickstats.components import ExtendedModel
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import aux_utils as utils
from itertools import repeat
from glob import glob
from os import path
from pdb import set_trace

@click.command(name='gen_asimov')
@click.option('-i', '--input_path', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-p', '--parallel', required=False, type=int, default=-1, help='number of parallel jobs')
def gen_asimov(input_path, poi_name, dataset, parallel):
    input_files = []
    if input_path.endswith('.root'):
        input_files.append(input_path)
    else:
        input_files = glob(input_path + '/[0-9]*[0-9].root')
    if len(input_files) == 0:
        assert(0), 'no input found'
    if parallel == -1:
        max_workers = min(multiprocessing.cpu_count(), len(input_files))
    else:
        max_workers = parallel

    if len(input_files) == 1: # disable multiprocessing for debugging
        for input_file in input_files:
            _asimov(input_file, dataset)
    else:
        arguments = (input_files, repeat(dataset))
        utils.parallel_run(_asimov, *arguments, max_workers=max_workers)

def _asimov(input_file, dataset):

    # settings for asimov ('poi_profile', 'profile', 'poi_val')
    # if profile = True, asimov dataset will be generated with the profiled NP when POI taking poi_profile, and set the POI to poi_val after fit.
    settings = [
        #[1, True],  # for pvalue and significance calculation
        [1, False],  # for ranking plot S+B asimov
        ]
    for setting in settings:
        if len(setting) == 2: setting.append(setting[0])
        model = ExtendedModel(input_file, data_name=dataset)
        model.generate_asimov(poi_name="xsec_br", poi_val = setting[0], poi_profile = setting[2], do_conditional = setting[1], do_import=True, object_names={'asimov': 'asimovData_{mu}_'+str(setting[1])})
        model.workspace.writeToFile(path.dirname(input_file) + f'/asimov{setting[0]}_{setting[1]}.' + path.basename(input_file))
