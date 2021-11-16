import sys
import os
import re
import yaml
import click

import combiner
import utils

DEFAULT_NEW_POI = "xsec_br"
DEFAULT_BLIND_DATASET = 'asimovData'
DEFAULT_UNBLIND_DATASET = 'obsData'
DEFAULT_COMB_DATASET = 'combData'

@click.command(name='process_channels')
@click.option('-i', '--input_dir', required=True, help='path to the input workspaces')
@click.option('-r', '--resonant_type', required=True, type=click.Choice(['nonres', 'spin0'], case_sensitive=False), 
              help='resonant or non-resonant analysis')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', help='analysis channels (separated by commas)')
@click.option('-o', '--outdir', default="./output", help='output directory')
@click.option('--better_bands/--no-better-bands', 'do_better_bands', default=True, help='do better limit bands')
@click.option('--cl', default="0.95", help='confidence level')
@click.option('--scaling_release', default="r999", help='scaling release (obselete, one should set the value by `rescale_poi` in config/regularization.yaml')
@click.option('--blind/--unblind', default=True, help='blind/unblind analysis')
@click.option('--file_expr', default="<mass[F]>", show_default=True,
              help='\b\nFile name expression describing the external parameterisation.\n'
                   '\b Example: "<mass[F]>_kl_<klambda[P]>"\n'
                   '\b Refer to documentation for more information\n')
@click.option('--param_expr', default=None, show_default=True,
              help='\b\nParameter name expression describing the internal parameterisation.\n'
                   '\b Example: "klambda=-10_10_0.2,k2v=1"\n'
                   '\b Refer to documentation for more information\n')
@click.option('--config', 'config_file', default=None, help='configuration file for regularization')
@click.option('--minimizer_options', default=None, help='configuration file for minimizer options')
@click.option('--verbose/--silent', default=False, help='show debug messages in stdout')
@click.option('--parallel', type=int, default=-1, help='number of parallelized workers')
@click.option('--cache/--no-cache', default=True, help='cache existing results')
@click.option('--save_summary/--skip_summary', default=False, help='Save summary information')
@click.option('--do-limit/--skip-limit', default=True, help='whether to evaluate limits')
def process_channels(input_dir, resonant_type, channels, outdir, do_better_bands, cl, 
                     scaling_release, blind, file_expr, param_expr, config_file,
                     minimizer_options, verbose, parallel, cache,
                     save_summary, do_limit):
    
    if config_file is not None:
        config = yaml.safe_load(open(config_file))
    else:
        config = None
    redefine_parameters = config.get('redefine_parameters', None)
    rescale_poi = config.get('rescale_poi', None)
    
    channels = channels.split(',')
    for channel in channels:
        old_poi = None if config is None else config['poi'][channel]
        new_poi = DEFAULT_NEW_POI if config is None else config['poi']['combination']
        if blind:
            old_dataname = DEFAULT_BLIND_DATASET if config is None else config['dataset'][channel]['blind']
            new_dataname = DEFAULT_COMB_DATASET if config is None else config['dataset']['combination']['blind']
        else:
            old_dataname = DEFAULT_BLIND_DATASET if config is None else config['dataset'][channel]['unblind']
            new_dataname = DEFAULT_COMB_DATASET if config is None else config['dataset']['combination']['unblind']
        if redefine_parameters is not None:
            channel_redefine_parameters = redefine_parameters.get(channel, None)
        else:
            channel_redefine_parameters = None
        if rescale_poi is not None:
            channel_rescale_poi = rescale_poi.get(channel, None)
        else:
            channel_rescale_poi = None
        pipeline = combiner.TaskPipelineWS(input_dir, outdir, resonant_type, channel, scaling_release,
                                           old_poi, new_poi, old_dataname, new_dataname, do_better_bands,
                                           cl, blind, file_expr=file_expr, param_expr=param_expr,
                                           verbose=verbose, minimizer_options=minimizer_options,
                                           redefine_parameters=channel_redefine_parameters, 
                                           rescale_poi=channel_rescale_poi,
                                           parallel=parallel, file_format=file_format, cache=cache,
                                           do_limit=do_limit)
        pipeline.run_pipeline()
