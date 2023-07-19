from typing import Optional, Union, Dict, List
from pdb import set_trace
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
from itertools import repeat

import utils

from quickstats.parsers import ParamParser
from quickstats.utils.common_utils import execute_multi_tasks
from quickstats.concurrent.logging import standard_log
from quickstats.maths.numerics import str_encode_value, str_decode_value

import scalings
from xml_tool import create_combination_xml

class TaskBase:
    
    WSC_PATH  = os.environ['WORKSPACECOMBINER_PATH']
    kMergedLimitFileName = 'limits.json'
    
    def __init__(self, **kwargs):
        self.initialize(**kwargs)

    def initialize(self, resonant_type:str, poi_name:str, data_name:str, file_expr:Optional[str]=None,
                   param_expr:Optional[str]=None, blind:bool=True, minimizer_options:Optional[Dict]=None, 
                   do_limit:bool=True, do_likelihood:bool=False, do_pvalue:bool=False,
                   task_options:Optional[Dict]=None, filter_expr:Optional[str]=None,
                   exclude_expr:Optional[str]=None, extra_pois:Optional[Union[str, List]]=None,
                   parallel:int=-1, cache:bool=True, verbosity:str="INFO", experimental:bool=False, prefix_dir:Optional[str]=None, **kwargs):
        self.minimizer_options = self.parse_minimizer_options(minimizer_options)
        config = {}
        config['data_name']    = data_name
        config['poi_name']     = poi_name
        config['do_blind']     = blind
        config['verbosity']    = verbosity
        self.config = config
        
        self.resonant_type = resonant_type
        self.file_expr = file_expr
        self.param_expr = param_expr
        
        self.cache = cache
        self.parallel = parallel
        self.do_limit = do_limit
        self.do_likelihood = do_likelihood
        self.do_pvalue = do_pvalue
        self.task_options = task_options
        self.prefix_dir = prefix_dir if prefix_dir else ''
        self.setup_paths()
        
        self.param_parser = ParamParser(self.file_expr, self.param_expr)
        self.int_param_points = self.param_parser.get_internal_param_points()
        self.param_points = self.get_param_points(filter_expr=filter_expr,
                                                  exclude_expr=exclude_expr)
        self.filter_expr = filter_expr
        self.exclude_expr = exclude_expr

        self.pois_to_keep = [poi_name]
        if len(self.int_param_points) > 0:
            param_point = self.int_param_points[0]
            self.pois_to_keep += list(param_point)
        self.pois_to_keep = list(set(self.pois_to_keep))
        
        if extra_pois is not None:
            if isinstance(extra_pois, str):
                extra_pois = extra_pois.split(",")
            self.pois_to_keep = list(set(self.pois_to_keep + extra_pois))        
        
        self.experimental = experimental
        
        self.sanity_check()
            
    def parse_minimizer_options(self, config_path:Optional[str]=None):
        minimizer_options = {
            'general': {},
            'limit_setting': {},
            'likelihood_scan': {},
            'pvalue': {}
        }
        if config_path is not None:
            with open(config_path, "r") as f:
                config = json.load(f)
            if 'general' in config:
                for k in minimizer_options:
                    minimizer_options[k].update(config['general'])
            for k in ['limit_setting', 'likelihood_scan', 'pvalue']:
                if k in config:
                    minimizer_options[k].update(config[k])
        return minimizer_options
    
    def sanity_check(self):
        if not os.path.exists(self.WSC_PATH):
            raise FileNotFoundError('workspace combiner directory {} does not exist.'.format(self.WSC_PATH))
        try:
            import quickstats
        except ImportError as e:
            raise ImportError("quickstats module is not installed")
    
    def setup_paths(self):
        raise NotImplementedError("this method should be overridden")
        
    def makedirs(self):
        raise NotImplementedError("this method should be overridden")
    
    def copy_dtd(self):
        raise NotImplementedError("this method should be overridden")
        
    def get_param_points(self):
        raise NotImplementedError("this method should be overridden")        
        
    def limit_setting(self):

        kwargs = {
            'input_path'  : self.basis_dir,
            'file_expr'   : self.file_expr,
            'param_expr'  : self.param_expr,
            'filter_expr' : self.filter_expr,
            'exclude_expr': self.exclude_expr,
            'outdir'      : self.limit_dir,
            'outname'     : self.kMergedLimitFileName,
            'cache'       : self.cache,
            'save_log'    : not self.config['verbosity'] == "DEBUG",
            'save_summary': self.config['verbosity'] == "DEBUG",
            'parallel'    : self.parallel,
            'config'      : {**self.minimizer_options['limit_setting'], **self.config}
        }
        from quickstats.concurrent import ParameterisedAsymptoticCLs
        runner = ParameterisedAsymptoticCLs(**kwargs)
        runner.run()

    def compute_significance(self, filename:str, data_name:str, poi_name:str, verbosity:str, scan_point:Union[Dict, str]=""):
        if isinstance(scan_point, str):
            scan_fix_param = None
            scan_str = scan_point
        elif isinstance(scan_point, dict):
            scan_name = list(scan_point.keys())[0]
            scan_value = list(scan_point.values())[0]
            scan_fix_param = f"{scan_name}={scan_value}"
            scan_str = scan_name + "_" + str_encode_value(round(scan_value, 2))
        else:
            assert(0), scan_point

        config    = self.minimizer_options['pvalue']
        options =  self.task_options.get("calculate_pvalue", None)
        newfix = ""
        mu = 0
        do_minos = False
        if options is not None:
            mu = options.get('mu', 0)
            do_minos = options.get('do_minos', False)
            if 'fix' in options:
                newfix += ("," + options['fix'])
            if 'fix_param' in self.config:
                newfix += ("," + self.config['fix_param'])
        if scan_fix_param:
            newfix += ("," + scan_fix_param)
        if config.get('fix_param', False):
            config['fix_param'] += newfix
        else:
            config['fix_param'] = newfix[1:]

        log_path = os.path.join(self.pvalue_dir, "cache")
        if not os.path.exists(log_path):
            os.makedirs(log_path, exist_ok=True)
        if self.config['do_blind']:
            log_file = os.path.join(log_path, f"{scan_str}_asimovData_1_NP_Nominal_mu_0.log")
        else:
            log_file = os.path.join(log_path, f"{scan_str}_pvalue_obs.log")
        outpath = log_file.replace(".log", ".json")
        if os.path.exists(outpath) and self.cache:
            print(f"INFO: Cached pvalue output from {outpath}")
            return None
        print(f"INFO: Evaluating pvalue for {filename} {scan_str}")

        from quickstats.components import AnalysisBase
        
        with standard_log(log_file) as logger:
            sys.stdout.write(f"INFO: Evaluating significance for {scan_point}\n")
            analysis = AnalysisBase(filename, data_name=data_name, eps=0.1, poi_name=poi_name, config=config, verbosity=verbosity)
            if self.config['do_blind']:
                analysis.generate_standard_asimov(asimov_types=[-2], asimov_names=[f"asimovData_1_NP_Nominal_{scan_str}"])
                analysis.set_data(f"asimovData_1_NP_Nominal_{scan_str}")
            fit_result = analysis.nll_fit(poi_val=mu, mode=0, do_minos=do_minos)
            with open(outpath, "w") as f:
                json.dump(fit_result, f, indent=4)

    def calculate_pvalue(self, param_point:Dict):
        if (self.task_options is None):
            return None
        options =  self.task_options.get("calculate_pvalue", None)
        filename  = os.path.join(self.basis_dir, f"{param_point['basename']}.root")
        data_name = self.config['data_name']
        poi_name  = self.config['poi_name']
        verbosity = self.config['verbosity']
        if options is not None:
            if 'poi_name' in options:
                poi_name = options['poi_name']
            if 'dataset' in options:
                _data_name = options['dataset']

        if self.int_param_points:
            arguments = (repeat(filename), repeat(data_name), repeat(poi_name), repeat(verbosity), self.int_param_points)
            _ = execute_multi_tasks(self.compute_significance, *arguments, parallel=self.parallel)
        else:
            arguments = (filename, data_name, poi_name, verbosity, param_point['basename'])
            self.compute_significance(*arguments)

        # Merge json
        json_files = glob.glob(os.path.join(self.pvalue_dir, "cache", "*json"))
        json_files.sort()
        result = {"scan_value": [], "significance": [], "pvalue": [], "best_fit": [], "best_fit_up": [], "best_fit_down": []}
        for ifile in json_files:
            try:
                scan_str = os.path.splitext(os.path.basename(ifile))[0].split('_')[0]
                scan_name = scan_str.split("_")[0]
                scan_value = str_decode_value(scan_str.split("_")[-1])
                data = json.load(open(ifile))
                result["scan_value"].append(scan_value)
                result["significance"].append(data["significance"])
                result["pvalue"].append(data["pvalue"])
                result["best_fit"].append(data["uncond_fit"]["muhat"]["xsec_br"])
                result["best_fit_up"].append(data["uncond_fit"]["muhat_errhi"]["xsec_br"])
                result["best_fit_down"].append(data["uncond_fit"]["muhat_errlo"]["xsec_br"])
            except:
                print("ERROR: ", ifile)
                return

        with open(os.path.join(self.pvalue_dir, "pvalue.json"), "w") as fp:
            print("INFO: Save to", os.path.join(self.pvalue_dir, "pvalue.json"))
            json.dump(result, fp, indent = 4)
        
    def likelihood_scan(self, param_point:Dict):
        if (self.task_options is None):
            return None
        scenario_options = self.task_options.get("likelihood_scan", None)
        if scenario_options is None:
            return None
        for scenario in scenario_options:
            options = scenario_options[scenario]
            filename = os.path.join(self.basis_dir, f"{param_point['basename']}.root")
            data_name = self.config['data_name']
            if 'poi_name' in options:
                poi_name = options['poi_name']
            else:
                poi_name  = self.config['poi_name']
            config    = self.minimizer_options['likelihood_scan']
            if 'fix' in options:
                if 'fix_param' in config:
                    config['fix_param'] = config['fix_param'] + "," + options['fix']
                else:
                    config['fix_param'] = options['fix']
            verbosity = self.config['verbosity']

            print(f'INFO: Running likelihood scan on the poi "{poi_name}" for the workspace {filename}')
            outname = f"{poi_name}.json"
            outdir  = os.path.join(self.likelihood_dir, scenario)
            if not os.path.exists(outdir) and self.cache:
                os.makedirs(outdir, exist_ok=True)
            outpath = os.path.join(outdir, outname)
            if os.path.exists(outpath) and self.cache:
                print(f"INFO: Cached likelihood scan output from {outpath}")
                return None

            log_path = os.path.splitext(outpath)[0] + ".log"
            from quickstats.components import AnalysisBase
            from quickstats.concurrent.logging import standard_log
            with standard_log(log_path) as logger:    
                analysis  = AnalysisBase(filename, data_name=data_name,
                                         poi_name=poi_name, config=config,
                                         verbosity=verbosity)
                if 'generate_asimov' in options:
                    asimov_type = options['generate_asimov']
                    analysis.generate_standard_asimov(asimov_type)
                    asimov_savepath = os.path.join(outdir, f"{param_point['basename']}_asimov.root")
                    analysis.save(asimov_savepath)
                    filename = asimov_savepath

                if 'dataset' in options:
                    data_name = options['dataset']
                    analysis.set_data(data_name)
                param_expr = f"{poi_name}={options['min']}_{options['max']}_{options['step']}"
                kwargs = {
                    'input_file': filename,
                    'param_expr': param_expr,
                    'cache': self.cache,
                    'outname': outname,
                    'outdir': outdir,
                    'data_name': data_name,
                    'config': {
                        **config,
                        'snapshot_name': config.get('snapshot_name', None)
                    },
                    'parallel' : self.parallel,
                    'save_log': True
                }
                from quickstats.concurrent import ParameterisedLikelihood
                runner = ParameterisedLikelihood(**kwargs)
                runner.run()
        
    def finalize(self):
        pass
            
    def preprocess(self, param_point:Dict):
        raise NotImplementedError("this method should be overridden")
        
    def run_pipeline(self):
        if not self.param_points:
            print(f"WARNING: No inputs found in {self.input_ws_dir} that satisfy the task requirement. "
                  f"Please double check.")
            return None
        start = time.time()
        self.makedirs()
        self.copy_dtd()
        result = execute_multi_tasks(self.preprocess, self.param_points, parallel=self.parallel)
        if self.do_limit:
            self.limit_setting()
        for param_point in self.param_points:
            if self.do_likelihood:
                self.likelihood_scan(param_point)
        if self.int_param_points:
            for param_point in self.param_points:
                if self.do_pvalue:
                    self.calculate_pvalue(param_point)
        else:
            if self.do_pvalue:
                execute_multi_tasks(self.calculate_pvalue, self.param_points, parallel=self.parallel)
        self.finalize()
        end = time.time()
        print('INFO: Task finished. Total time taken: {:.3f} s'.format(end-start))
        
        
class TaskPipelineWS(TaskBase):
    
    def initialize(self, input_dir:str, output_dir:str, resonant_type:str, channel:str,
                   old_poiname:str, new_poiname:str, old_dataname:str,
                   new_dataname:str, define_parameters:Optional[Dict]=None,
                   define_constraints:Optional[Dict]=None, 
                   redefine_parameters:Optional[Dict]=None, rename_parameters:Optional[Dict]=None,
                   rescale_poi:Optional[float]=None, fix_parameters:Optional[str]=None,
                   profile_parameters:Optional[str]=None, reset_parameters:Optional[str]=None, add_product_terms:Optional[Dict]=None,
                   **kwargs):
        
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.channel = channel
        self.define_parameters = define_parameters
        self.define_constraints = define_constraints
        self.add_product_terms = add_product_terms
        self.redefine_parameters = redefine_parameters
        self.rename_parameters = rename_parameters
        self.fix_parameters = fix_parameters
        self.profile_parameters = profile_parameters
        self.reset_parameters = reset_parameters
        self.rescale_poi = rescale_poi
        self.old_poiname = old_poiname
        self.new_poiname = new_poiname
        self.old_dataname = old_dataname
        self.new_dataname = new_dataname
        super().initialize(resonant_type=resonant_type,
                           poi_name=new_poiname,
                           data_name=new_dataname, **kwargs)

        
    def sanity_check(self):
        super().sanity_check()
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f'input workspace directory {self.input_dir} does not exist.')
                
    def setup_paths(self):
        self.input_ws_dir    = os.path.join(self.input_dir, self.channel, self.resonant_type)
        self.regularised_dir = os.path.join(self.output_dir, "regularised", self.resonant_type, self.channel)
        self.rescaled_dir    = os.path.join(self.output_dir, "rescaled", self.resonant_type, self.channel)
        self.limit_dir       = os.path.join(self.output_dir, 'limits', self.resonant_type, self.channel)
        self.likelihood_dir  = os.path.join(self.output_dir, 'likelihood_scans', self.resonant_type, self.channel)
        self.pvalue_dir      = os.path.join(self.output_dir, 'pvalues', self.resonant_type, self.channel)
        #self.figure_dir           = os.path.join(self.output_dir, 'figures')        
        self.rescale_cfg_file_dir = os.path.join(self.output_dir, 'cfg', 'rescale', self.resonant_type, self.channel)
        self.basis_dir = self.rescaled_dir
        #self.datafile_name = "{0}-{1}.dat".format(self.resonant_type, self.channel)       
        
    def makedirs(self):
        dirs = [self.rescaled_dir]
        if not self.experimental:
            dirs.append(self.regularised_dir)
            dirs.append(self.rescale_cfg_file_dir)
        if self.do_limit:
            dirs.append(self.limit_dir)
        if self.do_likelihood:
            dirs.append(self.likelihood_dir)
        if self.do_pvalue:
            dirs.append(self.pvalue_dir)

        utils.mkdirs(dirs)
        
    def copy_dtd(self):
        if self.experimental:
            return
        source_path = os.path.join(f'{self.WSC_PATH}/dtd', 'Organization.dtd')
        if not os.path.exists(source_path):
            raise FileNotFoundError('File {} not found'.format(source_path))
        shutil.copy2(source_path, self.rescale_cfg_file_dir)
        
    def get_param_points(self, filter_expr:Optional[str]=None, exclude_expr:Optional[str]=None):
        param_points = self.param_parser.get_external_param_points(self.input_ws_dir,
                                                                   filter_expr=filter_expr,
                                                                   exclude_expr=exclude_expr)
        return param_points
       
    @staticmethod
    def create_rescale_cfg_file(cfg_file:str, input_ws:str, output_ws:str, old_poiname:str,
                                new_poiname:str, poi_scale:float, pois_to_keep:List,
                                oldpoi_equiv_name:str='mu_old',
                                redefine_parameters:Optional[Dict]=None,
                                rename_parameters:Optional[Dict]=None,
                                define_parameters:Optional[Dict]=None,
                                define_constraints:Optional[Dict]=None,
                                add_product_terms:Optional[Dict]=None):
        
        print('INFO: Creating config file: {0}, poi: {1} --> {2}, scaling: {3}'.format(
              cfg_file,  old_poiname, new_poiname, poi_scale))
        
        from quickstats.components import ExtendedModel
        model   = ExtendedModel(input_ws, data_name=None, verbosity="WARNING")
        ws_name = model.workspace.GetName()
        mc_name = model.model_config.GetName()

        from quickstats.utils.xml_tools import TXMLTree
        
        cfg_xml = TXMLTree(doctype="Organization", system="Organization.dtd")
        
        attrib = {
            "InFile"   : input_ws,
            "OutFile"  : output_ws,
            "ModelName": mc_name,
            "POINames" : pois_to_keep,
            "WorkspaceName": ws_name
        }
        cfg_xml.new_root(tag="Organization", attrib=attrib)
        
        # need to check the default value of the poi
        poi     = model.workspace.var(old_poiname)
        if not poi:
            raise RuntimeError(f'the workspace "{input_ws}" does not contain the parameter "{old_poiname}"')
        old_poi_val = poi.getVal()
        new_poi_val = old_poi_val * poi_scale
        old_poi_min = poi.getRange()[0]
        old_poi_max = poi.getRange()[1]
        if abs(old_poi_min) > 1e10:
            new_poi_min = old_poi_min
        else:
            new_poi_min = old_poi_min * poi_scale
        if abs(old_poi_max) > 1e10:
            new_poi_max = old_poi_max
        else:
            new_poi_max = old_poi_max * poi_scale
        new_poi_expr = f"expr::{oldpoi_equiv_name}('@0/{poi_scale}', {new_poiname}[{new_poi_val}, {new_poi_min}, {new_poi_max}])"
        cfg_xml.add_node(tag="Item", Name=new_poi_expr)
        
        mappings = [(old_poiname, oldpoi_equiv_name)]

        if redefine_parameters is not None:
            if isinstance(redefine_parameters, dict):
                for param in redefine_parameters:
                    param_val = redefine_parameters[param]
                    redef_expr = f"{param}[{param_val}]"
                    cfg_xml.add_node(tag="Item", Name=redef_expr)
            elif isinstance(redefine_parameters, list):
                for expr in redefine_parameters:
                    cfg_xml.add_node(tag="Item", Name=expr)
            else:
                raise RuntimeError("invalid redefine expression")
                
        if define_parameters is not None:
            for expr in define_parameters:
                cfg_xml.add_node(tag="Item", Name=f"{expr}")
                
        if define_constraints is not None:
            for constr_data in define_constraints:
                expr = constr_data['Name']
                nuis = constr_data['NP']
                glob = constr_data['GO']
                cfg_xml.add_node(tag="Item", Name=f"{expr}", Type="constraint", NP=f"{nuis}", GO=f"{glob}")
        if add_product_terms is not None:
            for name, terms in add_product_terms.items():
                cfg_xml.add_node(tag="Item", Name=f"{name}", Terms=",".join(terms))
                
        if rename_parameters is not None:
            for old_name, new_name in rename_parameters.items():
                mappings.append((old_name, new_name))
                
        mappings_str = ", ".join([f"{old_name}={new_name}" for old_name, new_name in mappings])
        cfg_xml.add_node(tag="Map", Name=f"EDIT::NEWPDF(OLDPDF, {mappings_str})")
        
        cfg_xml.save(cfg_file)

    @staticmethod
    def guess_poi(input_ws):
        from quickstats.components import ExtendedModel
        model = ExtendedModel(input_ws, data_name=None, verbosity="WARNING")
        poi_names = [poi.GetName() for poi in model.pois]
        if len(poi_names) > 1:
            raise RuntimeError("Unable to deduce POI for the workspace {}. "
                               "Multiple POIs found: ".format(input_ws, ",".join(poi_names)))
        else:
            return poi_names[0]

    def regularise(self, param_point:Dict):
        filename = f"{param_point['basename']}.root"
        input_ws_path = param_point['filename']
        regularised_ws_path = os.path.join(self.regularised_dir, filename)       
        print("INFO: Regularising {0} --> {1}".format(input_ws_path, regularised_ws_path))
        
        from quickstats.components import ExtendedModel
        model   = ExtendedModel(input_ws_path, data_name=None, verbosity="WARNING")
        ws_name = model.workspace.GetName()
        
        wsc_bin_path = os.path.join(self.WSC_PATH, 'build', 'manager')
        
        tmp_ws_path = regularised_ws_path.replace(".root", "_tmp.root")

        cmd_regularise = [wsc_bin_path, "-w", "regulate", "-f", input_ws_path, "-p", tmp_ws_path,
                          "--dataName", self.old_dataname, "--wsName", ws_name]
        
        print(' '.join(cmd_regularise))
        regularise_logfile_path = regularised_ws_path.replace('.root', '.log')

        if os.path.exists(regularised_ws_path) and self.cache:
                print("\033[92mSkip: regularisation output {0} exists, skip regularisation\033[0m\033[0m".format(regularised_ws_path))
        else:
            with open(regularise_logfile_path, "w") as logfile:
                print("INFO: Writing regularisation log into {0}".format(regularise_logfile_path))
                proc = subprocess.Popen(cmd_regularise, stdout=logfile, stderr=logfile)
                proc.wait()
            status = proc.returncode
            if status != 0:
                raise RuntimeError("workspace regularisation failed, please check the log file for "
                                   f"more details: {regularise_logfile_path}")
                
        # rename datasets and fixing parameters   
        model = ExtendedModel(tmp_ws_path, data_name=None, verbosity="WARNING")
        model.rename_dataset({self.old_dataname: self.new_dataname})
        if self.fix_parameters is not None:
            model.fix_parameters(self.fix_parameters)
        if self.profile_parameters is not None:
            model.profile_parameters(self.profile_parameters)
        if self.reset_parameters is not None:
            model.reset_parameters(self.reset_parameters)
        model.save(regularised_ws_path)
                  
    def rescale(self, param_point:Dict):
        filename = f"{param_point['basename']}.root"
        regularised_ws_path = os.path.join(self.regularised_dir, filename)
        rescaled_ws_path = os.path.join(self.rescaled_dir, filename)
        if "mass" not in param_point['parameters']:
            raise ValueError(f"mass attribute not inferred from file name: {filename}")
        mass = param_point['parameters']['mass']
        rescale_cfg_filename = f"{param_point['basename']}.xml"
        rescale_cfg_file_path = os.path.join(self.rescale_cfg_file_dir, rescale_cfg_filename)

        if self.rescale_poi is None:
            poi_scale = 1.0
        else:
            poi_scale = self.rescale_poi
            
        if self.old_poiname is None:
            old_poiname = self.guess_poi(regularised_ws_path)
        else:
            old_poiname = self.old_poiname
        
        pois_to_keep = ','.join(self.pois_to_keep)
        
        self.create_rescale_cfg_file(rescale_cfg_file_path, regularised_ws_path,
                                     rescaled_ws_path, old_poiname, self.new_poiname,
                                     poi_scale, pois_to_keep,
                                     redefine_parameters=self.redefine_parameters,
                                     rename_parameters=self.rename_parameters,
                                     define_parameters=self.define_parameters,
                                     define_constraints=self.define_constraints)

        rescale_logfile_path = rescaled_ws_path.replace('.root', '.log')
        
        wsc_bin_path = os.path.join(self.WSC_PATH, 'build', 'manager')
        
        cmd_rescale = [wsc_bin_path, "-w", "edit", "-x", rescale_cfg_file_path]
        print(' '.join(cmd_rescale))
        
        if os.path.exists(rescaled_ws_path) and self.cache:
            print("\033[92mSkip: rescaling output {0} exists, skip rescaling\033[0m".format(rescaled_ws_path))
        else:
            with open(rescale_logfile_path, "w") as logfile:
                print("INFO: Writing rescaling log into {0}".format(rescale_logfile_path))
                proc = subprocess.Popen(cmd_rescale, stdout=logfile, stderr=logfile)
                proc.wait()
            status = proc.returncode
            if status != 0:
                raise RuntimeError("workspace modification failed, please check the log file for "
                                   f"more details: {rescale_logfile_path}")
                
    def modify_workspace(self, param_point:Dict, oldpoi_equiv_name:str='mu_old'):
        original_ws_path = param_point['filename']
        basename = f"{param_point['basename']}.root"
        rescaled_ws_path = os.path.join(self.rescaled_dir, basename)
        rescale_logfile_path = rescaled_ws_path.replace('.root', '.log')
        
        # cache if already done
        if os.path.exists(rescaled_ws_path) and self.cache:
            print("\033[92mSkip: rescaling output {0} exists, skip rescaling\033[0m".format(rescaled_ws_path))
            return None

        config = {
            "input_file": original_ws_path,
            "output_file": rescaled_ws_path,
            "poi_names": self.pois_to_keep,
        }
        
        config["actions"] = {"redefine": [], "define":[], "rename":{}, "constraint":[]}
        config["actions"]["rename"]["workspace"] = {None: "combWS"}
        config["actions"]["rename"]["dataset"]   = {self.old_dataname: self.new_dataname}
        config["actions"]["rename"]["variable"]  = {}

        # get poi scale factor
        mass = param_point['parameters']['mass']
        if self.rescale_poi is None:
            poi_scale = 1.0
        else:
            poi_scale = self.rescale_poi
        
        # need to check the default value and range of the poi
        from quickstats.components import ExtendedModel
        model = ExtendedModel(original_ws_path, data_name=None, verbosity="WARNING")
        new_poiname = self.new_poiname
        old_poiname = self.old_poiname if self.old_poiname is not None else self.guess_poi(original_ws_path)
        poi   = model.workspace.var(old_poiname)
        if not poi:
            raise RuntimeError(f'the workspace "{input_ws}" does not contain the parameter "{old_poiname}"')
        old_poi_val = poi.getVal()
        new_poi_val = old_poi_val * poi_scale
        old_poi_min = poi.getRange()[0]
        old_poi_max = poi.getRange()[1]
        if abs(old_poi_min) > 1e10:
            new_poi_min = old_poi_min
        else:
            new_poi_min = old_poi_min * poi_scale
        if abs(old_poi_max) > 1e10:
            new_poi_max = old_poi_max
        else:
            new_poi_max = old_poi_max * poi_scale
        new_poi_expr = f"expr::{oldpoi_equiv_name}('@0/{poi_scale}', {new_poiname}[{new_poi_val}, {new_poi_min}, {new_poi_max}])"
        config["actions"]["define"].append(new_poi_expr)
        config["actions"]["rename"]["variable"][old_poiname] = oldpoi_equiv_name
        
        if self.redefine_parameters is not None:
            if isinstance(self.redefine_parameters, dict):
                for param in self.redefine_parameters:
                    param_val = self.redefine_parameters[param]
                    redef_expr = f"{param}[{param_val}]"
                    config["actions"]["redefine"].append(redef_expr)
            elif isinstance(self.redefine_parameters, list):
                for expr in self.redefine_parameters:
                    config["actions"]["redefine"].append(expr)
            else:
                raise RuntimeError("invalid redefine expression")
                
        if self.define_parameters is not None:
            for expr in self.define_parameters:
                config["actions"]["define"].append(expr)
        if self.define_constraints is not None:
            for constr_dict in self.define_constraints:
                config["actions"]["constraint"].append(constr_dict)
        if self.add_product_terms is not None:
                config["actions"]["add_product_terms"] = self.add_product_terms
        if self.rename_parameters is not None:
            for old_name, new_name in self.rename_parameters.items():
                config["actions"]["rename"]["variable"][old_name] = new_name
        if self.fix_parameters is not None:
            config["fix_parameters"] = self.fix_parameters
        if self.profile_parameters is not None:
            config["profile_parameters"] = self.profile_parameters
        if self.reset_parameters is not None:
            config["reset_parameters"] = self.reset_parameters
            
        from quickstats.components.workspaces import XMLWSModifier
        from quickstats.concurrent.logging import standard_log
        print("INFO: Writing rescaling log into {0}".format(rescale_logfile_path))

        status = 0
        if self.config["verbosity"] == "DEBUG":
            rescale_logfile_path = None
        with standard_log(rescale_logfile_path) as logger:
            ws_modifier = XMLWSModifier(config)
            ws_modifier.create_modified_workspace()
            status = 1
        if not status:
            raise RuntimeError("workspace modification failed, please check the log file for "
                               f"more details: {rescale_logfile_path}")

    def preprocess(self, param_point):
        if self.experimental:
            self.modify_workspace(param_point)
        else:
            self.regularise(param_point)
            self.rescale(param_point)

class TaskCombination(TaskBase):
    
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
    
    def initialize(self, input_dir, resonant_type, channels, poi_name, data_name, correlation_scheme=None,
                   tag_pattern='A-{channels}-{scheme}', **kwargs):
        self.input_dir = input_dir
        self.channels = channels
        self.channels.sort()
        self.correlation_scheme = correlation_scheme
        self.scheme_tag = 'nocorr' if self.correlation_scheme is None else 'fullcorr'
        self.tag = tag_pattern.format(channels='_'.join(self.channels), scheme=self.scheme_tag)
        super().initialize(resonant_type=resonant_type,
                           poi_name=poi_name, data_name=data_name, **kwargs)
        if not self.param_points:
            raise RuntimeError("No points to combine")
        print('INFO: Registered the following param points and corresponding channels for combination')
        for param_point in self.param_points:
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
            param_points.append(param_point)
        return param_points
    
    def sanity_check(self):
        super().sanity_check()
        if not os.path.exists(self.input_ws_dir):
            raise FileNotFoundError('input workspace directory {} does not exist.'.format(self.input_ws_dir))   
    
    def setup_paths(self):
        self.input_ws_dir   = os.path.join(self.input_dir, 'rescaled', self.resonant_type)
        self.cfg_file_dir   = os.path.join(self.input_dir, self.prefix_dir+'cfg', 'combination', self.resonant_type, self.tag)
        self.output_ws_dir  = os.path.join(self.input_dir, self.prefix_dir+'combined', self.resonant_type, self.tag)
        self.limit_dir      = os.path.join(self.input_dir, self.prefix_dir+'limits', self.resonant_type, 'combined', self.tag)
        self.likelihood_dir = os.path.join(self.input_dir, self.prefix_dir+'likelihood_scans', self.resonant_type, 'combined', self.tag)
        self.pvalue_dir     = os.path.join(self.input_dir, self.prefix_dir+'pvalues', self.resonant_type, 'combined', self.tag)
        self.basis_dir = self.output_ws_dir
        #self.datafile_name = "{0}-combined-{1}.dat".format(self.resonant_type, self.tag)

    def makedirs(self):
        dirs = [self.cfg_file_dir, self.output_ws_dir]
        if self.do_limit:
            dirs.append(self.limit_dir)
        if self.do_likelihood:
            dirs.append(self.likelihood_dir)
        if self.do_pvalue:
            dirs.append(self.pvalue_dir)

        utils.mkdirs(dirs)
        
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
        data_name = self.config['data_name']
        for channel in channels:
            channel_attributes[channel] = {}
            channel_attributes[channel]["filename"]  = os.path.join(self.input_ws_dir, channel, filename)
            channel_attributes[channel]["data_name"] = data_name
        combined_ws_path = os.path.join(self.output_ws_dir, filename)
        poi_name = ",".join(self.pois_to_keep)
        xml = create_combination_xml(channel_attributes, combined_ws_path, poi_name, 
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
        
        if os.path.exists(combined_ws_path) and self.cache:
                print("\033[92mSkip: combined workspace {0} exists, skip workspace creation\033[0m\033[0m".format(combined_ws_path))
        else:
            with open(logfile_path, "w") as logfile:
                print("INFO: Writing combination log into {0}".format(logfile_path))
                proc = subprocess.Popen(cmd, stdout=logfile, stderr=logfile)
                proc.wait()
    
    def create_combined_ws_experimental(self, param_point):
        from quickstats.components.workspaces import XMLWSCombiner
        combined_ws_path = os.path.join(self.output_ws_dir, f"{param_point['basename']}.root")
        config_file_path = os.path.join(self.cfg_file_dir, f"{param_point['basename']}.xml")
        logfile_path = combined_ws_path.replace('.root', '.log')

        if os.path.exists(combined_ws_path) and self.cache:
                print("\033[92mSkip: combined workspace {0} exists, skip workspace creation\033[0m\033[0m".format(combined_ws_path))
        else:
            if self.config["verbosity"] == "DEBUG":
                logfile_path = None
            if logfile_path is not None:
                print("INFO: Writing combination log into {0}".format(logfile_path))
            status = 0
            from quickstats.concurrent.logging import standard_log
            from quickstats.components.workspaces import XMLWSCombiner
            with standard_log(logfile_path) as logger:
                ws_combiner = XMLWSCombiner(config_file_path)
                ws_combiner.create_combined_workspace()
                status = 1
            if not status:
                raise RuntimeError("workspace combination failed, please check the log file for "
                                   f"more details: {logfile_path}")
                
    def preprocess(self, param_point):
        self.create_combination_xml(param_point)
        if self.experimental:
            self.create_combined_ws_experimental(param_point)
        else:
            self.create_combined_ws(param_point)
        return True
