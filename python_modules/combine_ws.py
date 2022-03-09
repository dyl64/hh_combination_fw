import sys
import os
import re
import yaml
import click

import combiner

DEFAULT_POI = "xsec_br"
DEFAULT_DATASET = 'combData'

@click.command(name='combine_ws')
@click.option('-i', '--input_dir', required=True, 
              help='Path to the processed workspaces.')
@click.option('-r', '--resonant_type', required=True, 
              type=click.Choice(['nonres', 'spin0'], case_sensitive=False), 
              help='Type of analysis (resonant or non-resonant).')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', show_default=True,
              help='Channels to combine (separated by commas).')
@click.option('--file_expr', default="<mass[F]>", show_default=True,
              help='\b File name expression describing the external parameterisation.\n'
                   '\b Example: "<mass[F]>_kl_<klambda[P]>"\n'
                   '\b Refer to documentation for more information\n')
@click.option('--param_expr', default=None, show_default=True,
              help='\b Parameter name expression describing the internal parameterisation.\n'
                   '\b Example: "klambda=-10_10_0.2,k2v=1"\n'
                   '\b Refer to documentation for more information\n')
@click.option('-f', '--filter', 'filter_expr', default=None, show_default=True,
              help='\b Filter parameter points by expression.\n'
                   '\b Example: "mass=2*,350,400,450;klambda=1.*,2.*,-1.*,-2.*"\n'
                   '\b Refer to documentation for more information\n')
@click.option('-e', '--exclude', 'exclude_expr', default=None, show_default=True,
              help='\b Exclude parameter points by expression.\n'
                   '\b Example: "mass=2*,350,400,450;klambda=1.*,2.*,-1.*,-2.*"\n'
                   '\b Refer to documentation for more information\n')
@click.option('-s', '--scheme', 'correlation_scheme', default=None, show_default=True,
              help='Configuration file for the correlation scheme.')
@click.option('-t', '--tag', 'tag_pattern', default='A-{channels}-{scheme}', 
              help='Pattern for the output name tag.')
@click.option('--better_bands/--no-better-bands', 'do_better_bands', default=True, show_default=True,
              help='Evaluate the proper +1 and +2 sigma limit bands.')
@click.option('--cl', 'CL', type=float, default=0.95, help='Confidence level.')
@click.option('--blind/--unblind', default=True, show_default=True,
              help='Perform blind or unblind analysis.')
@click.option('--config', 'config_file', default=None, 
              help='Configuration file (yaml) for task options.')
@click.option('--minimizer_options', default=None, show_default=True,
              help='configuration file (json) for minimizer options')
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
def combine_ws(input_dir, resonant_type, channels, file_expr, param_expr,
               filter_expr, exclude_expr,
               correlation_scheme, tag_pattern, do_better_bands, CL, blind,
               config_file, minimizer_options, verbosity, parallel, cache,
               save_summary, do_limit, do_likelihood, do_pvalue):
    
    if config_file is not None:
        config = yaml.safe_load(open(config_file))
    else:
        config = None
        
    channels = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
    poi_name = DEFAULT_POI if config is None else config['poi']['combination']
    if blind:
        data_name = DEFAULT_DATASET if config is None else config['dataset']['combination']['blind']
    else:
        data_name = DEFAULT_DATASET if config is None else config['dataset']['combination']['unblind']
        
    if config is None:
        task_options = None
    else:
        task_options = {
            "likelihood_scan": config.get('likelihood_scan', None),
            "calculate_pvalue": config.get('calculate_pvalue', None),
        }        
        
    pipeline = combiner.TaskCombination(input_dir, resonant_type, channels, poi_name, data_name,
                                        correlation_scheme, tag_pattern, 
                                        file_expr=file_expr, param_expr=param_expr,
                                        do_better_bands=do_better_bands, CL=CL,
                                        blind=blind, minimizer_options=minimizer_options,
                                        verbosity=verbosity, parallel=parallel, cache=cache,
                                        save_summary=save_summary, do_limit=do_limit,
                                        do_likelihood=do_likelihood,
                                        do_pvalue=do_pvalue,
                                        task_options=task_options,
                                        filter_expr=filter_expr,
                                        exclude_expr=exclude_expr)
    pipeline.run_pipeline()

    
