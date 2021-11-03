import sys
import os
import re
import yaml
import click

import combiner

DEFAULT_POI = "xsec_br"
DEFAULT_DATASET = 'combData'

@click.command(name='combine_ws')
@click.option('-i', '--input_path', required=True, help='path to the processed workspaces')
@click.option('-r', '--resonant_type', required=True, type=click.Choice(['nonres', 'spin0'], case_sensitive=False), 
              help='resonant or non-resonant analysis')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', help='channels combine')
@click.option('-s', '--scheme', 'correlation_scheme', default=None, help='path to the json file containing the correlation scheme')
@click.option('-t', '--tag', 'tag_pattern', default='A-{channels}-{scheme}', help='pattern for the output name tag')
@click.option('--better_bands/--no-better-bands', 'do_better_bands', default=True, help='do better limit bands')
@click.option('--cl', default="0.95", help='confidence level')
@click.option('--blind/--unblind', default=True, help='blind/unblind analysis')
@click.option('-m', '--mass',  'mass_expr', default=None, help='mass points to run, wild card is accepted, default=None (all mass points)')
@click.option('-p', '--param',  default=None, help='perform limit scan on parameterized workspace on a certain parameter(s)'
                                             ', e.g. klambda=-10_10_0.2,cvv=1')
@click.option('--config', 'config_file', default=None, help='configuration file for regularization')
@click.option('--minimizer_options', default=None, help='configuration file for minimizer options')
@click.option('--verbose/--silent', default=False, help='show debug messages in stdout')
@click.option('--parallel', type=int, default=-1, help='number of parallelized workers')
@click.option('--file_format', default="<mass[F]>", help='file format')
@click.option('--cache/--no-cache', default=True, help='cache existing results')
@click.option('--do-limit/--skip-limit', default=True, help='whether to evaluate limits')
def combine_ws(input_path, resonant_type, channels, correlation_scheme, tag_pattern, 
               do_better_bands, cl, blind, mass_expr, param, config_file, 
               minimizer_options, verbose, parallel, file_format, cache, do_limit):
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
    pipeline = combiner.TaskCombination(input_path, resonant_type, channels, poi_name, data_name, correlation_scheme,
                                        tag_pattern, do_better_bands, cl, blind, mass_expr, param, 
                                        verbose=verbose, 
                                        minimizer_options=minimizer_options,
                                        parallel=parallel,
                                        file_format=file_format,
                                        cache=cache,
                                        do_limit=do_limit)
    pipeline.run_pipeline()

    
