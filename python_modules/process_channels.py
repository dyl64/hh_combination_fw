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
@click.option('-r', '--resonant_type', required=True, type=click.Choice(['nonres', 'spin0'], case_sensitive=False), 
              help='resonant or non-resonant analysis')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', help='analysis channels (separated by commas)')
@click.option('-o', '--outdir', default="./output", help='output directory')
@click.option('--better_bands/--no-better-bands', 'do_better_bands', default=True, help='do better limit bands')
@click.option('--cl', default="0.95", help='confidence level')
@click.option('--scaling_release', default="r03", help='scaling release')
@click.option('--blind/--unblind', default=True, help='blind/unblind analysis')
@click.option('-n', 'n_proc', type=int, default=16, help='number of concurrent processes')
@click.option('-m', '--mass', 'mass_expr', default=None, help='mass points to run, wild card is accepted, default=None (all mass points)')
@click.option('-p', '--param',  default=None, help='perform limit scan on parameterized workspace on a certain parameter(s)'
                                             ', e.g. klambda=-10_10_0.2,cvv=1')
@click.option('--new_method/--old_method', default=False, help='use quickstats for asymptotic cls limit')
@click.option('--config', 'config_file', default=None, help='configuration file for regularization')
@click.option('--minimizer_options', default=None, help='configuration file for minimizer options')
@click.option('--verbose/--silent', default=False, help='show debug messages in stdout')
def process_channels(input_path, resonant_type, channels, outdir, do_better_bands, cl, 
                     scaling_release, blind, n_proc, mass_expr, param, new_method, config_file,
                     minimizer_options, verbose):
    
    if config_file is not None:
        config = yaml.safe_load(open(config_file))
    else:
        config = None
        
    channels = channels.split(',')
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
        pipeline = wsc.TaskPipelineWS(workspace_dir, outdir, resonant_type, channel, scaling_release,
                                      old_poi, new_poi, old_dataname, new_dataname, do_better_bands,
                                      cl, blind, mass_expr, param, new_method=new_method,
                                      verbose=verbose, minimizer_options=minimizer_options)

        pipeline.run_pipeline()
