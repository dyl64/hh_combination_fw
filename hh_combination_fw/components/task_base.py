from typing import Optional, Union, Dict, List
import os
import json

from quickstats import AbstractObject, Timer
from quickstats.parsers import ParamParser
from quickstats.utils.common_utils import execute_multi_tasks, combine_dict

from hh_combination_fw.core.settings import *
from .combination_path_manager import CombinationPathManager

class TaskBase(AbstractObject):

    @property
    def minimizer_options(self):
        return self._minimizer_options

    @property
    def config(self):
        return self._config

    @property
    def path_manager(self):
        return self._path_manager

    @property
    def param_parser(self):
        return self._param_parser
        
    @property
    def base_input_dir(self):
        return self.path_manager.input_dir

    @property
    def base_output_dir(self):
        return self.path_manager.output_dir

    @property
    def analysis_name(self):
        return self.path_manager.analysis_name

    @property
    def channel(self):
        return self.path_manager.channel

    @property
    def tasks(self):
        return self._tasks
    
    def __init__(self, verbosity:Optional[Union[int, str]]="INFO", **kwargs):
        super().__init__(verbosity=verbosity)
        self.initialize(**kwargs)

    def initialize(self, analysis_name:Optional[str]=None,
                   channel:str='combined',
                   input_dir:Optional[str]=None,
                   output_dir:Optional[str]=None,
                   poi_name:Optional[str]=None, data_name:str="combData",
                   file_expr:Optional[str]=None, param_expr:Optional[str]=None,
                   filter_expr:Optional[str]=None, exclude_expr:Optional[str]=None,
                   blind:bool=True, minimizer_options:Optional[Union[str, Dict]]=None, 
                   tasks:Optional[List]=None, task_options:Optional[Dict]=None,
                   extra_pois:Optional[List[str]]=None,
                   parallel:int=-1, cache:bool=True, verbosity:str="INFO", **kwargs):
        config = {}
        config['extra_pois']   = extra_pois
        config['data_name']    = data_name
        config['poi_name']     = poi_name
        config['do_blind']     = blind
        config['file_expr']    = file_expr
        config['param_expr']   = param_expr
        config['filter_expr']  = filter_expr
        config['exclude_expr'] = exclude_expr
        config['cache']        = cache
        config['parallel']     = parallel
        self._config = config
        self.setup_paths(analysis_name=analysis_name,
                         channel=channel,
                         input_dir=input_dir,
                         output_dir=output_dir)
        self.setup_tasks(tasks)
        self.setup_param_parser()
        self.task_options = task_options
        self._minimizer_options = self.parse_minimizer_options(minimizer_options)
        
        self.sanity_check()

    @staticmethod
    def parse_minimizer_options(self, config_path:Optional[str]=None):
        minimizer_options = {
            'general'      : {},
            'limit'        : {},
            'likelihood'   : {},
            'significance' : {}
        }
        if config_path is not None:
            with open(config_path, "r") as f:
                config = json.load(f)
            if 'general' not in config:
                config['general'] = {}
            for task in config:
                if task != 'general':
                    minimizer_options[task] = combine_dict(config['general'], config[task])
                else:
                    minimizer_options[task] = combine_dict(config[task])
        return minimizer_options
    
    def setup_paths(self, **kwargs):
        self._path_manager = CombinationPathManager(**kwargs)

    def setup_tasks(self, tasks:Optional[List]=None):
        if tasks is None:
            tasks = []
        self._tasks = []
        for task in tasks:
            task = TaskType.parse(task)
            self._tasks.append(task)

    def setup_param_parser(self):
        self._param_parser = ParamParser(format_str=self.config['file_expr'],
                                         param_str=self.config['param_expr'])

    def get_param_points(self):
        raise NotImplementedError("this method should be overridden")
    
    def sanity_check(self):
        pass

    def get_pois_to_keep(self):
        pois_to_keep = []
        pois_to_keep.append(self.config["poi_name"])
        pois_to_keep.extend(self.config["extra_pois"])
        internal_param_points = self.param_parser.get_internal_param_points()
        internal_params = set()
        for param_point in internal_param_points:
            internal_params |= set(param_point)
        pois_to_keep.extend(list(internal_params))
        return pois_to_keep

    def get_runner_default_options(self):
        debug_mode = self.stdout.verbosity == "DEBUG"
        default_options = {
            'input_path'  : self.path_manager.get_directory('workspace'),
            'file_expr'   : self.config['file_expr'],
            'param_expr'  : self.config['param_expr'],
            'filter_expr' : self.config['filter_expr'],
            'exclude_expr': self.config['exclude_expr'],
            'cache'       : self.config['cache'],
            'save_log'    : not debug_mode,
            'parallel'    : self.config['parallel'],
            'verbosity'   : self.stdout.verbosity
        }
        return default_options

    def combine_task_options(self, default_options:Dict, task_options:Dict):
        scenario = task_options['scenario']
        custom_options = {"config":{}}
        for key, value in task_options.get('options', {}).items():
            if key in default_options:
                custom_options[key] = value
            else:
                custom_options['config'][key] = value
        combined_options = combine_dict(default_options, custom_options)
        if ('outdir' in combined_options) and ('outdir' not in custom_options):
            combined_options['outdir'] = os.path.join(combined_options['outdir'], scenario)
        return combined_options

    def run_parameterised_method(self, method:"ParameterisedRunner",
                                 task_name:str,
                                 output_name:str,
                                 extra_options:Optional[Dict]=None,
                                 require_minimization:bool=True):
        tasks = self.task_options.get(task_name, [])
        if not tasks:
            self.stdout.info(f'No jobs scheduled for the task "{task_name}". Skipping.')
            return None
        default_options = self.get_runner_default_options()
        outpath = self.path_manager.get_file(output_name)
        outdir  = os.path.dirname(outpath)
        outname = os.path.basename(outpath)
        default_options.update({
            'outdir'  : outdir,
            'outname' : outname,
            'config'  : {}
        })
        # there might be excessive copying of dictionary but that's ok
        if require_minimization:
            minimizer_options = combine_dict(self.minimizer_options.get(task_name, {}))
            default_options['config'].update(minimizer_options)
        default_options = combine_dict(default_options, extra_options)
        for task_options in tasks:
            scenario = task_options['scenario']
            task_options = self.combine_task_options(default_options, task_options)
            self.stdout.info(f'Executing subtask for the scenario "{scenario}"')
            runner = method(**task_options)
            runner.run()
            
    def run_limit(self):
        from quickstats.concurrent import ParameterisedAsymptoticCLs
        extra_options = {
            'config'  : {
                'poi_name'     : self.config['poi_name'],
                'data_name'    : self.config['data_name'],
                'do_blind'     : self.config['do_blind'],
                'save_summary' : self.stdout.verbosity == "DEBUG"
            }
        }
        self.run_parameterised_method(ParameterisedAsymptoticCLs,
                                      'limit', 'limit_output',
                                      extra_options)

    def run_likelihood(self):
        from quickstats.concurrent import ParameterisedLikelihood
        extra_options = {
            'data_name' : self.config['data_name']
        }
        # TODO: generate asimov for expected likelihood
        self.run_parameterised_method(ParameterisedLikelihood,
                                      'likelihood', 'likelihood_output',
                                      extra_options)

    def run_significance(self):
        from quickstats.concurrent import ParameterisedSignificance
        extra_options = {
            'poi_name'  : self.config['poi_name'],
            'data_name' : self.config['data_name']
        }
        self.run_parameterised_method(ParameterisedSignificance,
                                      'significance', 'significance_output',
                                      extra_options)
        
    def run_tasks(self):
        self.stdout.info(f"Scheduling tasks for the channel: {self.channel}")
        param_points = self.get_param_points()
        total_time = 0
        for task in self.tasks:
            task_name = task.name.lower()
            task_method = getattr(self, f'run_{task_name}')
            if not task_method:
                raise RuntimeError(f'no method defined for the task: {task_name}')
            self.stdout.info(f'Executing task "{task_name}"')
            with Timer() as t:
                # create directory for outputs
                output_type = task.output_type
                if output_type is None:
                    pass
                elif isinstance(output_type, str):
                    self.path_manager.makedirs([output_type])
                else:
                    self.path_manager.makedirs(list(output_type))
                if task.has_runner:
                    task_method()
                else:
                    execute_multi_tasks(task_method, param_points,
                                        parallel=self.config['parallel'])
            self.stdout.info(f"Task finished. Total time taken: {t.interval:.3f} s.")
            total_time += t.interval
        self.stdout.info("Successfully executed all scheduled tasks. "
                         f"Total time taken: {total_time:.3f} s.")