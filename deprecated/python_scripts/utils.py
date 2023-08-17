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
