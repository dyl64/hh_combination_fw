from typing import Optional, Union, Dict, List
import os
import sys
import re
import time
import shutil
import fnmatch
import subprocess
import glob
import json
import copy
import yaml


from hh_combination_fw.utils.combination_utils import create_combination_xml
from quickstats.parsers import ParamParser

from combiner import TaskBase
from quickstats.components.workspaces import XMLWSModifier

from hh_combination_fw.utils.combination_utils import create_combination_xml_bsm


class TaskPipelineBSM(TaskBase):

    def __init__(self, **kwargs):
        self.initialize(**kwargs)


    def initialize(self, input_dir:str, output_dir:str, resonant_type:str, channel:str, old_dataname:str,
                   new_dataname:str, define_parameters:Optional[Dict]=None,
                   reparam_pois:Optional[Dict]=None, rename_parameters:Optional[Dict]=None,
                   rescale_poi:Optional[float]=None, fix_parameters:Optional[str]=None,
                   profile_parameters:Optional[str]=None, file_expr:Optional[str]=None,
                   param_expr:Optional[str]=None, filter_expr:Optional[str]=None, exclude_expr:Optional[str]=None, **kwargs):
        
        config = {}
        self.config = config

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.channel = channel
        self.define_parameters = define_parameters
        self.rename_parameters = rename_parameters
        self.reparam_pois = reparam_pois
        self.old_dataname = old_dataname
        self.new_dataname = new_dataname
        self.file_expr = file_expr
        self.param_expr = param_expr
        self.resonant_type = resonant_type
        self.param_parser = ParamParser(self.file_expr, self.param_expr)
        self.setup_paths()
        self.param_points = self.get_param_points(filter_expr=filter_expr,
                                                  exclude_expr=exclude_expr)
    
    def setup_paths(self):
        self.input_ws_dir    = os.path.join(self.input_dir, "rescaled", self.resonant_type, self.channel)
        self.reparam_dir = os.path.join(self.output_dir, "reparam_BSM", self.resonant_type, self.channel)
        self.combined_dir    = os.path.join(self.output_dir, "comb_BSM", self.resonant_type, self.channel)      
        self.reparam_cfg_file_dir = os.path.join(self.output_dir, 'cfg', 'reparam_BSM', self.resonant_type, self.channel)
        self.comb_cfg_file_dir = os.path.join(self.output_dir, 'cfg', 'comb_BSM', self.resonant_type, self.channel)
        #self.datafile_name = "{0}-{1}.dat".format(self.resonant_type, self.channel)
    
    def mkdirs(self):
        dirnames = [self.reparam_dir,self.combined_dir,self.reparam_cfg_file_dir,self.comb_cfg_file_dir]
        for dirname in dirnames:
            abs_dirname = os.path.abspath(dirname)
            if not os.path.exists(abs_dirname):
                os.makedirs(abs_dirname)
        
    
    def get_param_points(self, filter_expr:Optional[str]=None, exclude_expr:Optional[str]=None):
        param_points = self.param_parser.get_external_param_points(self.input_ws_dir,
                                                                   filter_expr=filter_expr,
                                                                   exclude_expr=exclude_expr)
        return param_points
    
    def modify(self):
        for param_point in self.param_points:
            original_ws_path = param_point['filename']
            basename = f"{param_point['basename']}.root"
            rescaled_ws_path = os.path.join(self.reparam_dir, basename)
            pois_to_keep = self.reparam_pois
            config = {
                    "input_file": original_ws_path,
                    "output_file": rescaled_ws_path,
                    "poi_names": pois_to_keep,
                }
            config["actions"] = {"redefine": [], "define":[], "rename":{}, "constraint":[]}
            config["actions"]["rename"]["workspace"] = {None: "combWS"}
            config["actions"]["rename"]["dataset"]   = {self.old_dataname: self.new_dataname}
            config["actions"]["rename"]["variable"]  = {}
            if self.define_parameters is not None:
                for expr in self.define_parameters:
                    config["actions"]["define"].append(expr)
            if self.rename_parameters is not None:
                for old_name, new_name in self.rename_parameters.items():
                    config["actions"]["rename"]["variable"][old_name] = new_name
            ws_modifier = XMLWSModifier(config)
            ws_modifier.create_modified_workspace()


class TaskCombBSM(TaskBase):
    def __init__(self, *args, **kwargs):
        self.initialize(*args, **kwargs)
        # make sure the NPs are set to nominal values at the beginning
        for k in self.minimizer_options:
            self.minimizer_options[k]['snapshot_name'] = "nominalNuis"
    
    @property
    def channels(self):
        return self._channels
    
    @channels.setter
    def channels(self, val):
        if isinstance(val, str):
            self._channels = [c.strip() for c in val.split(',')]
        elif isinstance(val, list):
            self._channels = val
        else:
            raise ValueError('invalid format for channels')
    
    @property
    def correlation_scheme(self):
        return self._correlation_scheme
    
    @correlation_scheme.setter
    def correlation_scheme(self, val):
        if val is None:
            self._correlation_scheme = None
        elif isinstance(val, str):
            self._correlation_scheme = json.load(open(val, 'r'))
        elif isinstance(val, dict):
            self._correlation_scheme = val
        else:
            raise ValueError('invalid format for correlation scheme')
    
    def initialize(self, input_dir, resonant_type, channels, comb_pois, data_name,          
                   correlation_scheme=None, file_expr:Optional[str]=None,minimizer_options:Optional[Dict]=None, 
                   param_expr:Optional[str]=None,tag_pattern='A-{channels}-{scheme}', **kwargs):
        self.minimizer_options = self.parse_minimizer_options(minimizer_options)
        self.input_dir = input_dir
        self.channels = channels
        self.channels.sort()
        self.data_name=data_name
        self.correlation_scheme = correlation_scheme
        self.resonant_type = resonant_type
        self.scheme_tag = 'nocorr' if self.correlation_scheme is None else 'fullcorr'
        self.tag = tag_pattern.format(channels='_'.join(self.channels), scheme=self.scheme_tag)
        self.comb_pois = comb_pois
        self.file_expr=file_expr
        self.param_expr=param_expr 
        self.param_parser = ParamParser(self.file_expr, self.param_expr)
        self.setup_paths()
        self.makedirs()
        self.input_ws_dir   = os.path.join(self.input_dir, 'reparam_BSM', self.resonant_type)
        self.param_points=self.get_param_points()
        if not self.param_points:
            raise RuntimeError("No points to combine")
        print('INFO: Registered the following param points and corresponding channels for combination')
        for param_point in self.param_points:
            print(param_point)
            param_str = self.param_parser.val_encode_parameters(param_point['parameters'])
            print(f'({param_str}): {param_point["channels"]}')
        
    def get_param_points(self, filter_expr:Optional[str]=None, exclude_expr:Optional[str]=None):
        temp = {}
        for channel in self.channels:
            dirname = os.path.join(self.input_ws_dir, channel)
            ext_param_points = self.param_parser.get_external_param_points(dirname, filter_expr, exclude_expr)
            for param_point in ext_param_points:
                basename = param_point['basename']
                if basename not in temp:
                    temp[basename] = {"channels": [], "parameters": param_point['parameters']}
                temp[basename]['channels'].append(channel)
        param_points = []
        for basename in temp:
            channels = temp[basename]['channels']
            parameters = temp[basename]['parameters']
            param_point = {"basename":basename, "channels":channels, "parameters": parameters}
            if(len(channels)==len(self.channels)):
                param_points.append(param_point)
        return param_points
    
    def setup_paths(self):
        self.input_ws_dir   = os.path.join(self.input_dir, 'rescaled', self.resonant_type)
        self.cfg_file_dir   = os.path.join(self.input_dir, 'cfg', 'combination_BSM', self.resonant_type, self.tag)
        self.output_ws_dir  = os.path.join(self.input_dir, 'combined_BSM', self.resonant_type, self.tag)
        self.limit_dir      = os.path.join(self.input_dir, 'limits_BSM', self.resonant_type, 'combined', self.tag)
        # self.likelihood_dir = os.path.join(self.input_dir, self.prefix_dir+'likelihood_scans', self.resonant_type, 'combined', self.tag)
        # self.pvalue_dir     = os.path.join(self.input_dir, self.prefix_dir+'pvalues', self.resonant_type, 'combined', self.tag)
        self.basis_dir = self.output_ws_dir
        #self.datafile_name = "{0}-combined-{1}.dat".format(self.resonant_type, self.tag)

    def makedirs(self):
        dirnames = [self.cfg_file_dir, self.output_ws_dir]
        # if self.do_limit:
        #     dirs.append(self.limit_dir)
        # if self.do_likelihood:
        #     dirs.append(self.likelihood_dir)
        # if self.do_pvalue:
        #     dirs.append(self.pvalue_dir)
        for dirname in dirnames:
            abs_dirname = os.path.abspath(dirname)
            if not os.path.exists(abs_dirname):
                os.makedirs(abs_dirname)
        
    def copy_dtd(self):
        source_path = os.path.join(f'{self.WSC_PATH}/dtd', 'Combination.dtd')
        if not os.path.exists(source_path):
            raise FileNotFoundError('File {} not found'.format(source_path))
        shutil.copy2(source_path, self.cfg_file_dir)
        
    def get_combination_xml(self, param_point):
        channels = param_point.get("channels", None)
        param_str = self.param_parser.val_encode_parameters(param_point['parameters'])
        if channels is None:
            raise ValueError(f'no channels to combine for the parameter point "{param_str}"')
        channel_attributes = {}
        filename = f"{param_point['basename']}.root"
        data_name = self.data_name
        for channel in channels:
            channel_attributes[channel] = {}
            channel_attributes[channel]["filename"]  = os.path.join(self.input_ws_dir, channel, filename)
            channel_attributes[channel]["data_name"] = data_name
        combined_ws_path = os.path.join(self.output_ws_dir, filename)
        xml = create_combination_xml_bsm(channel_attributes, combined_ws_path, self.comb_pois, 
                                     rename_map=self.correlation_scheme, data_name=data_name)
        return xml
        
    def create_combination_xml(self, param_point):
        xml = self.get_combination_xml(param_point)
        xml_fname = os.path.join(self.cfg_file_dir, f"{param_point['basename']}.xml")
        xml.save(xml_fname)
        param_str = self.param_parser.val_encode_parameters(param_point['parameters'])
        print(f'INFO: Combination config for the point "{param_str}" saved as "{xml_fname}"')
        
    def create_combined_ws(self, param_point, fit_strategy='0', fit_tolerance='-1'):
        combined_ws_path = os.path.join(self.output_ws_dir, f"{param_point['basename']}.root")
        config_file_path = os.path.join(self.cfg_file_dir, f"{param_point['basename']}.xml")
        logfile_path = combined_ws_path.replace('.root', '.log')
        
        wsc_bin_path = os.path.join(self.WSC_PATH, 'build', 'manager')
        cmd = [wsc_bin_path, "-w", "combine", "-x", config_file_path, "-f", combined_ws_path, "-s", fit_strategy, "-t", fit_tolerance]
        print(' '.join(cmd))
        
        if os.path.exists(combined_ws_path):
                print("\033[92mSkip: combined workspace {0} exists, skip workspace creation\033[0m\033[0m".format(combined_ws_path))
        else:
            with open(logfile_path, "w") as logfile:
                print("INFO: Writing combination log into {0}".format(logfile_path))
                proc = subprocess.Popen(cmd, stdout=logfile, stderr=logfile)
                proc.wait()
    
    def create_combined_ws_experimental(self, param_point):
        from quickstats.components.workspaces import XMLWSCombiner
        from quickstats.concurrent.logging import standard_log
        combined_ws_path = os.path.join(self.output_ws_dir, f"{param_point['basename']}.root")
        config_file_path = os.path.join(self.cfg_file_dir, f"{param_point['basename']}.xml")
        logfile_path = combined_ws_path.replace('.root', '.log')

        if os.path.exists(combined_ws_path) and self.cache:
                print("\033[92mSkip: combined workspace {0} exists, skip workspace creation\033[0m\033[0m".format(combined_ws_path))
        else:
            if logfile_path is not None:
                print("INFO: Writing combination log into {0}".format(logfile_path))
            status = 0
            with standard_log(logfile_path) as logger:
                ws_combiner = XMLWSCombiner(config_file_path)
                ws_combiner.create_combined_workspace()
                status = 1
            if not status:
                raise RuntimeError("workspace combination failed, please check the log file for "
                                   f"more details: {logfile_path}")
                
    def preprocess(self, param_point):
        self.create_combination_xml(param_point)
        self.create_combined_ws(param_point)
        return True
    
    def combine(self):
        # self.copy_dtd()
        for param_point in self.param_points:
            self.create_combination_xml(param_point)
            self.create_combined_ws_experimental(param_point)

