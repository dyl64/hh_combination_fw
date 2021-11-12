#!/usr/bin/env python
from typing import Dict, List, Union
import sys
import os
import re
import errno
import csv
import json
import glob
import fnmatch
import itertools
import multiprocessing
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
import numpy as np

class job_manager:

    def __init__(self, func, nProc=8):
        self.task_args = []
        self.func      = func
        self.nProc     = nProc
        self.pool      = Pool(nProc)

    def add_task(self, task_arg):
        self.task_args.append( task_arg)

    def set_task_args(self, task_args):
        self.task_args = task_args

    def submit(self):
        print("Submitting jobs...")
        print("Workers: {0}".format(self.nProc))
        print("Tasks:  {0}".format(len(self.task_args)))
        print("Binary: RooStatTools/python_modules/workspaceCombiner.py:{0} {1}".format(self.func, self.task_args))
        self.pool.map(self.func, self.task_args)



def prog_info():
    print("Running {0}".format(sys.argv[0]))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
            
# will supercede mkdir_p         
def mkdirs(paths):
    for path in paths:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            os.makedirs(path)

def replace_single_token_in_a_file(file, old, new):
    """Replaces a single string token in a file.
       Uses `sed -i 's$old$new$g' <file>`"""

    cmd = "sed -i 's${0}${1}$g' {2}".format(old, new, file)
    os.system(cmd)


def replace_all_tokens(file, tokens):
    """Replaces all tokens in file."""

    for old, new in tokens.items():
        replace_single_token(file, old, new)


def replace_all_tokens_in_string(str, tokens):

    for old, new in tokens.items():
        str = re.sub(old, new, str)

    return str

def create_multiproc_pool(nProc=8):
    """Create a multiprocessing.Pool()."""

    pool = Pool(nProc)
    return pool


def check_if_file_exists(file):
    if not os.path.isfile(file):
        error_msg = "\n#####################\n\
### --- ERROR --- ###\n\
#####################\n\
File {0} is not found!".format(file)
        raise IOError(error_msg)
        exit()



def split_file(input_file_path, nParts, output_prefix, header_lines=0, include_header=False):

    line_count = 0
    with open(input_file_path, 'r') as inp:
        reader = csv.DictReader(inp, delimiter=' ')
        line_count = sum(1 for row in reader)

    with open(input_file_path, 'r') as inp:
        reader = csv.DictReader(inp, delimiter=' ')
        header = reader.fieldnames
        nLinesPerPart = int(line_count/nParts)

        for i in range(nParts):
            file = "{0}{1:03d}".format(output_prefix, i)

            with open(file, 'w') as out:
                writer = csv.DictWriter(out, delimiter=' ', fieldnames=header)
                writer.writeheader()
                for i in range(nLinesPerPart):
                    writer.writerow(reader.next())
        

def save_to_json(dict, f_out_path):
    with open(f_out_path, 'w') as f_out:
        json.dump(dict, f_out, indent=4)
    print("Saved to {}".format(f_out_path))


def load_from_json(json_path):
    with open(json_path, 'r') as f_in:
        dict = json.load(f_in)
    print('Loaded {}'.format(json_path))
    return dict


def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i
        
def pretty_float(val:Union[str, float])->Union[int, float]:
    if float(val).is_integer():
        return int(float(val))
    return float(val)
        
def approx_n_digit(val, default=5):
    s = str(val)
    if not s.replace('.','',1).isdigit():
        return default
    elif '.' in s:
        return len(s.split('.')[1])
    else:
        return 0
    
def str_encode_value(val, n_digit=None, formatted=True):
    if n_digit is not None:
        val_str = '{{:.{}f}}'.format(n_digit).format(val)
        # account for the case where val is negative zero
        if val_str == '-{{:.{}f}}'.format(n_digit).format(0):
            val_str = '{{:.{}f}}'.format(n_digit).format(0)
    else:
        val_str = str(val)
    
    if formatted:
        val_str = val_str.replace('.', 'p').replace('-', 'n')
    return val_str

def str_decode_value(val_str):
    val = float(val_str.replace('p','.').replace('n','-'))
    return val


def get_paramterized_points(param_expr):
    points = {}
    single_expr = param_expr.split(',')
    for expr in single_expr:
        tokens = expr.split('=')
        if len(tokens) != 2:
            raise ValueError('invalid expression for parameterization')
        param_name = tokens[0]
        values_expr = tokens[1]
        points[param_name] = {}
        tokens = values_expr.split('_')
        # fixed value
        if len(tokens) == 1:
            values = [float(tokens[0])]
            n_digit = approx_n_digit(tokens[0])
        # scan across range
        elif len(tokens) == 3:
            poi_min = float(tokens[0])
            poi_max = float(tokens[1])
            poi_step = float(tokens[2])
            n_digit = approx_n_digit(tokens[2])
            values = np.arange(poi_min, poi_max+poi_step, poi_step)
        else:
            raise ValueError('invalid expression for parameterization')
        points[param_name] = [str_encode_value(value, n_digit, False) for value in values]
    # for unordered dictionary in case of python2
    param_names = list(points.keys())
    combinations = [points[param_name] for param_name in param_names]
    combinations = itertools.product(*combinations)
    combined_points = {}
    for combination in combinations:
        val_repr = ','.join(["{}={}".format(p, v) for p, v in zip(param_names, combination)])
        str_repr = '_'.join(["{}_{}".format(p, str_encode_value(v)) for p, v in zip(param_names, combination)])
        combined_points[str_repr] = val_repr
    return combined_points


def get_cpu_count():
    return multiprocessing.cpu_count()

def parallel_run(func, *iterables, max_workers):

    with ProcessPoolExecutor(max_workers) as executor:
        result = executor.map(func, *iterables)

    return [i for i in result]

def execute_multi_tasks(func, *iterables, parallel):
    if parallel == 0:
        result = []
        for args in zip(*iterables):
            result.append(func(*args))
        return result
    else:
        if parallel == -1:
            max_workers = get_cpu_count()
        else:
            max_workers = parallel
        return parallel_run(func, *iterables, max_workers=max_workers)

def filter_by_expression(source, expr=None):
    if expr is None:
        return source
    patterns = expr.split(',')
    keep = []
    for item in source:
        if any(fnmatch.fnmatch(item, pattern) for pattern in patterns):
            keep.append(item)
    return keep

def get_mass_points(ws_dir, mass_expr=None, file_expr=None):
    ws_files = glob.glob(os.path.join(ws_dir, '*.root'))
    mass_points = []
    if file_expr is None:
        mass_regex = re.compile(r'(\d+).root')
    else:
        mass_regex = re.compile(file_expr)
    for ws_file in ws_files:
        basename = os.path.basename(ws_file)
        match = mass_regex.match(basename)  
        if match:
            mass = match.group(1)
            mass_points.append(mass)
     
    mass_points = filter_by_expression(mass_points, mass_expr)
    mass_points = sorted(mass_points, key=float)
    return mass_points


def get_channel_mass_points(base_dir, channels, mass_expr=None, file_expr=None):
    channel_mass_points = {}
    all_mass_points = set()
    for channel in channels:
        ws_dir = os.path.join(base_dir, channel)
        if not os.path.exists(ws_dir):
            raise FileNotFoundError('workspace directory "{}" does not exist'.format(ws_dir))
        channel_mass_points[channel] = get_mass_points(ws_dir, mass_expr, file_expr)
        all_mass_points |= set(channel_mass_points[channel])
    all_mass_points = sorted(list(all_mass_points), key=float)
    # result format:  {mass_points : available channels}
    result = {mass: [] for mass in all_mass_points}
    for channel in channel_mass_points:
        for mass in channel_mass_points[channel]:
            result[mass].append(channel)
    return result


def str_decode_value(val_str):
    val = float(val_str.replace('p','.').replace('n','-'))
    return val

signature_map = {
    'F': r"\d+[.]?\d*",
    'P': r"n?\d+p?\d*",
    'S': r"\w+"
}

signature_parser = {
    'F': pretty_float,
    'P': str_decode_value,
    'S': str
}

def format_str_to_regex(format_str:str):
    expr = format_str
    attribute_groups = re.findall(r"<(\w+)\[(\w)\]>", format_str)
    for token in attribute_groups:
        attribute = token[0]
        signature = token[1]
        attribute_expr = signature_map.get(signature.upper(), None)
        if attribute_expr is None:
            raise ValueError(f"unknown signature `{signature}`")
        group_expr = f"(?P<{attribute}>{attribute_expr})"  
        expr = expr.replace(f"<{attribute}[{signature}]>", group_expr)
    expr += '.root'
    regex = re.compile(expr)
    return regex

def filter_param_points(param_points:List[Dict], filter_expr:str=None):
    if filter_expr is None:
        return param_points
    patterns = {k: v.split(',') for k,v in filter_expr.items()}
    passed_points = []
    for point in param_points:
        passed = True
        for key in patterns:
            attrib_val = point[key]
            passed &= any(fnmatch.fnmatch(attrib_val, pattern) for pattern in patterns[key])
        if passed:
            passed_points.append(point)
    return passed_points

def get_format_str_components(format_str:str):
    attribute_groups = re.findall(r"<(\w+)\[(\w)\]>", format_str)
    components = {}
    for token in attribute_groups:
        components[token[0]] = token[1]
    return components

def sort_param_points(param_points, format_str:str):
    components = get_format_str_components(format_str)
    lambda_sort_keys = []
    for name in components:
        signature = components[name]
        parser = signature_parser.get(signature, None)
        if parser is None:
            raise ValueError(f"unknown signature `{signature}`")
        lambda_sort_key = lambda d: parser(d[name])
        lambda_sort_keys.append(lambda_sort_key)
    key = lambda d: tuple(l(d) for l in lambda_sort_keys)
    return sorted(param_points, key=key)

def get_param_points(ws_dir:str, filter_expr:Dict=None, file_format:str=None):
    ws_files = glob.glob(os.path.join(ws_dir, '*.root'))
    param_points = []
    if file_format is None:
        file_format = "<mass[F]>"
    regex = format_str_to_regex(file_format)
   
    for ws_file in ws_files:
        basename = os.path.basename(ws_file)
        match = regex.match(basename)
        if match:
            # strip off extension for name reformatting
            point = {'basename': basename.replace(".root", "")}
            point.update(match.groupdict())
            param_points.append(point)
    param_points = filter_param_points(param_points, filter_expr)
    param_points = sort_param_points(param_points, file_format)
    return param_points

def get_channel_param_points(base_dir:str, channels:List, filter_expr:Dict=None, file_format:str=None, min_num_channels=None):
    channel_param_points = {}
    for channel in channels:
        ws_dir = os.path.join(base_dir, channel)
        if not os.path.exists(ws_dir):
            raise FileNotFoundError('workspace directory "{}" does not exist'.format(ws_dir))
        param_points = get_param_points(ws_dir, filter_expr, file_format)
        for param_point in param_points:
            hash_value = tuple(param_point.values())
            if hash_value not in channel_param_points:
                channel_param_points[hash_value] = param_point
                channel_param_points[hash_value]['channels'] = []
            channel_param_points[hash_value]['channels'].append(channel)
    channel_param_points = list(channel_param_points.values())
    if min_num_channels is not None:
        temp = []
        for param_point in channel_param_points:
            if len(param_point['channels']) >= min_num_channels:
                temp.append(param_point)
        channel_param_points = temp
    channel_param_points = sort_param_points(channel_param_points, file_format)
    return channel_param_points

def format_param_point(param_point:Dict):
    result = ', '.join(["{} = {}".format(k, v) for k, v in param_point.items() if k not in ['basename', 'channels']])
    result = '(' + result + ')'
    return result
