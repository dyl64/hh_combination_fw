from typing import Dict
import sys
import os
import yaml
import click

from combiner import TaskCombination

kDefaultPOI         = "xsec_br"
kDefaultDataset    = 'combData'

def process_task_config(config:Dict, blind:bool=True):
    if config is None:
        config = {}
    poi        = config.get('poi', {}).get("combination", kDefaultPOI)
    dataset    = config.get('dataset', {}).get("combination", {})
    extra_pois = config.get('extra_pois', {}).get("combination", None)
    
    task_config = {
        "poi_name"  : poi,
        "blind"     : blind,
        "extra_pois": extra_pois
    }
    
    if blind:
        task_config["data_name"] = dataset.get("blind", kDefaultDataset)
    else:
        task_config["data_name"] = dataset.get("unblind", kDefaultDataset)
        
    task_options = {
        "likelihood_scan": config.get('likelihood_scan', None),
        "calculate_pvalue": config.get('calculate_pvalue', None),
    }
    
    task_config["task_options"] = task_options
    
    return task_config

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
@click.option('--do-limit/--skip-limit', default=True, show_default=True,
              help='Whether to evaluate limits.')
@click.option('--do-likelihood/--skip-likelihood', default=False, show_default=True,
              help='Whether to run likelihood scan.')
@click.option('--do-pvalue/--skip-pvalue', default=False, show_default=True,
              help='Whether to evaluate pvalue(s).')
@click.option('--experimental/--official', default=False, show_default=True,
              help='Whether to use experimental method for workspace combination.')
@click.option('--prefix', 'prefix_dir', default='', show_default=True,
              help='Prefix of folders for combined workspace, limits, pvalues, and likelihood results.')
def combine_ws(**kwargs):
    
    blind       = kwargs['blind']
    channels    = kwargs['channels']
    config_file = kwargs["config_file"]
    
    if config_file is not None:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = None
        
    channels    = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
    task_config = process_task_config(config, blind)
    
    task_config["input_dir"]                   = kwargs["input_dir"]
    task_config["resonant_type"]      = kwargs["resonant_type"]
    task_config["channels"]           = kwargs['channels']
    task_config["correlation_scheme"] = kwargs['correlation_scheme']
    task_config["tag_pattern"]        = kwargs['tag_pattern']
    task_config["file_expr"]         = kwargs["file_expr"]
    task_config["param_expr"]        = kwargs["param_expr"]
    task_config["filter_expr"]       = kwargs["filter_expr"]
    task_config["exclude_expr"]      = kwargs["exclude_expr"]
    task_config["minimizer_options"] = kwargs["minimizer_options"]
    task_config["verbosity"]         = kwargs["verbosity"]
    task_config["parallel"]          = kwargs["parallel"]
    task_config["cache"]             = kwargs["cache"]
    task_config["do_limit"]          = kwargs["do_limit"]
    task_config["do_likelihood"]     = kwargs["do_likelihood"]
    task_config["do_pvalue"]         = kwargs["do_pvalue"]
    task_config["experimental"]      = kwargs["experimental"]
    task_config["prefix_dir"]      = kwargs["prefix_dir"]
    
    pipeline = TaskCombination(**task_config)
    pipeline.run_pipeline()
