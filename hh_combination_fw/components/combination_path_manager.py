from typing import Optional, Union, Dict, List, Tuple
import os

from quickstats import PathManager
from quickstats.utils.common_utils import combine_dict

class CombinationPathManager(PathManager):

    DEFAULT_FILES = {
        "likelihood_output"   : ("likelihood", "likelihoods_{poi_names}.json"),
        "limit_output"        : ("limit", "limits_{poi_name}.json"),
        "significance_output" : ("significance", "significance_{param_names}.json")
    }

    DEFAULT_OUTPUT_TYPES = ["workspace", "limit", "likelihood", "significance",
                            "ranking", "plot", "cfg"]
    
    def __init__(self, analysis_name:str, channel:str,
                 input_dir:Optional[str]=None,
                 output_dir:Optional[str]=None,
                 extra_output_types:Optional[List[str]]=None):

        super().__init__()
        self.set_analysis_name(analysis_name, False)
        self.set_channel(channel, False)
        self.set_io_dir(input_dir, output_dir, False)
        self.set_extra_output_types(extra_output_types, False)
        self.update()

    def get_channel_input_path(self):
        return os.path.join(self.input_dir, self.channel, self.analysis_name)

    def get_channel_output_path(self, output_type:str, channel:Optional[str]=None):
        if channel is None:
            channel = self.channel
        return os.path.join(self.output_dir, output_type, self.analysis_name, channel)
        
    def update(self):
        directories = {
            'input_ws': self.get_channel_input_path()
        }
        output_types = list(self.DEFAULT_OUTPUT_TYPES) + list(self.extra_output_types)
        for output_type in output_types:
            directories[output_type] = self.get_channel_output_path(output_type)
        self.update_directories(directories)
        files = combine_dict(self.DEFAULT_FILES)
        self.update_files(files)
        
    def set_analysis_name(self, analysis_name:str, update:bool=True):
        self.analysis_name = analysis_name
        if update:
            self.update()
        
    def set_channel(self, channel:str, update:bool=True):
        self.channel = channel
        if update:
            self.update()

    def set_io_dir(self, input_dir:str, output_dir:str, update:bool=True):
        if input_dir is None:
            input_dir = os.getcwd()
        if output_dir is None:
            output_dir = os.getcwd()
        self.input_dir  = os.path.abspath(input_dir)
        self.output_dir = os.path.abspath(output_dir)
        if update:
            self.update()

    def set_extra_output_types(self, extra_output_types:Optional[List[str]]=None,
                               update:bool=True):
        if extra_output_types is None:
            extra_output_types = []
        self.extra_output_types = list(extra_output_types)
        if update:
            self.update