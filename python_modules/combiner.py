import os
from pdb import set_trace
import sys
import re
import time
import shutil
import subprocess
import glob
import json
import copy

import utils
from quickstats.components import ExtendedModel
import scalings
import limit_setting as ls
from xml_tool import create_combination_xml

class TaskBase:
    
    WSC_PATH  = os.environ['WORKSPACECOMBINER_PATH']
    BASIS_WS_PATTERN = '{basename}.root'
    MERGED_LIMITS_FNAME = 'limits.json'
    
    def __init__(self, *args, **kwargs):
        self.initialize(*args, **kwargs)

    def initialize(self, resonant_type, poi_name, data_name, do_better_bands=True, CL=0.95, blind=True, 
                   mass_expr=None, param=None, verbose=False, minimizer_options=None,
                   parallel=-1, file_format=None, cache=True, save_summary=False, do_limit=True, **kwargs):
        self.resonant_type = resonant_type
        self.poi_name = poi_name
        self.data_name = data_name
        self.do_better_bands = do_better_bands
        self.CL = CL
        self.blind = blind
        self.verbose = verbose
        self.parallel = parallel
        self.snapshot = None
        self.file_format = file_format
        if minimizer_options is not None:
            self.minimizer_options = json.load(open(minimizer_options))
        else:
            self.minimizer_options = {}
        self.cache = cache
        self.save_summary = save_summary
        self.do_limit = do_limit
        self.setup_paths()
        self.param_points = self.get_param_points(mass_expr)
        if not self.param_points:
            print('mass_expr = {0}, self.param_points = {1}'.format(mass_expr, self.param_points))
            raise FileNotFoundError('no param point found.')
        if param is None:
            self.parameterized_points = None
        else:
            self.parameterized_points = utils.get_paramterized_points(param)
        self.pois_to_keep = [poi_name]
        if param is not None:
            self.pois_to_keep += [p.split('=')[0] for p in param.split(',')]
        self.sanity_check()
    
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
    
    def get_param_points(self, mass_expr=None):
        raise NotImplementedError("this method should be overridden")
    
    #def gen_asimov(self, param_point):
    #    filename = self.BASIS_WS_PATTERN.format(**param_point)
    #    basis_ws_path = os.path.join(self.basis_dir, filename)
    #    asimov_NP_nom_filename = self.ASIMOV_NP_NOM_WS_PATTERN.format(**param_point)
    #    asimov_NP_fit_filename = self.ASIMOV_NP_FIT_WS_PATTERN.format(**param_point)
    #    ws_with_Asimov_NP_nom_path = os.path.join(self.asimov_dir, asimov_NP_nom_filename)
    #    ws_with_Asimov_NP_fit_path = os.path.join(self.asimov_dir, asimov_NP_fit_filename)
    #    
    #    # NOTE: the dataset name is changed to "combData" after the regularization step
    #    dg.makeAsimovData(basis_ws_path, ws_with_Asimov_NP_nom_path,
    #                      self.data_name, "false", 0.0, "asimovData_POI_0_NP_nom", self.poi_name, self.snapshot)
    #    dg.makeAsimovData(basis_ws_path, ws_with_Asimov_NP_fit_path, 
    #                      self.data_name, "true",  0.0, "asimovData_POI_0_NP_fit", self.poi_name, self.snapshot)
        
    def limit_setting(self, param_point):
        
        filename = self.BASIS_WS_PATTERN.format(**param_point)
        ws_path = os.path.join(self.basis_dir, filename)
        
        basename = param_point["basename"]

        ls.CalcLimit_new(basename, ws_path, self.rootfiles_dir, self.data_name, self.poi_name,
                         self.blind, self.do_better_bands, self.CL, self.parameterized_points,
                         self.verbose, self.minimizer_options, parallel=self.parallel,
                         cache=self.cache, save_summary=self.save_summary)
        
    def merge_limits(self, param_points):
        signatures = utils.get_format_str_components(self.file_format)
        default_limit = {
              "0": None,
              "2": None,
              "1": None,
             "-1": None,
             "-2": None,
            "obs": None,
            "inj": None
        }
        all_results = []
        for param_point in param_points:
            attributes_data = {k: utils.signature_parser[signatures[k]](v) \
                               for k, v in param_point.items() if k in signatures}
            if (self.parameterized_points is None):
                result = attributes_data.copy()
                result.update(default_limit)
                basename = '{0}.json'.format(param_point["basename"])
                output_limit_path = os.path.join(self.rootfiles_dir, basename)
                if os.path.exists(output_limit_path):
                    result.update(json.load(open(output_limit_path, 'r')))
                all_results.append(result)            
            else:
                for key, value in self.parameterized_points.items():
                    result = attributes_data.copy()
                    parameters = {token.split("=")[0]:float(token.split("=")[1]) for token in value.split(',')}
                    result.update(parameters)
                    result.update(default_limit)
                    basename = '{0}_{1}.json'.format(param_point["basename"], key)
                    output_limit_path = os.path.join(self.rootfiles_dir, basename)
                    if os.path.exists(output_limit_path):
                        result.update(json.load(open(output_limit_path, 'r')))
                    all_results.append(result)
        merged_limit_path = os.path.join(self.rootfiles_dir, self.MERGED_LIMITS_FNAME)
        import pandas as pd
        merged_limits = pd.DataFrame(all_results).to_dict('list')
        with open(merged_limit_path, 'w') as outfile:
            json.dump(merged_limits, outfile, indent=2)
        
    def finalize(self, param_points):
        if self.do_limit:
            self.merge_limits(param_points)
            
    def _run_pipeline(self, param_point):
        raise NotImplementedError("this method should be overridden")
        
    def run_pipeline(self):
        start = time.time()
        self.makedirs()
        self.copy_dtd()
        if self.parameterized_points is None:
            utils.execute_multi_tasks(self._run_pipeline, self.param_points, parallel=self.parallel)
        else:
            print('INFO: Force sequential execution with parameterization')
            for param_point in self.param_points:
                self._run_pipeline(param_point)
        self.finalize(self.param_points)
        end = time.time()
        print('INFO: Task finished. Total time taken: {}s'.format(end-start))
        
        
class TaskPipelineWS(TaskBase):
    
    RESCALE_CFG_EXPR = r'{basename}.xml'
    
    def initialize(self, input_dir, output_dir, resonant_type, channel, scaling_release, 
                   old_poiname, new_poiname, old_dataname, new_dataname, do_better_bands=True,
                   CL=0.95, blind=True, mass_expr=None, param=None, verbose=False, 
                   minimizer_options=None, redefine_parameters=None, rescale_poi=None,
                   parallel=-1, file_format=None, **kwargs):
        
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
        super().initialize(resonant_type, new_poiname, new_dataname, do_better_bands, CL, blind, 
                           mass_expr, param, verbose=verbose,
                           minimizer_options=minimizer_options, parallel=parallel, file_format=file_format, **kwargs)
        
    def sanity_check(self):
        super().sanity_check()
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError('input workspace directory {} does not exist.'.format(self.input_dir))
        if (self.parameterized_points is not None) and (self.resonant_type != "nonres"):
                raise ValueError("parameterization is only allowed for non-resonant analysis")
                
    def setup_paths(self):
        self.regularized_dir = os.path.join(self.output_dir, "regularised", self.resonant_type, self.channel)
        self.rescaled_dir    = os.path.join(self.output_dir, "rescaled", self.resonant_type, self.channel)
        self.rootfiles_dir        = os.path.join(self.output_dir, 'limits', self.resonant_type, self.channel)
        self.figure_dir           = os.path.join(self.output_dir, 'figures')        
        self.rescale_cfg_file_dir = os.path.join(self.output_dir, 'cfg', 'rescale', self.resonant_type, self.channel)
        self.basis_dir = self.rescaled_dir
        self.asimov_dir = self.rescaled_dir
        self.datafile_name = "{0}-{1}.dat".format(self.resonant_type, self.channel)       
        
    def makedirs(self):
        utils.mkdirs([self.regularized_dir, self.rescaled_dir, self.rescale_cfg_file_dir,
                      self.rootfiles_dir, self.figure_dir])
        
    def copy_dtd(self):
        source_path = os.path.join(f'{self.WSC_PATH}/dtd', 'Organization.dtd')
        if not os.path.exists(source_path):
            raise FileNotFoundError('File {} not found'.format(source_path))
        shutil.copy2(source_path, self.rescale_cfg_file_dir)
       
    @staticmethod
    def create_rescale_cfg_file(cfg_file, input_ws, output_ws, old_poiname, new_poiname,
                                poi_scale, pois_to_keep, oldpoi_equiv_name='mu_old', 
                                redefine_parameters=None):
        
        print('Creating config file: {0}, poi: {1} --> {2}, scaling: {3}'.format(
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

        new_poi_expr = f"expr::{oldpoi_equiv_name}('@0/{poi_scale}', {new_poiname}[0.0, -1.0, 20.0])"
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
        
    def get_param_points(self, mass_expr=None):
        if mass_expr is None:
            filter_expr = None
        else:
            filter_expr = {"mass": mass_expr}
        param_points = utils.get_param_points(self.input_dir, filter_expr=filter_expr, file_format=self.file_format)
        return param_points

    @staticmethod
    def guess_poi(input_ws):
        model = ExtendedModel(input_ws, data_name=None, verbosity="WARNING")
        poi_names = model.get_poi_names(input_ws)
        if len(poi_names) > 1:
            raise RuntimeError("Unable to deduce POI for the workspace {}. "
                               "Multiple POIs found: ".format(input_ws, ",".join(poi_names)))
        else:
            return poi_names[0]

    def regularize(self, param_point):
        filename = "{}.root".format(param_point['basename'])
        input_ws_path = os.path.join(self.input_dir, filename)
        regularized_ws_path = os.path.join(self.regularized_dir, filename)
        print("INFO: Regularising {0} --> {1}".format(input_ws_path, regularized_ws_path))
        
        wsc_bin_path = os.path.join(self.WSC_PATH, 'bin', 'manager')
                                    
        cmd_regularize = [wsc_bin_path, "-w", "decorate", "-f", input_ws_path, "-p", regularized_ws_path,
                          "-d", self.old_dataname]

        print(' '.join(cmd_regularize))
        regularize_logfile_path = regularized_ws_path.replace('.root', '.log')

        if os.path.exists(regularized_ws_path) and self.cache:
                print("\033[92mSkip: regularisation output {0} exists, skip regularisation\033[0m\033[0m".format(regularized_ws_path))
        else:
            with open(regularize_logfile_path, "w") as logfile:
                print("INFO: Writing regularisation log into {0}".format(regularize_logfile_path))
                proc = subprocess.Popen(cmd_regularize, stdout=logfile, stderr=logfile)
                proc.wait()
                  
    def rescale(self, param_point):
        filename = "{}.root".format(param_point['basename'])
        regularized_ws_path = os.path.join(self.regularized_dir, filename)
        rescaled_ws_path = os.path.join(self.rescaled_dir, filename)

        if "mass" not in param_point:
            raise ValueError(f"mass attribute not inferred from file name: {filename}")
        mass = param_point['mass']
        rescale_cfg_filename = self.RESCALE_CFG_EXPR.format(**param_point)
        rescale_cfg_file_path = os.path.join(self.rescale_cfg_file_dir, rescale_cfg_filename)

        if self.rescale_poi is None:
            try:
                poi_scale = scalings.get_scaling(self.scaling_release, self.channel, self.resonant_type, mass)
            except:
                raise RuntimeError('ERROR: cannot find {0} for {1} in python_modules/scalings.py'.format(
                                   mass, self.channel))
        else:
            poi_scale = self.rescale_poi

        old_poiname = self.old_poiname if self.old_poiname is not None else self.guess_poi(regularized_ws_path)
        
        pois_to_keep = ','.join(self.pois_to_keep)
        
        self.create_rescale_cfg_file(rescale_cfg_file_path, regularized_ws_path,
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
                
    def _run_pipeline(self, param_point):
        self.regularize(param_point)
        self.rescale(param_point)
        if not self.do_limit:
            return None
        self.limit_setting(param_point)


class TaskCombination(TaskBase):

    CHANNEL_WS_EXPR = r'{basename}.root'
    COMB_WS_EXPR = r'{basename}.root'
    COMB_CFG_EXPR = r'{basename}.xml'
    
    def __init__(self, *args, **kwargs):
        self.initialize(*args, **kwargs)
        # make sure the NPs are set to nominal values at the beginning
        self.minimizer_options['snapshot_name'] = "nominalNuis"
        self.snapshot = "nominalNuis"
    
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
                   tag_pattern='A-{channels}-{scheme}', do_better_bands=True, CL=0.95, blind=True, 
                   mass_expr=None, param=None, **kwargs):
        self.input_dir = input_dir
        self.channels = channels
        self.correlation_scheme = correlation_scheme
        self.scheme_tag = 'nocorr' if self.correlation_scheme is None else 'fullcorr'
        self.tag = tag_pattern.format(channels='_'.join(self.channels), scheme=self.scheme_tag)
        super().initialize(resonant_type, poi_name, data_name, do_better_bands, CL, blind, 
                           mass_expr, param, **kwargs)
        self.param_points = self.param_points
        print('INFO: Registered the following mass points and corresponding channels for combination')
        for param_point in self.param_points:
            print('{}: {}'.format(utils.format_param_point(param_point), param_point["channels"]))
        
    def get_param_points(self, mass_expr=None):
        if mass_expr is None:
            filter_expr = None
        else:
            filter_expr = {"mass": mass_expr}
        param_points = utils.get_channel_param_points(self.input_ws_dir, self.channels,
                                                      filter_expr=filter_expr, 
                                                      file_format=self.file_format)
        return param_points
    
    def sanity_check(self):
        super().sanity_check()
        if not os.path.exists(self.input_ws_dir):
            raise FileNotFoundError('input workspace directory {} does not exist.'.format(self.input_ws_dir))   
    
    def setup_paths(self):
        self.input_ws_dir = os.path.join(self.input_dir, 'rescaled', self.resonant_type)
        self.cfg_file_dir = os.path.join(self.input_dir, 'cfg', 'combination', self.resonant_type, self.tag)
        self.output_ws_dir = os.path.join(self.input_dir, 'combined', self.resonant_type, self.tag)
        self.rootfiles_dir = os.path.join(self.input_dir, 'limits', self.resonant_type, 'combined', self.tag)
        self.basis_dir = self.output_ws_dir
        self.asimov_dir = self.output_ws_dir
        self.datafile_name = "{0}-combined-{1}.dat".format(self.resonant_type, self.tag)

    def makedirs(self):      
        utils.mkdirs([self.cfg_file_dir, self.output_ws_dir, self.rootfiles_dir])
        
    def copy_dtd(self):
        source_path = os.path.join(f'{self.WSC_PATH}/dtd', 'Combination.dtd')
        if not os.path.exists(source_path):
            raise FileNotFoundError('File {} not found'.format(source_path))
        shutil.copy2(source_path, self.cfg_file_dir)
        
    def get_combination_xml(self, param_point):
        channels = param_point.get("channels", None)
        if channels is None:
            raise ValueError('no channels to combine for the parameter point {}'.format(
                             utils.format_param_point(param_point)))
        input_ws_paths = {}
        channel_ws_expr =  self.CHANNEL_WS_EXPR
        for channel in channels:
            input_ws_paths[channel] = os.path.join(self.input_ws_dir, channel, channel_ws_expr.format(**param_point))
        combined_ws_path = os.path.join(self.output_ws_dir, self.COMB_WS_EXPR.format(**param_point))
        poi_name = ",".join(self.pois_to_keep)
        xml = create_combination_xml(input_ws_paths, combined_ws_path, poi_name, 
                                     rename_map=self.correlation_scheme, data_name=self.data_name)
        return xml
        
    def create_combination_xml(self, param_point):
        xml = self.get_combination_xml(param_point)
        xml_fname = os.path.join(self.cfg_file_dir, self.COMB_CFG_EXPR.format(**param_point))
        xml.save(xml_fname)
        print('INFO: Combination config for the point "{}" saved as "{}"'.format(
              utils.format_param_point(param_point), xml_fname))
        
    def create_combined_ws(self, param_point, fit_strategy='0', fit_tolerance='-1'):
        combined_ws_path = os.path.join(self.output_ws_dir, self.COMB_WS_EXPR.format(**param_point))
        config_file_path = os.path.join(self.cfg_file_dir, self.COMB_CFG_EXPR.format(**param_point))
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
                
    def _run_pipeline(self, param_point):
        self.create_combination_xml(param_point)
        self.create_combined_ws(param_point)
        #if (self.parameterized_points is None):
        #    self.gen_asimov(param_point)
        if not self.do_limit:
            return None
        self.limit_setting(param_point)
