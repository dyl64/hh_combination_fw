from typing import Dict, List, Optional, Union
import sys
import os
import re
import yaml
import click

from quickstats.utils.string_utils import split_str
from quickstats.utils.common_utils import combine_dict

from hh_combination_fw.core.settings import *

__all__ = ['cli']

class NaturalOrderGroup(click.Group):
    """Command group trying to list subcommands in the order they were added.

    With decorator, use::

        @click.group(cls=NaturalOrderGroup)
    """

    def list_commands(self, ctx):
        """List command names as they are in commands dict.

        If the dict is OrderedDict, it will preserve the order commands
        were added.
        """
        return self.commands.keys()

@click.group(cls=NaturalOrderGroup)
def cli():
    pass

def parse_task_options(config:Dict, channels:List[str]):
    task_options = {}
    for channel in channels:
        task_options[channel] = {}
        for task in TaskType:
            name = task.name.lower()
            task_options[channel][name] = []
    for task in TaskType:
        name = task.name.lower()
        if name not in config:
            continue
        components = config[name]
        for component in components:
            target_channels = component.get('channels', channels)
            for channel in target_channels:
                if channel not in channels:
                    continue
                options = combine_dict(component)
                options.pop('channels', None)
                task_options[channel][name].append(options)
    return task_options

def parse_task_config(config:Dict,
                      channels:List[str],
                      blind:bool=True):

    def get_channel_config(channel, attrib:str, default=None):
        if (attrib not in config) or (channel not in config[attrib]):
            return default
        return config[attrib][channel]

    channel_common_attribs = ["extra_pois"]
    task_list = [task.name.lower() for task in TaskType]
    channel_mod_attribs = list(kModificationOptionList)

    task_config = {}
    for channel in channels:
        task_config[channel] = {}
        for attrib in channel_common_attribs:
            task_config[channel][attrib] = get_channel_config(channel, attrib)
        extra_pois = get_channel_config(channel, "extra_pois")
        if extra_pois is None:
            extra_pois = []
        else:
            extra_pois = split_str(extra_pois, ',', remove_empty=True)
        task_config[channel]["extra_pois"] = extra_pois
        if channel != "combination":
            task_config[channel]["old_poi_name"] = get_channel_config(channel, "poi")
            data_name = get_channel_config(channel, "dataset", {})
            if blind:
                task_config[channel]["old_data_name"] = data_name.get("blind", kDefaultBlindDataset)
            else:
                task_config[channel]["old_data_name"] = data_name.get("unblind", kDefaultUnblindDataset)
        task_config[channel]["poi_name"] = get_channel_config("combination", "poi")
        data_name = get_channel_config("combination", "dataset", {})  
        task_config[channel]["data_name"] = data_name.get("unblind", kDefaultCombDataset)
        
        # options specific to process channels / combine channels
        if channel != "combination":
            task_config[channel]["modification_options"] = {}
            for attrib in channel_mod_attribs:
                task_config[channel]["modification_options"][attrib] = get_channel_config(channel, attrib)
        else:
            task_config[channel]["gen_asimov"] = get_channel_config(channel, "gen_asimov")
    task_options = parse_task_options(config.get("tasks", {}), channels)
    for channel in channels:
        task_config[channel]["task_options"] = task_options[channel]
    return task_config
    
def parse_cli_inputs(combination:bool=False, **kwargs):
    config_file = kwargs["config_file"]
    blind       = kwargs['blind']
    channels    = split_str(kwargs["channels"], ',', remove_empty=True)
    tasks       = split_str(kwargs["tasks"], ',', remove_empty=True)
    
    if config_file is not None:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
    else:
        config = {}

    if combination:
        task_config = parse_task_config(config, ['combination'], blind)
    else:
        task_config = parse_task_config(config, channels, blind)
        
    arg_names = ["input_dir", "output_dir", "analysis_name",
                 "file_expr", "param_expr", "filter_expr",
                 "exclude_expr", "minimizer_options",
                 "blind", "verbosity", "parallel", "cache"]
    if combination:
        arg_names.extend(['tag_pattern', 'correlation_scheme', 'useCMSOptPDF'])
    # setup configs for each channel
    for channel in task_config:
        task_config[channel]["channel"] = channel
        for name in arg_names:
            task_config[channel][name] = kwargs[name]
        task_config[channel]['tasks'] = list(tasks)

    if combination:
        task_config['combination'].pop('channel')
        task_config['combination']['channels'] = channels
        
    return task_config
                        
@cli.command(name='process_channels')
@click.option('-i', '--input_dir', required=True, 
              help='Path to the input workspaces.')
@click.option('-n', '--analysis', 'analysis_name', required=True,
              help='Name of analysis (e.g. resonant or non-resonant).')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', show_default=True,
              help='analysis channels (separated by commas)')
@click.option('-o', '--outdir', "output_dir", default="./output", show_default=True,
              help='output directory')
@click.option('--file_expr', default="<mX[F]>", show_default=True,
              help='\b\n File name expression describing the external parameterisation.'
                   '\b\n Example: "<mX[F]>_kl_<klambda[P]>"'
                   '\b\n Refer to documentation for more information')
@click.option('--param_expr', default=None, show_default=True,
              help='\b\n Parameter name expression describing the internal parameterisation.'
                   '\b\n Example: "klambda=-10_10_0.2,k2v=(0, 1)"'
                   '\b\n Refer to documentation for more information')
@click.option('-f', '--filter', 'filter_expr', default=None, show_default=True,
              help='\b\n Filter parameter points by expression.'
                   '\b\n Example: "mX=(2*,350,400,450)"'
                   '\b\n Refer to documentation for more information')
@click.option('-e', '--exclude', 'exclude_expr', default=None, show_default=True,
              help='\b\n Exclude parameter points by expression.'
                   '\b\n Example: "mX=(2*,350,400,450)"'
                   '\b\n Refer to documentation for more information')
@click.option('--blind/--unblind', default=True, show_default=True,
              help='Perform blind or unblind analysis.')
@click.option('--config', 'config_file', default=None, show_default=True,
              help='configuration file for task options')
@click.option('--minimizer_options', default=None, show_default=True,
              help='configuration file for minimizer options')
@click.option('-t', '--tasks', default='modification', show_default=True,
              help='\b\n Tasks to perform (separated by commas). Available options:'
                   '\b\n modification  : modify workspaces'
                   '\b\n limit         : upper limit scans'
                   '\b\n likelihood    : likelihood scans'
                   '\b\n significance  : significance scans')
@click.option('--cache/--no-cache', default=True, show_default=True,
              help='Cache existing results.')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b\n Parallelize job across the N workers.'
                   '\b\n Case  0: Jobs are run sequentially (for debugging).'
                   '\b\n Case -1: Jobs are run across N_CPU workers.')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
def process_channels(**kwargs):
        
    task_config = parse_cli_inputs(**kwargs)
    
    from hh_combination_fw.components import TaskProcessChannel
    for channel, config in task_config.items():
        tool = TaskProcessChannel(**config)
        tool.run_tasks()

@cli.command(name='combine_channels')
@click.option('-i', '--input_dir', required=True, 
              help='Path to the processed workspaces.')
@click.option('-n', '--analysis', 'analysis_name', required=True,
              help='Name of analysis (e.g. resonant or non-resonant).')
@click.option('-c', '--channels', default='bbbb,bbtautau,bbyy', show_default=True,
              help='Channels to combine (separated by commas).')
@click.option('--file_expr', default="<mX[F]>", show_default=True,
              help='\b\n File name expression describing the external parameterisation.'
                   '\b\n Example: "<mX[F]>_kl_<klambda[P]>"'
                   '\b\n Refer to documentation for more information')
@click.option('--param_expr', default=None, show_default=True,
              help='\b\n Parameter name expression describing the internal parameterisation.'
                   '\b\n Example: "klambda=-10_10_0.2,k2v=(0, 1)"'
                   '\b\n Refer to documentation for more information')
@click.option('-f', '--filter', 'filter_expr', default=None, show_default=True,
              help='\b\n Filter parameter points by expression.'
                   '\b\n Example: "mX=(2*,350,400,450)"'
                   '\b\n Refer to documentation for more information')
@click.option('-e', '--exclude', 'exclude_expr', default=None, show_default=True,
              help='\b\n Exclude parameter points by expression.'
                   '\b\n Example: "mX=(2*,350,400,450)"'
                   '\b\n Refer to documentation for more information')
@click.option('-s', '--scheme', 'correlation_scheme', default=None, show_default=True,
              help='Configuration file for the correlation scheme.')
@click.option('-t', '--tag', 'tag_pattern', default='{channels}-{scheme}', 
              help='Pattern for the output name tag.')
@click.option('--blind/--unblind', default=True, show_default=True,
              help='Perform blind or unblind analysis.')
@click.option('--config', 'config_file', default=None, 
              help='Configuration file (yaml) for task options.')
@click.option('--minimizer_options', default=None, show_default=True,
              help='configuration file (json) for minimizer options')
@click.option('-t', '--tasks', default='combination', show_default=True,
              help='\b\n Tasks to perform (separated by commas). Available options:'
                   '\b\n combination  : combine workspaces'
                   '\b\n limit        : upper limit scans'
                   '\b\n likelihood   : likelihood scans'
                   '\b\n significance : significance scans')
@click.option('--cache/--no-cache', default=True, show_default=True,
              help='Cache existing results.')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b\n Parallelize job across the N workers.'
                   '\b\n Case  0: Jobs are run sequentially (for debugging).'
                   '\b\n Case -1: Jobs are run across N_CPU workers.')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
@click.option('--useCMSOptPDF/--no-useCMSOptPDF', 'useCMSOptPDF', default=True, show_default=True,
              help='Use CMS Optimal PDF to make combined workspace when there is CMS workspace in inputs.')
def combine_channels(**kwargs):
    kwargs['output_dir'] = kwargs['input_dir']
    task_config = parse_cli_inputs(**kwargs, combination=True)
    
    from hh_combination_fw.components import TaskCombineChannel
    tool = TaskCombineChannel(**task_config['combination'])
    tool.run_tasks()