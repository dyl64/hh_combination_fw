from typing import Optional, List, Dict, Union
import os
import uuid
import fnmatch

from quickstats import semistaticmethod
from quickstats.utils.common_utils import combine_dict
from quickstats.components import ExtendedModel
from quickstats.components.workspaces import XMLWSModifier, XMLWSBase
from quickstats.concurrent.logging import standard_log

from hh_combination_fw.core.settings import *
from .task_base import TaskBase, TaskType

class TaskProcessChannel(TaskBase):

    @property
    def modification_options(self):
        return self._modification_options
    
    def initialize(self, channel:str,
                   old_poi_name:str,
                   old_data_name:str,
                   modification_options:Optional[Dict]=None,
                   **kwargs):
        super().initialize(channel=channel, **kwargs)
        self._config['old_poi_name'] = old_poi_name
        self._config['old_data_name'] = old_data_name
        self._modification_options = self.parse_modification_options(modification_options)

    @semistaticmethod
    def parse_modification_options(self, options:Optional[Dict]=None):
        options = combine_dict(options)
        for option_name in kModificationOptionList:
            if option_name not in options:
                options[option_name] = None
        return options
        
    def sanity_check(self):
        super().sanity_check()
        self.path_manager.check_directory('input_ws')

    def get_param_points(self):
        dirname = self.path_manager.get_directory('input_ws')
        param_points = self.param_parser.get_param_points(dirname,
                                                          self.config["filter_expr"],
                                                          self.config["exclude_expr"])
        return param_points

    def get_modification_config(self, input_filename:str,
                                output_filename:str):
        config = {
            "input_file"  : input_filename,
            "output_file" : output_filename,
        }

        config["poi_names"] = self.get_pois_to_keep()
        
        modification_options = self.modification_options
        action_config = {
            "redefine"   : [],
            "define"     : [],
            "rename"     : {},
            "constraint" : []
        }
        # rename workspace
        action_config["rename"]["workspace"] = {None: kCombWSName}
        # rename dataset
        data_name = self.config["data_name"]
        old_data_name = self.config["old_data_name"]
        action_config["rename"]["dataset"] = {old_data_name: data_name}
        action_config["rename"]["variable"] = {}
        
        # rename and rescale poi
        poi_name = self.config["poi_name"]
        old_poi_name = self.config["old_poi_name"]
        if modification_options['rescale_poi'] is None:
            poi_scale = 1.0
        else:
            poi_scale = modification_options['rescale_poi']
        if isinstance(poi_scale, dict):
            basename = os.path.basename(input_filename)
            if basename in poi_scale:
                poi_scale = poi_scale[basename]
            else:
                keys = list(poi_scale)
                matched_keys = [key for key in keys if fnmatch.fnmatch(basename, str(key))]
                if len(matched_keys) == 0:
                    poi_scale = 1.0
                elif len(matched_keys) == 1:
                    poi_scale = poi_scale[matched_keys[0]]
                else:
                    raise RuntimeError(f'found multiple matched keys for the rescale_poi options: {matched_keys}')
                
        # need to check the default value and range of the poi
        model = ExtendedModel(input_filename, data_name=None, verbosity="WARNING")
        poi = model.get_poi(old_poi_name)
        if not poi:
            raise RuntimeError(f'the workspace "{input_filename}" does not contain the parameter "{old_poi_name}"')
        old_poi_name = poi.GetName()
        old_poi_val = poi.getVal()
        new_poi_val = old_poi_val / poi_scale
        old_poi_min = poi.getRange()[0]
        old_poi_max = poi.getRange()[1]
        if abs(old_poi_min) > 1e10:
            new_poi_min = old_poi_min
        else:
            new_poi_min = old_poi_min / poi_scale
        if abs(old_poi_max) > 1e10:
            new_poi_max = old_poi_max
        else:
            new_poi_max = old_poi_max / poi_scale

        redefine_parameters = modification_options['redefine_parameters']
        if redefine_parameters is not None:
            if isinstance(redefine_parameters, dict):
                for name, val in redefine_parameters.items():
                    redef_expr = f"{name}[{val}]"
                    action_config["redefine"].append(redef_expr)
            elif isinstance(redefine_parameters, list):
                for expr in redefine_parameters:
                    action_config["redefine"].append(expr)
            else:
                raise RuntimeError("invalid redefine parameter options")
                
        define_parameters = modification_options["define_parameters"]
        if define_parameters is not None:
            for expr in define_parameters:
                action_config["define"].append(expr)                

        if kRescaledOldPOIName == poi_name:
            raise ValueError(f'can not define poi name as "{kRescaledOldPOIName}" which is a reserved name')
        poi_expr_1 = f"{poi_name}[{new_poi_val}, {new_poi_min}, {new_poi_max}]"
        poi_expr_2 = f"expr::{kRescaledOldPOIName}('@0/{poi_scale}', {poi_name})"
        # put the define of poi at the end to not override custom defines
        action_config["define"].append(poi_expr_1)
        action_config["define"].append(poi_expr_2)
        action_config["rename"]["variable"][old_poi_name] = kRescaledOldPOIName

        define_constraints = modification_options["define_constraints"]
        if define_constraints is not None:
            for constr_dict in define_constraints:
                action_config["constraint"].append(constr_dict)
        add_product_terms = modification_options["add_product_terms"]
        if add_product_terms is not None:
                action_config["add_product_terms"] = add_product_terms
        rename_parameters = modification_options["rename_parameters"]
        if rename_parameters is not None:
            for old_name, new_name in rename_parameters.items():
                action_config["rename"]["variable"][old_name] = new_name

        config["actions"] = action_config
        for option in ["fix_parameters",
                       "profile_parameters",
                       "set_parameters"]:
            config[option] = modification_options[option]
        return config

    def run_asimov(self,outfile:str,asimov_types:str):
        from quickstats.components import AsimovGenerator
        from quickstats.utils.string_utils import split_str
        generator = AsimovGenerator(outfile, poi_name=self.config["poi_name"],
                                    data_name=self.config["data_name"])
        try:
            asimov_types = split_str(asimov_types, sep=",", cast=int)
        except Exception:
            asimov_types = split_str(asimov_types, sep=",")
        generator.generate_standard_asimov(asimov_types)
        generator.save(outfile, rebuild=True)

    def run_modification(self, param_point:Dict):
        input_ws_path = param_point['filename']
        basename = os.path.basename(input_ws_path)
        output_ws_dir = self.path_manager.get_directory('workspace')
        output_ws_path = os.path.join(output_ws_dir, basename)
        if self.stdout.verbosity == "DEBUG":
            output_log_path = None
        else:
            output_log_path = os.path.splitext(output_ws_path)[0] + '.log'
        
        if os.path.exists(output_ws_path) and self.config['cache']:
            self.stdout.info(f'Cache modified workspace "{output_ws_path}".', 'okgreen')
            return None

        config = self.get_modification_config(input_ws_path, output_ws_path)

        status = 0
        self.stdout.info(f'Creating modified workspace "{output_ws_path}".')
        with standard_log(output_log_path) as logger:
            ws_modifier = XMLWSModifier(config)
            ws_modifier.create_modified_workspace()
            status = 1
        if not status:
            raise RuntimeError("workspace modification failed, please check the log file for "
                               f"more details: {output_log_path}")

        if self.modification_options["gen_asimov"] is not None:
            self.run_asimov(output_ws_path,str(self.modification_options["gen_asimov"]))