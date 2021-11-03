# copied from RooStatTools/python_modules/LimitSetting.py (Rui Zhang)

import sys
import os
import re
from itertools import repeat
import utils
import ROOT

def CalcLimit_quickstats(workspace_path, poi_name, data_name, output_limit_path, 
                         do_blind=True, do_better_bands=True, CL=0.95, fix_param="",
                         verbose=False, minimizer_options=None, cache=False):
    if minimizer_options is None:
        minimizer_options = {}
    # update the fix param options to cope with both config supplied value and 
    # parameterization supplied value
    if ('fix_param' in minimizer_options) and fix_param:
        minimizer_options['fix_param'] = "{},{}".format(fix_param, minimizer_options['fix_param'])
    elif fix_param:
        minimizer_options['fix_param'] = fix_param
    info_txt = info_txt = '({})'.format(fix_param) if fix_param else ''
    print('INFO: Evaluating limit using quickstats for the workspace {} {}...'.format(workspace_path, info_txt))

    if os.path.exists(output_limit_path) and \
       ((os.environ['HH_COMBINATION_FW_MODE'].lower() == 'skip_exist') or cache):
        print("\033[92mSkip: limit setting output {0} exists, skip limit setting\033[0m".format(output_limit_path))    
        return None
    
    if not verbose:
        # now redirect stdout to log file
        logfile_path = re.sub('\.json', '.log', output_limit_path)
        sys.stdout = open(logfile_path, 'a+')
        ROOT.gSystem.RedirectOutput(logfile_path)
    
    from quickstats.components import AsymptoticCLs
    try:
        asymptotic_cls = AsymptoticCLs(filename=workspace_path, poi_name=poi_name, data_name=data_name,
                                        do_blind=do_blind, do_better_bands=do_better_bands,
                                        CL=float(CL), **minimizer_options)
        asymptotic_cls.evaluate_limits()
        asymptotic_cls.save(output_limit_path)
    except Exception as e:
        print(e)
        raise
    
    if not verbose:
        # recover stdout
        sys.stdout = sys.__stdout__
        ROOT.gROOT.ProcessLine('gSystem->RedirectOutput(0);')
    
    
def CalcLimit_new(mass_point, workspace_path, output_limit_dir, data_name, poi_name=None,
                  do_blind=True, do_better_bands=True, CL=0.95, parameterized_points=None,
                  verbose=False, minimizer_options=None, parallel=-1, cache=False):
    if parameterized_points is None:
        basename = '{0}.json'.format(mass_point)
        output_limit_path = os.path.join(output_limit_dir, basename)
        CalcLimit_quickstats(workspace_path, poi_name, data_name, output_limit_path, 
                             do_blind, do_better_bands, CL, verbose=verbose,
                             minimizer_options=minimizer_options, cache=cache)
    else:
        output_limit_paths = []
        param_expressions = []
        for key in parameterized_points: 
            basename = '{0}_{1}.json'.format(mass_point, key)
            output_limit_path = os.path.join(output_limit_dir, basename)
            output_limit_paths.append(output_limit_path)
            param_expressions.append(parameterized_points[key])
        arguments = (repeat(workspace_path), repeat(poi_name), repeat(data_name),
                     output_limit_paths, repeat(do_blind), repeat(do_better_bands),
                     repeat(CL), param_expressions, repeat(verbose), repeat(minimizer_options),
                     repeat(cache))
        utils.execute_multi_tasks(CalcLimit_quickstats, *arguments, parallel=parallel)



