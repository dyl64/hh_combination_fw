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
@click.option('-i', '--input_dir', required=True, 
              help='Path to the processed workspaces.')
@click.option('-r', '--resonant_type', required=True, 
              type=click.Choice(['nonres', 'spin0'], case_sensitive=False), 
              help='Type of analysis (resonant or non-resonant).')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', show_default=True,
              help='analysis channels (separated by commas)')
@click.option('-o', '--outdir', default="./output", show_default=True,
              help='output directory')
@click.option('--file_expr', default="<mass[F]>", show_default=True,
              help='\b File name expression describing the external parameterisation.\n'
                   '\b Example: "<mass[F]>_kl_<klambda[P]>"\n'
                   '\b Refer to documentation for more information\n')
@click.option('--param_expr', default=None, show_default=True,
              help='\b Parameter name expression describing the internal parameterisation.\n'
                   '\b Example: "klambda=-10_10_0.2,k2v=1"\n'
                   '\b Refer to documentation for more information\n')
@click.option('--scaling_release', default="r999", show_default=True,
              help='Scaling release (obselete, one should set the value by `rescale_poi` in config/regularization.yaml')
@click.option('--better_bands/--no-better-bands', 'do_better_bands', default=True, show_default=True,
              help='Evaluate the proper +1 and +2 sigma limit bands.')
@click.option('--cl', 'CL', type=float, default=0.95, help='Confidence level.')
@click.option('--blind/--unblind', default=True, show_default=True,
              help='Perform blind or unblind analysis.')
@click.option('--config', 'config_file', default=None, show_default=True,
              help='configuration file for regularization')
@click.option('--minimizer_options', default=None, show_default=True,
              help='configuration file for minimizer options')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b Parallelize job across the N workers.'
                   '\b Case  0: Jobs are run sequentially (for debugging).\n'
                   '\b Case -1: Jobs are run across N_CPU workers.\n')
@click.option('--cache/--no-cache', default=True, show_default=True,
              help='Cache existing results.')
@click.option('--save_summary/--skip_summary', default=False, show_default=True,
              help='Save limit summary.')
@click.option('--do-limit/--skip-limit', default=True, show_default=True,
              help='Whether to evaluate limits.')
@click.option('--do-likelihood/--skip-likelihood', default=False, show_default=True,
              help='Whether to run likelihood scan.')
@click.option('--do-pvalue/--skip-pvalue', default=False, show_default=True,
              help='Whether to evaluate pvalue(s).')
def process_channels(input_dir, resonant_type, channels, outdir, file_expr, param_expr,
                     scaling_release, do_better_bands, CL, blind,
                     config_file, minimizer_options, verbosity, 
                     parallel, cache, save_summary, do_limit,
                     do_likelihood, do_pvalue):
    
    if config_file is not None:
        config = yaml.safe_load(open(config_file))
    else:
        config = None
    redefine_parameters = config.get('redefine_parameters', None)
    rescale_poi = config.get('rescale_poi', None)
    
    channels = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
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

        if config is None:
            task_options = None
        else:
            task_options = {
                "likelihood_scan": config.get('likelihood_scan', None),
                "calculate_pvalue": config.get('calculate_pvalue', None),
            }
        pipeline = combiner.TaskPipelineWS(input_dir, outdir, resonant_type, channel, scaling_release,
                                           old_poi, new_poi, old_dataname, new_dataname,
                                           redefine_parameters=channel_redefine_parameters, 
                                           rescale_poi=channel_rescale_poi,                                           
                                           file_expr=file_expr, param_expr=param_expr,
                                           do_better_bands=do_better_bands, CL=CL,
                                           blind=blind, minimizer_options=minimizer_options,
                                           verbosity=verbosity, parallel=parallel, cache=cache,
                                           save_summary=save_summary, do_limit=do_limit,
                                           do_likelihood=do_likelihood,
                                           do_pvalue=do_pvalue,
                                           task_options=task_options)
        pipeline.run_pipeline()
