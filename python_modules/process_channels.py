from typing import Dict, List
import sys
import os
import re
import yaml
import click

from combiner import TaskPipelineWS

kDefaultNewPOI         = "xsec_br"
kDefaultBlindDataset   = 'asimovData'
kDefaultUnblindDataset = 'obsData'
kDefaultCombDataset    = 'combData'

def process_task_config(config:Dict, channels:List, blind:bool=True):
    if config is None:
        config = {}
    poi                  = config.get('poi', {})
    dataset              = config.get('dataset', {})
    _extra_pois          = config.get('extra_pois', {})
    _rescale_poi         = config.get('rescale_poi', {})
    _define_parameters   = config.get('define_parameters', {})
    _define_constraints  = config.get('define_constraints', {})
    _add_product_terms   = config.get('add_product_terms', {})
    _redefine_parameters = config.get('redefine_parameters', {})
    _rename_parameters   = config.get('rename_parameters', {})
    _fix_parameters      = config.get('fix_parameters', {})
    _profile_parameters  = config.get('profile_parameters', {})
    
    task_config = {}
    for channel in channels:
        task_config[channel] = {}
        old_poiname = poi.get(channel, None)
        new_poiname = poi.get('combination', kDefaultNewPOI)
        channel_dataset = dataset.get(channel, {})
        comb_dataset    = dataset.get('combination', {})
        if blind:
            old_dataname = channel_dataset.get("blind", kDefaultBlindDataset)
            new_dataname = comb_dataset.get("blind", kDefaultCombDataset)
        else:
            old_dataname = channel_dataset.get("unblind", kDefaultUnblindDataset)
            new_dataname = comb_dataset.get("unblind", kDefaultCombDataset)
        extra_pois          = _extra_pois.get(channel, None)
        rescale_poi         = _rescale_poi.get(channel, None) 
        define_parameters   = _define_parameters.get(channel, None)
        define_constraints  = _define_constraints.get(channel, None)
        add_product_terms   = _add_product_terms.get(channel, None)
        redefine_parameters = _redefine_parameters.get(channel, None)
        rename_parameters   = _rename_parameters.get(channel, None)
        fix_parameters      = _fix_parameters.get(channel, None)
        profile_parameters  = _profile_parameters.get(channel, None)
        task_options = {
            "likelihood_scan": config.get('likelihood_scan', None),
            "calculate_pvalue": config.get('calculate_pvalue', None),
        }
        task_config[channel] = {
            "blind": blind,
            "old_poiname": old_poiname,
            "new_poiname": new_poiname,
            "old_dataname": old_dataname,
            "new_dataname": new_dataname,
            "extra_pois": extra_pois,
            "rescale_poi": rescale_poi,
            "define_parameters": define_parameters,
            "define_constraints": define_constraints,
            "add_product_terms": add_product_terms,
            "redefine_parameters": redefine_parameters,
            "rename_parameters": rename_parameters,
            "fix_parameters": fix_parameters,
            "profile_parameters": profile_parameters,
            "task_options": task_options
        }
    return task_config
                        
@click.command(name='process_channels')
@click.option('-i', '--input_dir', required=True, 
              help='Path to the processed workspaces.')
@click.option('-r', '--resonant_type', required=True, 
              type=click.Choice(['nonres', 'spin0'], case_sensitive=False), 
              help='Type of analysis (resonant or non-resonant).')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', show_default=True,
              help='analysis channels (separated by commas)')
@click.option('-o', '--outdir', "output_dir", default="./output", show_default=True,
              help='output directory')
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
@click.option('--blind/--unblind', default=True, show_default=True,
              help='Perform blind or unblind analysis.')
@click.option('--config', 'config_file', default=None, show_default=True,
              help='configuration file for task options')
@click.option('--minimizer_options', default=None, show_default=True,
              help='configuration file for minimizer options')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b Parallelize job across N workers.'
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
              help='Whether to use experimental method for workspace modification.')
def process_channels(**kwargs):
    
    blind       = kwargs['blind']
    channels    = kwargs['channels']
    config_file = kwargs["config_file"]
    
    if config_file is not None:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = None
  
    channels    = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
    task_config = process_task_config(config, channels, blind)
                                            
    for channel in channels:
        task_config[channel]["input_dir"]         = kwargs["input_dir"]
        task_config[channel]["output_dir"]        = kwargs["output_dir"]
        task_config[channel]["resonant_type"]     = kwargs["resonant_type"]
        task_config[channel]["channel"]           = channel
        task_config[channel]["file_expr"]         = kwargs["file_expr"]
        task_config[channel]["param_expr"]        = kwargs["param_expr"]
        task_config[channel]["filter_expr"]       = kwargs["filter_expr"]
        task_config[channel]["exclude_expr"]      = kwargs["exclude_expr"]
        task_config[channel]["minimizer_options"] = kwargs["minimizer_options"]
        task_config[channel]["verbosity"]         = kwargs["verbosity"]
        task_config[channel]["parallel"]          = kwargs["parallel"]
        task_config[channel]["cache"]             = kwargs["cache"]
        task_config[channel]["do_limit"]          = kwargs["do_limit"]
        task_config[channel]["do_likelihood"]     = kwargs["do_likelihood"]
        task_config[channel]["do_pvalue"]         = kwargs["do_pvalue"]
        task_config[channel]["experimental"]      = kwargs["experimental"]
        pipeline = TaskPipelineWS(**task_config[channel])
        pipeline.run_pipeline()
