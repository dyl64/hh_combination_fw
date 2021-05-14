import sys
import os
import re
import yaml
import click

import workspaceCombiner as wsc
import aux_utils as utils

DEFAULT_NEW_POI = "xsec_br"
DEFAULT_BLIND_DATASET = 'asimovData'
DEFAULT_UNBLIND_DATASET = 'obsData'
DEFAULT_COMB_DATASET = 'combData'

@click.command(name='process_channels')
@click.option('-i', '--input_path', required=True, help='path to the input workspaces')
@click.option('-r', '--resonant_type', default='nonres', help='resonant or non-resonant analysis')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', help='analysis channels (separated by commas)')
@click.option('-o', '--output_path', default="./output", help='output directory')
@click.option('--better_bands/--no-better-bands', 'do_better_bands', default=True, help='do better limit bands')
@click.option('--cl', default="0.95", help='confidence level')
@click.option('--scaling_release', default="r02", help='scaling release')
@click.option('--blind/--unblind', default=True, help='blind analysis')
@click.option('-n', 'n_proc', type=int, default=16, help='number of concurrent processes')
@click.option('--param',  default=None, help='perform limit scan on parameterized workspace on a certain parameter(s)'
                                             ', e.g. klambda=-10_10_0.2,cvv=1')
@click.option('--config', 'config_file', default=None, help='configuration file for regularization')
def process_channels(input_path, resonant_type, channels, output_path, do_better_bands, 
                     cl, scaling_release, blind, n_proc, param, config_file):
    task_list = []
    channels = channels.split(',')
    if config_file is not None:
        config = yaml.safe_load(open(config_file))
    else:
        config = None
    for channel in channels:
        workspace_dir = os.path.join(input_path, channel, resonant_type)
        old_poi = None if config is None else config['poi'][channel]
        new_poi = DEFAULT_NEW_POI if config is None else config['poi']['combination']
        if blind:
            old_dataname = DEFAULT_BLIND_DATASET if config is None else config['dataset'][channel]['blind']
            new_dataname = DEFAULT_COMB_DATASET if config is None else config['dataset']['combination']['blind']
        else:
            old_dataname = DEFAULT_BLIND_DATASET if config is None else config['dataset'][channel]['unblind']
            new_dataname = DEFAULT_COMB_DATASET if config is None else config['dataset']['combination']['unblind']            
        task = (workspace_dir, output_path, resonant_type, channel, scaling_release, old_poi,
                new_poi, old_dataname, new_dataname, do_better_bands, 
                cl, blind, param)
        task_list.append(task)
        
    if param is not None:
        # forcing parallelization across parameterization instead of channels
        for task in task_list:
            wsc.task_pipeline_ws(task)
    else:
        manager = utils.job_manager(func=wsc.task_pipeline_ws, nProc=n_proc)
        manager.set_task_args(task_list)
        manager.submit()


