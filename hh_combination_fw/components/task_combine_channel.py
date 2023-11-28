from typing import Optional, Union, List, Dict
import os
import json

from quickstats.parsers import ParamParser
from quickstats.concurrent.logging import standard_log
from quickstats.components.workspaces import XMLWSCombiner

from hh_combination_fw.utils.combination_utils import create_combination_xml
from .task_base import TaskBase

class TaskCombineChannel(TaskBase):
    
    @property
    def correlation_scheme(self):
        return self._correlation_scheme

    @property
    def channels(self):
        return self._channels
        
    def parse_correlation_scheme(self, correlation_scheme):
        if correlation_scheme is None:
            result = None
        elif isinstance(correlation_scheme, str):
            with open(correlation_scheme, 'r') as file:
                result = json.load(file)
        elif isinstance(correlation_scheme, dict):
            result = combine_dict(correlation_scheme)
        else:
            raise ValueError('invalid format for correlation scheme')
        return result
    
    def initialize(self, **kwargs):
        tag_pattern = kwargs['tag_pattern']
        correlation_scheme = self.parse_correlation_scheme(kwargs['correlation_scheme'])
        scheme = "nocorr" if correlation_scheme is None else "fullcorr"
        channels = kwargs['channels']
        channels.sort()
        self._channels = channels
        channel_str = '_'.join(channels)
        channel = f"combined/{tag_pattern.format(channels=channel_str, scheme=scheme)}"
        super().initialize(channel=channel, **kwargs)
        self._config['tag_pattern'] = tag_pattern
        self._correlation_scheme = correlation_scheme

        # make sure the NPs are set to nominal values at the beginning
        for task in self.minimizer_options:
            self.minimizer_options[task]['snapshot_name'] = "nominalNuis"

        param_points = self.get_param_points()
        if not param_points:
            raise RuntimeError("No points to combine")
        self.stdout.info("Registered the following parameter points and corresponding "
                         "channels for combination")
        param_str_list = []
        channels_list = []
        max_len = 0
        for param_point in param_points:
            param_str = self.param_parser.val_encode_parameters(param_point['parameters'])
            max_len = max(max_len, len(param_str))
            param_str_list.append(param_str)
            channels_list.append(param_point['channels'])
        for param_str, channels in zip(param_str_list, channels_list):
            self.stdout.info(f'({param_str})'.ljust(max_len + 3) +
                             f': {channels}', bare=True)

    def sanity_check(self):
        super().sanity_check()
        for channel in self.channels:
            self.path_manager.check_directory('channel_workspace', channel=channel)
    
    def setup_paths(self, **kwargs):
        super().setup_paths(**kwargs)
        directories = {
            'channel_workspace': self.path_manager.get_channel_output_path('workspace', channel='{channel}')
        }
        self.path_manager.update_directories(directories)
   
    def get_param_points(self, filter_expr:Optional[str]=None, exclude_expr:Optional[str]=None):
        param_points = {}
        for channel in self.channels:
            dirname = self.path_manager.get_directory('channel_workspace', channel=channel)
            ext_param_points = self.param_parser.get_external_param_points(dirname,
                                                                           self.config["filter_expr"],
                                                                           self.config["exclude_expr"])
            for param_point in ext_param_points:
                filename = param_point['filename']
                basename = os.path.basename(filename)
                param_str = self.param_parser.str_encode_parameters(param_point['parameters'])
                if param_str not in param_points:
                    param_points[param_str] = {"filenames": [], "basenames": [], "channels": [],
                                               "parameters": param_point['parameters']}
                param_points[param_str]['filenames'].append(filename)
                param_points[param_str]['basenames'].append(basename)
                param_points[param_str]['channels'].append(channel)
        param_points = list(param_points.values())
        for param_point in param_points:
            basenames = param_point.pop('basenames')
            if len(set(basenames)) == 1:
                basename = basenames[0]
            else:
                basename = ParamParser.str_encode_parameters(param_point['parameters'])
            param_point['basename'] = basename
        param_points = ParamParser.sort_param_points(param_points)
        return param_points
        
    def get_combination_xml(self, param_point):
        channels  = param_point["channels"]
        filenames = param_point["filenames"]
        basename  = param_point['basename']
        channel_attributes = {}
        data_name = self.config['data_name']
        for filename, channel in zip(filenames, channels):
            channel_attributes[channel] = {}
            channel_attributes[channel]["filename"]  = filename
            channel_attributes[channel]["data_name"] = data_name
        output_ws_dir = self.path_manager.get_directory('workspace')
        output_ws_path = os.path.join(output_ws_dir, basename)
        pois_to_keep = self.get_pois_to_keep()
        poi_name = ",".join(pois_to_keep)
        xml = create_combination_xml(channel_attributes, output_ws_path, poi_name, 
                                     rename_map=self.correlation_scheme, data_name=data_name)
        return xml
        
    def create_combination_xml(self, param_point):
        xml = self.get_combination_xml(param_point)
        basename = os.path.splitext(param_point['basename'])[0]
        cfg_dir = self.path_manager.get_directory('cfg')
        filename = os.path.join(cfg_dir, f"{basename}.xml")
        xml.save(filename)
        param_str = ParamParser.val_encode_parameters(param_point['parameters'])
        self.stdout.info(f'Combination config for the point "{param_str}" saved as "{filename}"')
        
    def create_combined_ws(self, param_point):
        from quickstats.components.workspaces import XMLWSCombiner
        output_ws_dir = self.path_manager.get_directory('workspace')
        cfg_dir = self.path_manager.get_directory('cfg')
        basename = os.path.splitext(param_point['basename'])[0]
        output_ws_path = os.path.join(output_ws_dir, f"{basename}.root")
        config_path = os.path.join(cfg_dir, f"{basename}.xml")
        if self.stdout.verbosity == "DEBUG":
            output_log_path = None
        else:
            output_log_path = os.path.splitext(output_ws_path)[0] + '.log'

        if os.path.exists(output_ws_path) and self.config['cache']:
            self.stdout.info(f'Cache combined workspace "{output_ws_path}".', 'okgreen')
            return None
            
        status = 0
        self.stdout.info(f'Creating combined workspace "{output_ws_path}".')
        with standard_log(output_log_path) as logger:
            ws_combiner = XMLWSCombiner(config_path)
            ws_combiner.create_combined_workspace()
            status = 1
        if not status:
            raise RuntimeError("workspace modification failed, please check the log file for "
                               f"more details: {output_log_path}")

            self.stdout.info(f'Creating modified workspace "{output_ws_path}".')
            with standard_log(logfile_path) as logger:
                ws_combiner = XMLWSCombiner(config_file_path)
                ws_combiner.create_combined_workspace()
                status = 1
            if not status:
                raise RuntimeError("workspace combination failed, please check the log file for "
                                   f"more details: {logfile_path}")
                
    def run_combination(self, param_point):
        self.create_combination_xml(param_point)
        self.create_combined_ws(param_point)
