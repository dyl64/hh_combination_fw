from typing import Optional, Union, Dict, List
import os
import sys
import re
import time
import shutil
import subprocess
import glob
import json
import copy

import utils
from quickstats.components import ExtendedModel, ParamParser, AnalysisBase
from quickstats.concurrent.logging import standard_log
from quickstats.utils.common_utils import execute_multi_tasks
from quickstats.concurrent.parameterised_asymptotic_cls import run_param_scan
import scalings
from xml_tool import create_combination_xml

class TaskBase:
    
    WSC_PATH  = os.environ['WORKSPACECOMBINER_PATH']
    MERGED_LIMITS_FNAME = 'limits.json'
    
    def __init__(self, *args, **kwargs):
        self.initialize(*args, **kwargs)

    def initialize(self, resonant_type, poi_name, data_name, file_expr=None, param_expr=None,
                   do_better_bands=True, CL=0.95, blind=True, verbosity:str="INFO", minimizer_options=None,
                   parallel=-1, cache=True, save_summary=False, do_limit=True, 
                   do_likelihood=False, do_pvalue=False, task_options=None, **kwargs):
        self.minimizer_options    = self.parse_minimizer_options(minimizer_options)
        config = {}
        config['data_name']       = data_name
        config['poi_name']        = poi_name
        config['do_blind']        = blind
        config['do_better_bands'] = do_better_bands
        config['CL']              = CL
        config['verbosity']       = verbosity
        self.config = config
        
        self.resonant_type = resonant_type
        self.file_expr = file_expr
        self.param_expr = param_expr
        
        self.cache = cache
        self.save_summary = save_summary
        self.parallel = parallel        
        self.do_limit = do_limit
        self.do_likelihood = do_likelihood
        self.do_pvalue = do_pvalue
        self.task_options = task_options
        self.setup_paths()
        
        self.param_parser = ParamParser(self.file_expr, self.param_expr)
        self.int_param_points = self.param_parser.get_internal_param_points()
        self.param_points = self.get_param_points()

        self.pois_to_keep = [poi_name]
        if len(self.int_param_points) > 0:
            param_point = self.int_param_points[0]
            self.pois_to_keep += list(param_point)
            
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
            'dirname'     : self.basis_dir,
            'file_expr'   : self.file_expr,
            'param_expr'  : self.param_expr,
            'outdir'      : self.limit_dir,
            'outname'     : self.MERGED_LIMITS_FNAME,
            'cache'       : self.cache,
            'save_log'    : True,
            'save_summary': self.save_summary,
            'parallel'    : self.parallel,
            'config'      : {**self.minimizer_options['limit_setting'], **self.config}
        }

        run_param_scan(**kwargs)
        
    def calculate_pvalue(self, param_point):
        if (self.task_options is None):
            return None
        options =  self.task_options.get("calculate_pvalue", None)
        if options is None:
            return None
        filename  = os.path.join(self.basis_dir, f"{param_point['basename']}.root")
        data_name = self.config['data_name']
        if 'poi_name' in options:
            poi_name = options['poi_name']
        else:
            poi_name  = self.config['poi_name']
        config    = self.minimizer_options['pvalue']
        verbosity = self.config['verbosity']
        
        if 'dataset' in options:
            _data_name = options['dataset']

        if 'mu' in options:
            mu = options['mu']
        else:
            mu = 0
        
        if 'do_minos' in options:
            do_minos = options['do_minos']
        else:
            do_minos = False
        
        print(f"INFO: Evaluating p-value (dataset={_data_name}, mu={round(mu, 8)}) for the workspace {filename}")
        outpath = os.path.join(self.pvalue_dir, f"{param_point['basename']}_{_data_name}_mu_{mu}.json")
        if os.path.exists(outpath) and self.cache:
            print(f"INFO: Cached p-value output from {outpath}")
            return None
        log_path = os.path.splitext(outpath)[0] + ".log"
        with standard_log(log_path) as logger:
            analysis  = AnalysisBase(filename, data_name=data_name,
                                     poi_name=poi_name, config=config,
                                     verbosity=verbosity)
            if 'generate_asimov' in options:
                asimov_type = options['generate_asimov']
                analysis.generate_standard_asimov(asimov_type)
                asimov_savepath = os.path.join(self.pvalue_dir, f"{param_point['basename']}_asimov.root")
                analysis.save(asimov_savepath)

            analysis.set_data(_data_name)

            fit_result = analysis.nll_fit(poi_val=mu, mode=0, do_minos=do_minos)
            
            with open(outpath, "w") as f:
                json.dump(fit_result, f, indent=4)
        
    def likelihood_scan(self, param_point):
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
                kwargs = {
                    'filename': filename,
                    'poi_min': float(options['min']),
                    'poi_max': float(options['max']),
                    'poi_step': float(options['step']),
                    'poi_name': poi_name,
                    'cache': self.cache,
                    'outname': outname,
                    'outdir': outdir,
                    'data_name': data_name,
                    'snapshot_name': config.get('snapshot_name', None),
                    'parallel' : self.parallel,
                    'save_log': True
                }
                kwargs = {**config, **kwargs}

                from quickstats.components.likelihood import scan_nll

                scan_nll(**kwargs)
        
    def finalize(self):
        pass
            
    def preprocess(self, param_point):
        raise NotImplementedError("this method should be overridden")
        
    def run_pipeline(self):
        start = time.time()
        self.makedirs()
        self.copy_dtd()
        execute_multi_tasks(self.preprocess, self.param_points, parallel=self.parallel)
        if self.do_limit:
            self.limit_setting()
        for param_point in self.param_points:
            if self.do_likelihood:
                self.likelihood_scan(param_point)
            if self.do_pvalue:
                self.calculate_pvalue(param_point)
        self.finalize()
        end = time.time()
        print('INFO: Task finished. Total time taken: {:.3f} s'.format(end-start))
        
        
class TaskPipelineWS(TaskBase):
    
    def initialize(self, input_dir, output_dir, resonant_type, channel, scaling_release, 
                   old_poiname, new_poiname, old_dataname, new_dataname, 
                   redefine_parameters=None, rescale_poi=None, **kwargs):
        
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.channel = channel
        self.scaling_release = scaling_release
        self.redefine_parameters = redefine_parameters
        self.rescale_poi = rescale_poi
        self.old_poiname = old_poiname
        self.new_poiname = new_poiname
        self.old_dataname = old_dataname
        self.new_dataname = new_dataname
        super().initialize(resonant_type, new_poiname, new_dataname, **kwargs)
        
    def sanity_check(self):
        super().sanity_check()
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError('input workspace directory {} does not exist.'.format(self.input_dir))
                
    def setup_paths(self):
        self.input_ws_dir    = os.path.join(self.input_dir, self.channel, self.resonant_type)
        self.regularised_dir = os.path.join(self.output_dir, "regularised", self.resonant_type, self.channel)
        self.rescaled_dir    = os.path.join(self.output_dir, "rescaled", self.resonant_type, self.channel)
        self.limit_dir       = os.path.join(self.output_dir, 'limits', self.resonant_type, self.channel)
        self.likelihood_dir  = os.path.join(self.output_dir, 'likelihood_scans', self.resonant_type, self.channel)
        self.pvalue_dir      = os.path.join(self.output_dir, 'pvalues', self.resonant_type, self.channel)
        self.figure_dir           = os.path.join(self.output_dir, 'figures')        
        self.rescale_cfg_file_dir = os.path.join(self.output_dir, 'cfg', 'rescale', self.resonant_type, self.channel)
        self.basis_dir = self.rescaled_dir
        self.datafile_name = "{0}-{1}.dat".format(self.resonant_type, self.channel)       
        
    def makedirs(self):
        utils.mkdirs([self.regularised_dir, self.rescaled_dir, self.rescale_cfg_file_dir,
                      self.limit_dir, self.figure_dir, self.pvalue_dir, self.likelihood_dir])
        
    def copy_dtd(self):
        source_path = os.path.join(f'{self.WSC_PATH}/dtd', 'Organization.dtd')
        if not os.path.exists(source_path):
            raise FileNotFoundError('File {} not found'.format(source_path))
        shutil.copy2(source_path, self.rescale_cfg_file_dir)
        
    def get_param_points(self):
        param_points = self.param_parser.get_external_param_points(self.input_ws_dir)
        return param_points
       
    @staticmethod
    def create_rescale_cfg_file(cfg_file, input_ws, output_ws, old_poiname, new_poiname,
                                poi_scale, pois_to_keep, oldpoi_equiv_name='mu_old', 
                                redefine_parameters=None):
        
        print('INFO: Creating config file: {0}, poi: {1} --> {2}, scaling: {3}'.format(
              cfg_file,  old_poiname, new_poiname, poi_scale))

        from quickstats.utils.xml_tools import TXMLTree
        
        cfg_xml = TXMLTree(doctype="Organization", system="Organization.dtd")
        
        attrib = {
            "InFile": input_ws,
            "OutFile": output_ws,
            "ModelName": "dummy",
            "POINames": pois_to_keep
        }
        cfg_xml.new_root(tag="Organization", attrib=attrib)
        # need to check the default value of the poi
        model = ExtendedModel(input_ws, data_name=None, verbosity="WARNING", binned_likelihood=False)
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
        cfg_xml.add_node(tag="Item", Name=new_poi_expr)
        
        mappings = [(old_poiname, oldpoi_equiv_name)]

        if redefine_parameters is not None:
            for param in redefine_parameters:
                param_val = redefine_parameters[param]
                cfg_xml.add_node(tag="Item", Name=f"{param}_redef[{param_val}]")
                mappings.append((param, f"{param}_redef"))
        
        mappings_str = ", ".join([f"{old_name}={new_name}" for old_name, new_name in mappings])
        cfg_xml.add_node(tag="Map", Name=f"EDIT::NEWPDF(OLDPDF, {mappings_str})")
        
        cfg_xml.save(cfg_file)

    @staticmethod
    def guess_poi(input_ws):
        model = ExtendedModel(input_ws, data_name=None, verbosity="WARNING")
        poi_names = model.get_poi_names(input_ws)
        if len(poi_names) > 1:
            raise RuntimeError("Unable to deduce POI for the workspace {}. "
                               "Multiple POIs found: ".format(input_ws, ",".join(poi_names)))
        else:
            return poi_names[0]

    def regularise(self, param_point):
        filename = f"{param_point['basename']}.root"
        input_ws_path = param_point['filename']
        regularised_ws_path = os.path.join(self.regularised_dir, filename)       
        print("INFO: Regularising {0} --> {1}".format(input_ws_path, regularised_ws_path))
        
        wsc_bin_path = os.path.join(self.WSC_PATH, 'bin', 'manager')
                                    
        cmd_regularise = [wsc_bin_path, "-w", "decorate", "-f", input_ws_path, "-p", regularised_ws_path,
                          "-d", self.old_dataname]

        print(' '.join(cmd_regularise))
        regularise_logfile_path = regularised_ws_path.replace('.root', '.log')

        if os.path.exists(regularised_ws_path) and self.cache:
                print("\033[92mSkip: regularisation output {0} exists, skip regularisation\033[0m\033[0m".format(regularised_ws_path))
        else:
            with open(regularise_logfile_path, "w") as logfile:
                print("INFO: Writing regularisation log into {0}".format(regularise_logfile_path))
                proc = subprocess.Popen(cmd_regularise, stdout=logfile, stderr=logfile)
                proc.wait()
                  
    def rescale(self, param_point):
        filename = f"{param_point['basename']}.root"
        regularised_ws_path = os.path.join(self.regularised_dir, filename)
        rescaled_ws_path = os.path.join(self.rescaled_dir, filename)
        if "mass" not in param_point['parameters']:
            raise ValueError(f"mass attribute not inferred from file name: {filename}")
        mass = param_point['parameters']['mass']
        rescale_cfg_filename = f"{param_point['basename']}.xml"
        rescale_cfg_file_path = os.path.join(self.rescale_cfg_file_dir, rescale_cfg_filename)

        if self.rescale_poi is None:
            try:
                poi_scale = scalings.get_scaling(self.scaling_release, self.channel, self.resonant_type, mass)
            except:
                raise RuntimeError('ERROR: cannot find {0} for {1} in python_modules/scalings.py'.format(
                                   mass, self.channel))
        else:
            poi_scale = self.rescale_poi

        old_poiname = self.old_poiname if self.old_poiname is not None else self.guess_poi(regularised_ws_path)
        
        pois_to_keep = ','.join(self.pois_to_keep)
        
        self.create_rescale_cfg_file(rescale_cfg_file_path, regularised_ws_path,
                                     rescaled_ws_path, old_poiname, self.new_poiname, poi_scale, pois_to_keep,
                                     redefine_parameters=self.redefine_parameters)

        rescale_logfile_path = rescaled_ws_path.replace('.root', '.log')
        
        wsc_bin_path = os.path.join(self.WSC_PATH, 'bin', 'manager')
        
        cmd_rescale = [wsc_bin_path, "-w", "organize", "-x", rescale_cfg_file_path]
        print(' '.join(cmd_rescale))
        
        if os.path.exists(rescaled_ws_path) and self.cache:
            print("\033[92mSkip: rescaling output {0} exists, skip rescaling\033[0m".format(rescaled_ws_path))
        else:
            with open(rescale_logfile_path, "w") as logfile:
                print("INFO: Writing rescaling log into {0}".format(rescale_logfile_path))
                proc = subprocess.Popen(cmd_rescale, stdout=logfile, stderr=logfile)
                proc.wait()
                
    def preprocess(self, param_point):
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
        self.correlation_scheme = correlation_scheme
        self.scheme_tag = 'nocorr' if self.correlation_scheme is None else 'fullcorr'
        self.tag = tag_pattern.format(channels='_'.join(self.channels), scheme=self.scheme_tag)
        super().initialize(resonant_type, poi_name, data_name, **kwargs)
        self.param_points = self.get_param_points()
        print('INFO: Registered the following param points and corresponding channels for combination')
        for param_point in self.param_points:
            param_str = self.param_parser.val_encode_parameters(param_point['parameters'])
            print(f'({param_str}): {param_point["channels"]}')
        
    def get_param_points(self):
        temp = {}
        for channel in self.channels:
            dirname = os.path.join(self.input_ws_dir, channel)
            ext_param_points = self.param_parser.get_external_param_points(dirname)
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
        self.cfg_file_dir   = os.path.join(self.input_dir, 'cfg', 'combination', self.resonant_type, self.tag)
        self.output_ws_dir  = os.path.join(self.input_dir, 'combined', self.resonant_type, self.tag)
        self.limit_dir      = os.path.join(self.input_dir, 'limits', self.resonant_type, 'combined', self.tag)
        self.likelihood_dir = os.path.join(self.input_dir, 'likelihood_scans', self.resonant_type, 'combined', self.tag)
        self.pvalue_dir     = os.path.join(self.input_dir, 'pvalues', self.resonant_type, 'combined', self.tag)
        self.basis_dir = self.output_ws_dir
        self.datafile_name = "{0}-combined-{1}.dat".format(self.resonant_type, self.tag)

    def makedirs(self):      
        utils.mkdirs([self.cfg_file_dir, self.output_ws_dir, self.limit_dir, self.pvalue_dir, self.likelihood_dir])
        
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
        input_ws_paths = {}
        filename = f"{param_point['basename']}.root"
        for channel in channels:
            input_ws_paths[channel] = os.path.join(self.input_ws_dir, channel, filename)
        combined_ws_path = os.path.join(self.output_ws_dir, filename)
        poi_name = ",".join(self.pois_to_keep)
        data_name = self.config['data_name']
        xml = create_combination_xml(input_ws_paths, combined_ws_path, poi_name, 
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
        
        wsc_bin_path = os.path.join(self.WSC_PATH, 'bin', 'manager')
        cmd = [wsc_bin_path, "-w", "combine", "-x", config_file_path, "-f", combined_ws_path, "-s", fit_strategy, "-t", fit_tolerance]
        print(' '.join(cmd))
        
        if os.path.exists(combined_ws_path) and self.cache:
                print("\033[92mSkip: combined workspace {0} exists, skip workspace creation\033[0m\033[0m".format(combined_ws_path))
        else:
            with open(logfile_path, "w") as logfile:
                print("INFO: Writing combination log into {0}".format(logfile_path))
                proc = subprocess.Popen(cmd, stdout=logfile, stderr=logfile)
                proc.wait()
                
    def preprocess(self, param_point):
        self.create_combination_xml(param_point)
        self.create_combined_ws(param_point)
