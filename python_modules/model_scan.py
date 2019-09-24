 #!/usr/bin/env python

import os
import sys
import csv
import json
import re
import logging

import aux_utils as utils
import physics as phy
import workspaceCombiner as wsc
import LimitSetting as ls
import parameter_space as ps
from parameter_space import parameter_point as param_pt
import correlation_scheme as cs

import sge_scheduler as sge
import lsf_scheduler as lsf
import condor_scheduler as condor


mass_pts = {
             'spin0' :
             {
               'bbbb':     [260,275,300,325,350,400,450,500,550,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800,2000,2250,2500,2750,3000],
               'bbtautau': [260,275,300,325,350,400,450,500,550,600,700,800,900,1000],
               'bbyy':     [260,275,300,325,350,400,450,500,550,600,700,800,900,1000],
               'WWWW':     [260,275,300,325,350,400,450,500],
               # test 5 channels
               #'bbbb':     [260,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800,2000,2250,2500,2750,3000],
               #'bbtautau': [260,300,400,500,600,700,800,900,1000],
               #'bbyy':     [260,300,400,500,600,700,800,900,1000],
               #'WWyy':     [260,300,400,500],
               #'bbWW':     [500,600,700,800,900,1000],
             }
           }


models = {
           'hMSSM' : {'search_particle' : 'H', 'parameters' : ['mA', 'tanb']},
           'EWS'   : {'search_particle' : 'H', 'parameters' : ['mH', 'cba', 'tanb']}
         }

new_poiname = 'xsec_br_model_rescaled'


def find_nearest_neighbours(mass, type, channel):
    """Very basic function to find nearest neighbours."""

    available_pts = mass_pts[type][channel]

    isFound = False
    idx = 0

    while not isFound and idx < (len(available_pts)-1):

        low = available_pts[idx]
        high  = available_pts[idx+1]

        if low < mass and high > mass:
            isFound = True
        idx += 1

    if isFound:
        return low, high
    else:
        return False, False


def br_hh_XXYY_modifier(br_hh_XXYY, XXYY):

    br_hh_XXYY_SM = phy.br_hh[XXYY]
    modifier = br_hh_XXYY/br_hh_XXYY_SM
    return modifier 

######################################
### --- Keys, labels and reprs --- ###
######################################

### --- Types:
###   - label: file labels
###   - key: dictionary keys
###   - repr: printable representation

def get_key_br_hh(ch):
    """Returns the Di-Higgs branching ratio key.
    Example: br_hh_bbbb"""
    return 'br_hh_{}'.format(ch)


def get_mass_neighbour_key(model, ch, neighbour):
    """Returns the mass neighbour key.
    Example: mH_bbbb_low"""

    mass_label = get_search_particle_mass_key(model)
    return '{}_{}_{}'.format(mass_label, neighbour, ch)


def get_search_particle_mass_key(model):
    """Returns the mass label for the search particle in question.
    Example: mH"""
    return "m{}".format(models[model]['search_particle'])

########################################
### --- model scan manager class --- ###
########################################

class model_scan_manager:

    def __init__(self, scan_run_dir, model, type, channels, scan_points_path, original_workspaces_dir, nJobs, job_options, job_task_path, correlation_scheme_version, job_log_dir=None, init=False):

        job_manager_config_path = os.path.join(scan_run_dir, 'job_manager.cfg')

        # - Common configuration
        # - (this is passed onto the config of the individual jobs)
        self.common_config = {
                               'scan_run_dir' : scan_run_dir,
                               'model'        : model,
                               'type'         : type,
                               'channels'     : channels,
                               'original_workspaces_dir' : original_workspaces_dir,
                               'job_manager_config_path'  : job_manager_config_path,
                               'job_options'  : job_options,
                               'job_task_path'     : job_task_path,
                               'xsec_to_be_compared' : ps.models[model]['xsec_to_be_compared'],
                               'correlation_scheme_version' : correlation_scheme_version,
                              }


        self.full_config = dict(self.common_config)
        self.full_config['scan_points_path']          = scan_points_path
        self.full_config['scan_points_appended_path'] = os.path.join(scan_run_dir, 'scan_pts.dat')
        self.full_config['list_of_job_processed_pts']   = os.path.join(scan_run_dir, 'list_of_job_processed_pts.txt')
        self.full_config['result_pts_path'] = os.path.join(scan_run_dir, 'result_pts.dat')
        self.full_config['job_log_dir']               = os.path.join(scan_run_dir, './job_logs/') if job_log_dir is None else job_log_dir
        self.full_config['nJobs']                     = nJobs

        self.full_config['jobs']                      = {}

        if init:

            utils.mkdir_p(self.scan_run_dir)
            utils.mkdir_p(self.job_log_dir)

            self.display_config()

            for id in range(nJobs):
                self.init_job(id)

            with open(self.job_manager_config_path, 'w') as job_mgr_cfg:
                json.dump(self.full_config, job_mgr_cfg, indent=2) 

            print("Jobs initialised.")

    @classmethod
    def from_manager_config(cls, job_manager_config_path):

        with open(job_manager_config_path, 'r') as cfg:
            full_config = json.load(cfg)
            scan_run_dir = full_config['scan_run_dir']
            model = full_config['model']
            type = full_config['type']
            channels = full_config['channels']
            scan_points_path = full_config['scan_points_path']
            original_workspaces_dir = full_config['original_workspaces_dir']
            nJobs = full_config['nJobs']
            job_options = full_config['job_options']
            job_task_path = full_config['job_task_path']
            correlation_scheme_version = full_config['correlation_scheme_version']

            return cls(scan_run_dir, model, type, channels, scan_points_path, original_workspaces_dir, nJobs, job_options, job_task_path, correlation_scheme_version, init=False)

    def display_config(self):

        print("model:        {}".format(self.model))
        print("type:         {}".format(self.type))
        print("channels:     {}".format(self.channels))
        print("scan_run_dir: {}".format(self.scan_run_dir))
        print("nJobs:        {}".format(self.nJobs))

    # - class variabales
    def __getitem__(self, key):
        return self.full_config[key]

    def __setitem__(self, key, value):
        self.full_config[key] = value

    def __getattr__(self, name):
        return self.full_config[name]

    def generate_job_name(self, job_id):
        job_name = "job_{0:03d}".format(job_id)
        return job_name

    def init_job(self, id):
        """Initialise a job with id"""

        job_name = self.generate_job_name(id)
            
        # - Hard copy of the dict
        job_options = dict(self.common_config)
        job_dir = os.path.join(self.scan_run_dir, job_name)
        job_scan_pts_path = os.path.join(job_dir, 'scan_pts_list.dat')
        job_processed_pts_path = os.path.join(job_dir, 'scan_processed_pts.dat')
    
        # - Directories to be created
        rescaled_dir    = os.path.join(self.scan_run_dir, job_name, 'rescaled')
        combined_dir    = os.path.join(self.scan_run_dir, job_name, 'combined')
        limits_dir      = os.path.join(self.scan_run_dir, job_name, 'limits')
        cfg_rescale_dir = os.path.join(self.scan_run_dir, job_name, 'cfg', 'rescale')
        cfg_combine_dir = os.path.join(self.scan_run_dir, job_name, 'cfg', 'combine')

        job_config_file_name = "{}.cfg".format(job_name) 
        job_config_file_path = os.path.join(job_dir, job_config_file_name)

        job_log_file_name = "{}.log".format(job_name) 
        job_log_file_path = os.path.join(job_dir, job_log_file_name)

        # - Create directories
        dirs_to_be_created = []
        dirs_to_be_created.append(job_dir)
        dirs_to_be_created.append(rescaled_dir)
        dirs_to_be_created.append(combined_dir)
        dirs_to_be_created.append(limits_dir)
        dirs_to_be_created.append(cfg_rescale_dir)
        dirs_to_be_created.append(cfg_combine_dir)
        for dir in dirs_to_be_created:
            utils.mkdir_p(dir)
    
        # - Update a scan run options
        job_options['job_name']          = job_name
        job_options['id']                = id
        job_options['job_dir']           = job_dir
        job_options['rescaled_dir']      = rescaled_dir
        job_options['cfg_rescale_dir']   = cfg_rescale_dir
        job_options['cfg_combine_dir']   = cfg_combine_dir
        job_options['combined_dir']      = combined_dir
        job_options['limits_dir']        = limits_dir
        job_options['job_scan_pts_path']      = job_scan_pts_path
        job_options['job_processed_pts_path'] = job_processed_pts_path
        job_options['job_config_file_path']   = job_config_file_path
        job_options['job_log_file_path']      = job_log_file_path

        wsc.copy_organization_dtd(cfg_rescale_dir)
        wsc.copy_combination_dtd(cfg_combine_dir)
    
        self.write_job_config_file(job_options)
        self.jobs[job_name] = job_options
    

    def write_job_config_file(self, job_options):

        job_config_file_path = job_options['job_config_file_path']
        
        with open(job_config_file_path, 'w') as outfile:
            json.dump(job_options, outfile, indent=2) 


    def append_with_mass_pt_neighbours(self):
    
        mass_label = get_search_particle_mass_key(self.model)
        nLines = 0
    
        with open(self.scan_points_path, 'rb') as in_file:
            reader = csv.DictReader(in_file, delimiter=' ')
            header = reader.fieldnames
            print(header)
    
            for ch in self.channels:
                key_low  = "{}_low_{}".format(mass_label, ch)
                key_high = "{}_high_{}".format(mass_label, ch)
                header.append(key_low)
                header.append(key_high)
        
            with open(self.scan_points_appended_path, 'w') as out_file:
                writer = csv.DictWriter(out_file, delimiter=' ', fieldnames=header)
                writer.writeheader()
    
                for row in reader:
                    mass = float(row[mass_label])
                    writeRow = True
    
                    if mass == 'nan':
                        writeRow = False
                    for ch in self.channels:
                        low, high = find_nearest_neighbours(mass, self.type, ch)
                        key_low  = "{}_low_{}".format(mass_label, ch)
                        key_high = "{}_high_{}".format(mass_label, ch)           
                        if low and high:

                            row[key_low]  = low
                            row[key_high] = high
                        else:
                            row[key_low]  = 'outside'
                            row[key_high] = 'outside'
                            pt = param_pt.from_dict(self.model, row) 
                            print("{}: {} outside the range. Discarding point {}".format(mass_label, mass, pt))
                            writeRow = True
                    
                    if writeRow:
                        writer.writerow(row)
                        nLines += 1


    def distribute_scan_pts_among_jobs(self):

        print("Distributing parameter space points:")
    
        line_count = 0
        with open(self.scan_points_appended_path, 'r') as inp:
            reader = csv.DictReader(inp, delimiter=' ')
            line_count = sum(1 for row in reader)
    
        with open(self.scan_points_appended_path, 'r') as inp:
            reader = csv.DictReader(inp, delimiter=' ')
            header = reader.fieldnames
            nLinesPerPart = int(line_count/self.nJobs)
    
            for job_name, options in self.jobs.items():
    
                job_scan_pts_path = options['job_scan_pts_path']
    
                with open(job_scan_pts_path, 'w') as out:
                    print("- Now writing to {}".format(job_scan_pts_path))
                    writer = csv.DictWriter(out, delimiter=' ', fieldnames=header)
                    writer.writeheader()
                    for i in range(nLinesPerPart):
                        writer.writerow(reader.next())


    def write_process_pts_list(self):
        with open(self.list_of_job_processed_pts, 'w') as out:
            for job_id, options in self.jobs.items():
                processed_pts_path = options['job_processed_pts_path']
                out.write("{}\n".format(processed_pts_path))

    def submit_jobs_sge(self):
        """Submits jobs using the Sun Grid Engine job scheduler (qsub)."""

        print("Submitting jobs:")
        print(self.full_config)

        for job_id, options in self.jobs.items():
            task_args = options['job_config_file_path']
            print("- Submitting {}..".format(job_id))
            
            if 'resources' in self.job_options:
                resources = self.job_options['resources']
            else:
                resources = None
            if 'machines' in self.job_options:
                machines = self.job_options['machines']
            else:
                machines = None

            sge.submit_job(self.job_task_path, task_args=task_args, log_dir=self.job_log_dir, job_name=job_id, resources=resources,
                            machines=machines)

    def submit_jobs_lsf(self):
        """Submits jobs using the LSF job scheduler (bsub)."""

        print("Submitting jobs:")
        print(self.full_config)

        for job_id, options in self.jobs.items():
            task_args = options['job_config_file_path']
            print("- Submitting {}..".format(job_id))
            
            if 'resources' in self.job_options:
                resources = self.job_options['resources']
            else:
                resources = None
            if 'machines' in self.job_options:
                machines = self.job_options['machines']
            else:
                machines = None

            lsf.submit_job(self.job_task_path, task_args=task_args, log_dir=self.job_log_dir, job_name=job_id, resources=resources,
                            machines=machines)

    def submit_jobs_condor(self):
        """Submits jobs using condor."""

        print("Submitting jobs:")
        print(self.full_config)

        for job_id, options in self.jobs.items():
            task_args = options['job_config_file_path']
            job_dir = options['job_dir']
            print("- Submitting {}..".format(job_id))
            
            condor.submit_job(self.job_task_path, task_args=task_args, job_name=job_id, log_dir=self.job_log_dir)


    def pool_results(self):
        with open(self.result_pts_path, 'w') as out:
            with open(self.list_of_job_processed_pts, 'r') as f_list:

                # - Header
                job_processed_pts_path = f_list.readline().rstrip()
                # in case the job fails and no line in the file
                while os.stat(job_processed_pts_path).st_size == 0:
                    job_processed_pts_path = f_list.readline().rstrip()
                print("Opening file: {}".format(job_processed_pts_path))
                with open(job_processed_pts_path, 'r') as job_processed_pts:
                    out.write(job_processed_pts.readline())

                # - Points
                f_list.seek(0)
                n_pts_total = 0
                for file in f_list:
                    job_processed_pts_path = file.rstrip()
                    if os.stat(job_processed_pts_path).st_size == 0:
                        print('Scan point file has size 0: {} skip'.format(job_processed_pts_path))
                        continue
                    print("Opening file: {}".format(job_processed_pts_path))
                    n_pts = 0
                    with open(job_processed_pts_path, 'r') as job_processed_pts:
                        job_processed_pts.next()
                        for line in job_processed_pts:
                            out.write(line)
                            n_pts += 1
                    print('File has {} successful scan points'.format(n_pts))
                    n_pts_total += n_pts
                n_pts_total_plan = sum(1 for line in open(self.scan_points_appended_path)) - 1
                print('In total, successful/planned scan points: {}/{}'.format(n_pts_total,n_pts_total_plan))




####################################
### --- model scan job class --- ###
####################################

class scan_job:

    def __init__(self, job_config_path):

        self.job_config_path = job_config_path
        with open(job_config_path, 'r') as inp:
            self.job_config = json.load(inp)
            
        self.logger  = logging.getLogger(self.job_name)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        file_handler = logging.FileHandler(self.job_log_file_path, mode='w')
        
        file_handler.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

        self.logger.info("--------------------")
        self.logger.info("Job config {} loaded".format(self.job_config_path))


        #sys.stdout = open(job_log_file_path, "w")
        #sys.stdout.flush()

    def __getitem__(self, key):
        return self.job_config[key]

    def __getattr__(self, name):
        return self.job_config[name]


    def add_new_cols_to_header(self, header, channels):

        header.append('limit_combined_m1s_interpolated')
        header.append('limit_combined_m2s_interpolated')
        header.append('limit_combined_exp_interpolated')
        header.append('limit_combined_p1s_interpolated')
        header.append('limit_combined_p2s_interpolated')
        header.append('limit_combined_obs_interpolated')
        theory_over_limit_combined_m1s_ratio_key = "{}_over_limit_combined_m1s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_m2s_ratio_key = "{}_over_limit_combined_m2s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_exp_ratio_key = "{}_over_limit_combined_exp".format(self.xsec_to_be_compared)
        theory_over_limit_combined_p1s_ratio_key = "{}_over_limit_combined_p1s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_p2s_ratio_key = "{}_over_limit_combined_p2s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_obs_ratio_key = "{}_over_limit_combined_obs".format(self.xsec_to_be_compared)

        header.append(theory_over_limit_combined_m1s_ratio_key)
        header.append(theory_over_limit_combined_m2s_ratio_key)
        header.append(theory_over_limit_combined_exp_ratio_key)
        header.append(theory_over_limit_combined_p1s_ratio_key)
        header.append(theory_over_limit_combined_p2s_ratio_key)
        header.append(theory_over_limit_combined_obs_ratio_key)

        for ch in self.channels:
            limit_ch_m1s_interpolated_key = 'limit_{}_m1s_interpolated'.format(ch)
            limit_ch_m2s_interpolated_key = 'limit_{}_m2s_interpolated'.format(ch)
            limit_ch_exp_interpolated_key = 'limit_{}_exp_interpolated'.format(ch)
            limit_ch_p1s_interpolated_key = 'limit_{}_p1s_interpolated'.format(ch)
            limit_ch_p2s_interpolated_key = 'limit_{}_p2s_interpolated'.format(ch)
            limit_ch_obs_interpolated_key = 'limit_{}_obs_interpolated'.format(ch)
            theory_over_limit_ch_m1s_ratio_key= "{}_over_limit_{}_m1s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_m2s_ratio_key= "{}_over_limit_{}_m2s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_exp_ratio_key= "{}_over_limit_{}_exp".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_p1s_ratio_key= "{}_over_limit_{}_p1s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_p2s_ratio_key= "{}_over_limit_{}_p2s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_obs_ratio_key= "{}_over_limit_{}_obs".format(self.xsec_to_be_compared, ch)
            header.append(limit_ch_m1s_interpolated_key)
            header.append(limit_ch_m2s_interpolated_key)
            header.append(limit_ch_exp_interpolated_key)
            header.append(limit_ch_p1s_interpolated_key)
            header.append(limit_ch_p2s_interpolated_key)
            header.append(limit_ch_obs_interpolated_key)
            header.append(theory_over_limit_ch_m1s_ratio_key)
            header.append(theory_over_limit_ch_m2s_ratio_key)
            header.append(theory_over_limit_ch_exp_ratio_key)
            header.append(theory_over_limit_ch_p1s_ratio_key)
            header.append(theory_over_limit_ch_p2s_ratio_key)
            header.append(theory_over_limit_ch_obs_ratio_key)

        return header


    def process_param_pts(self):
    
        with open(self.job_scan_pts_path, 'r') as inp:
            reader = csv.DictReader(inp, delimiter=' ')

            header = reader.fieldnames
            header = self.add_new_cols_to_header(header, self.channels)
            with open(self.job_processed_pts_path, 'w') as out:
                writer = csv.DictWriter(out, delimiter=' ', fieldnames=header)
                writer.writeheader()
                out.flush()
                self.logger.info("--------------------")
                self.logger.info("Writing processed points to {}".format(self.job_processed_pts_path))
                self.logger.info("--")
                self.logger.info("Processing points:")
    
                for pt in reader:
                    pt = param_pt.from_dict(self.model, pt)
                    self.logger.info("- point: {}".format(pt))
                    pt = self.process_param_pt(pt)
                    self.logger.debug("----------- header -------------- ")
                    self.logger.debug(header)
                    self.logger.debug("----------------------------------")
                    self.logger.debug("--- pt.print_all_parameteres() ---")
                    pt.print_all_parameters()
                    self.logger.debug("----------------------------------")
                    writer.writerow(pt.parameters)
                    out.flush()
                    sys.stdout.flush()

    def get_mass_neighbour(self, pt, channel, neighbour):
        mass_neighbour_key = get_mass_neighbour_key(self.model, channel, neighbour)
        mass_neighbour     = pt[mass_neighbour_key]
        return mass_neighbour


    def get_channel_neighbour_basename(self, pt, channel, neighbour):
        """Returns channel mass point neighbour basename.
        Example: mA_300.0_tanb_2.0_mH_bbbb_low_260"""

        # - keys
        mass_neighbour_key = get_mass_neighbour_key(self.model, channel, neighbour)
        mass_label = get_search_particle_mass_key(self.model)
        mass_neighbour = pt[mass_neighbour_key]

        # - Filename
        basename = "{}_{}_{}_{}_{}".format(pt, mass_label, neighbour, mass_neighbour, channel)

        return basename


    def get_neighbour_basename(self, pt, neighbour):
        """Returns channel mass point neighbour basename.
        Example: mA_300.0_tanb_2.0_mH_bbbb_low_260"""

        # - keys
        mass_key = get_search_particle_mass_key(self.model)
        mass_neighbour_key = "{}_{}_{}".format(mass_key, neighbour, self.channels[0])
        mass_neighbour = pt[mass_neighbour_key]

        # - Filename
        basename = "{}_{}_{}_{}".format(pt, mass_key, neighbour, mass_neighbour)

        return basename


    def get_cfg_rescale_path(self, pt, channel, neighbour):
    
        basename = self.get_channel_neighbour_basename(pt, channel, neighbour)
    
        # - Filename
        filename = "{}.cfg".format(basename)
        cfg_rescale_path = os.path.join(self.cfg_rescale_dir, filename)
    
        return cfg_rescale_path

    def get_cfg_combine_path(self, pt, neighbour):
    
        basename = self.get_neighbour_basename(pt, neighbour)
    
        # - Filename
        filename = "{}.cfg".format(basename)
        cfg_combine_path = os.path.join(self.cfg_combine_dir, filename)
    
        return cfg_combine_path

    def get_combined_ws_path(self, pt, neighbour):
    
        basename = self.get_neighbour_basename(pt, neighbour)
    
        # - Filename
        filename = "{}.root".format(basename)
        combined_ws_path = os.path.join(self.combined_dir, filename)
    
        return combined_ws_path

    def get_rescaled_workspace_path(self, pt, channel, neighbour):
    
        basename = self.get_channel_neighbour_basename(pt, channel, neighbour)
    
        # - Filename
        filename = "{}.root".format(basename)
        rescaled_workspace_path = os.path.join(self.rescaled_dir, filename)
    
        return rescaled_workspace_path

    def get_input_workspace_path(self, pt, channel, neighbour):
    
        mass_neighbour = self.get_mass_neighbour(pt, channel, neighbour)
        workspace_name = "{0:d}.root".format(int(mass_neighbour))
        input_workspace_path = os.path.join(self.original_workspaces_dir, channel, workspace_name)
    
        return input_workspace_path

    def create_channels_options_for_combination(self, pt, neighbour):

        channels_options =  {}

        for ch in self.channels:
            channel_options = {}
            rescaled_ws_path = self.get_rescaled_workspace_path(pt, ch, neighbour)
            channel_options['input_ws_path'] = rescaled_ws_path
            if isinstance( self.correlation_scheme_version, str ):
                # if str, same scheme for all
                channel_options['scheme_file'] = cs.get_scheme_file_path(ch, self.correlation_scheme_version)
            else:
                # if not str, then dict, ch:'scheme' per channel
                channel_options['scheme_file'] = cs.get_scheme_file_path(ch, self.correlation_scheme_version[ch] )
            channels_options[ch] = channel_options

        return channels_options
    
    def process_param_pt(self, pt):

        mass_key = get_search_particle_mass_key(self.model)
        mass = float(pt[mass_key])

        mass_neighbour = self.get_mass_neighbour(pt, self.channels[0], 'low')
        if  mass_neighbour == 'outside':
            return pt
    
        for ch in self.channels:
            
            br_hh_XXYY_model = float(pt[get_key_br_hh(ch)])
            scaling = 1.0/br_hh_XXYY_modifier(br_hh_XXYY_model, ch)
            
            limit_pts = {}
    
            for neighbour in ['low', 'high']:

                mass_neighbour = self.get_mass_neighbour(pt, self.channels[0], neighbour)

                ### --- Rescaling --- ###
                rescaled_workspace_path  = self.get_rescaled_workspace_path(pt, ch, neighbour)
                rescale_cfg_file_path    = self.get_cfg_rescale_path(pt, ch, neighbour)
                input_workspace_path     = self.get_input_workspace_path(pt, ch, neighbour)

                rescale_logfile_path = re.sub('\.root', '.log', rescaled_workspace_path)
                wsc.create_rescale_config_file(wsc.wsc_rescale_config_template,
                                               rescale_cfg_file_path,
                                               input_workspace_path,
                                               rescaled_workspace_path,
                                               new_poiname,
                                               scaling,
                                               oldpoi_equivalent_name='mu_SM_normalized')

                wsc.run_edit_workspace(rescale_cfg_file_path, rescale_logfile_path)
                output_limit_NP_nom_path = os.path.join(self.limits_dir, "{}_{}_{}_exp.dat".format(pt, ch, neighbour))
                output_limit_NP_fit_path = os.path.join(self.limits_dir, "{}_{}_{}_obs.dat".format(pt, ch, neighbour))
                output_limit_combined_path = os.path.join(self.limits_dir, "{}_{}_{}.dat".format(pt, ch, neighbour))
                limit_pt = ls.LimitPoint.from_single_workspace_NP_nom_and_fit_on_the_fly(rescaled_workspace_path, output_limit_NP_nom_path, output_limit_NP_fit_path, output_limit_combined_path)
                limit_pts[neighbour] = { 'mass': mass_neighbour, 'limit_pt': limit_pt}
            
            limit_ch_m1s_interpolated, limit_ch_m2s_interpolated, limit_ch_exp_interpolated, limit_ch_p1s_interpolated, limit_ch_p2s_interpolated, limit_ch_obs_interpolated = interpolate_limits_pts(limit_pts, mass)

            limit_ch_m1s_key = "limit_{}_m1s_interpolated".format(ch)
            limit_ch_m2s_key = "limit_{}_m2s_interpolated".format(ch)
            limit_ch_exp_key = "limit_{}_exp_interpolated".format(ch)
            limit_ch_p1s_key = "limit_{}_p1s_interpolated".format(ch)
            limit_ch_p2s_key = "limit_{}_p2s_interpolated".format(ch)
            limit_ch_obs_key = "limit_{}_obs_interpolated".format(ch)

            theory_over_limit_ch_m1s_ratio_key = "{}_over_limit_{}_m1s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_m2s_ratio_key = "{}_over_limit_{}_m2s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_exp_ratio_key = "{}_over_limit_{}_exp".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_p1s_ratio_key = "{}_over_limit_{}_p1s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_p2s_ratio_key = "{}_over_limit_{}_p2s".format(self.xsec_to_be_compared, ch)
            theory_over_limit_ch_obs_ratio_key = "{}_over_limit_{}_obs".format(self.xsec_to_be_compared, ch)

            self.logger.debug("limit_ch_exp_interpolated: {}".format(limit_ch_exp_interpolated))
            self.logger.debug("limit_ch_obs_interpolated: {}".format(limit_ch_obs_interpolated))

            pt[limit_ch_m1s_key] = limit_ch_m1s_interpolated
            pt[limit_ch_m2s_key] = limit_ch_m2s_interpolated
            pt[limit_ch_exp_key] = limit_ch_exp_interpolated
            pt[limit_ch_p1s_key] = limit_ch_p1s_interpolated
            pt[limit_ch_p2s_key] = limit_ch_p2s_interpolated
            pt[limit_ch_obs_key] = limit_ch_obs_interpolated

            pt[theory_over_limit_ch_m1s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_ch_m1s_interpolated)
            pt[theory_over_limit_ch_m2s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_ch_m2s_interpolated)
            pt[theory_over_limit_ch_exp_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_ch_exp_interpolated)
            pt[theory_over_limit_ch_p1s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_ch_p1s_interpolated)
            pt[theory_over_limit_ch_p2s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_ch_p2s_interpolated)
            pt[theory_over_limit_ch_obs_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_ch_obs_interpolated)

            sys.stdout.flush()


        ### --- Combination --- ###

        limit_pts = {}

        for neighbour in ['low', 'high']:

            mass_neighbour = self.get_mass_neighbour(pt, self.channels[0], neighbour)
        
            cfg_combine_path       = self.get_cfg_combine_path(pt, neighbour)
            output_ws_path         = self.get_combined_ws_path(pt, neighbour)
            input_prepath          = self.original_workspaces_dir
            input_path_placeholder = "{0}/{1}.root"

            combination_channels_options = self.create_channels_options_for_combination(pt, neighbour)
            comb = wsc.CombinePoint(mass, cfg_combine_path, output_ws_path, combination_channels_options, POI_name='xsec_br_model_rescaled')

#           comb = wsc.CombinePoint.from_flexible_input_and_fixed_scheme(
#                                                                          mass_neighbour,
#                                                                          cfg_combine_path,
#                                                                          output_ws_path,
#                                                                          input_prepath,
#                                                                          input_path_placeholder,
#                                                                          self.channels,
#                                                                          self.correlation_scheme_version,
#                                                                          POI_name='xsec_br'
#                                                                       )

            comb.run_combination()
            comb.run_generate_Asimov()
            limit_pt = comb.run_calc_limit(self.limits_dir)
            limit_pts[neighbour] = { 'mass': mass_neighbour, 'limit_pt': limit_pt}


        limit_combined_m1s_interpolated, limit_combined_m2s_interpolated, limit_combined_exp_interpolated, limit_combined_p1s_interpolated, limit_combined_p2s_interpolated, limit_combined_obs_interpolated = interpolate_limits_pts(limit_pts, mass)
        self.logger.debug("limit_combined_exp_interpolated: {}".format(limit_combined_exp_interpolated))
        self.logger.debug("limit_combined_obs_interpolated: {}".format(limit_combined_obs_interpolated))

        pt['limit_combined_m1s_interpolated'] = limit_combined_m1s_interpolated
        pt['limit_combined_m2s_interpolated'] = limit_combined_m2s_interpolated
        pt['limit_combined_exp_interpolated'] = limit_combined_exp_interpolated
        pt['limit_combined_p1s_interpolated'] = limit_combined_p1s_interpolated
        pt['limit_combined_p2s_interpolated'] = limit_combined_p2s_interpolated
        pt['limit_combined_obs_interpolated'] = limit_combined_obs_interpolated

        theory_over_limit_combined_m1s_ratio_key = "{}_over_limit_combined_m1s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_m2s_ratio_key = "{}_over_limit_combined_m2s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_exp_ratio_key = "{}_over_limit_combined_exp".format(self.xsec_to_be_compared)
        theory_over_limit_combined_p1s_ratio_key = "{}_over_limit_combined_p1s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_p2s_ratio_key = "{}_over_limit_combined_p2s".format(self.xsec_to_be_compared)
        theory_over_limit_combined_obs_ratio_key = "{}_over_limit_combined_obs".format(self.xsec_to_be_compared)

        pt[theory_over_limit_combined_m1s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_combined_m1s_interpolated)
        pt[theory_over_limit_combined_m2s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_combined_m2s_interpolated)
        pt[theory_over_limit_combined_exp_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_combined_exp_interpolated)
        pt[theory_over_limit_combined_p1s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_combined_p1s_interpolated)
        pt[theory_over_limit_combined_p2s_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_combined_p2s_interpolated)
        pt[theory_over_limit_combined_obs_ratio_key] = float(pt[self.xsec_to_be_compared])/float(limit_combined_obs_interpolated)
        sys.stdout.flush()

        return pt


def interpolate_limits_pts(limit_pts, mass):

    limit_m1s_low  = limit_pts['low']['limit_pt']['mu_m1s_NP_fit']
    limit_m2s_low  = limit_pts['low']['limit_pt']['mu_m2s_NP_fit']
    limit_exp_low  = limit_pts['low']['limit_pt']['mu_exp_NP_fit']
    limit_p1s_low  = limit_pts['low']['limit_pt']['mu_p1s_NP_fit']
    limit_p2s_low  = limit_pts['low']['limit_pt']['mu_p2s_NP_fit']
    limit_obs_low  = limit_pts['low']['limit_pt']['mu_obs_NP_fit']

    limit_m1s_high  = limit_pts['high']['limit_pt']['mu_m1s_NP_fit']
    limit_m2s_high  = limit_pts['high']['limit_pt']['mu_m2s_NP_fit']
    limit_exp_high  = limit_pts['high']['limit_pt']['mu_exp_NP_fit']
    limit_p1s_high  = limit_pts['high']['limit_pt']['mu_p1s_NP_fit']
    limit_p2s_high  = limit_pts['high']['limit_pt']['mu_p2s_NP_fit']
    limit_obs_high  = limit_pts['high']['limit_pt']['mu_obs_NP_fit']
    
    mass_low       = limit_pts['low']['mass']
    mass_high      = limit_pts['high']['mass']
    
    limit_m1s_interpolated = interpolate(limit_m1s_low, limit_m1s_high, mass_low, mass_high, mass)
    limit_m2s_interpolated = interpolate(limit_m2s_low, limit_m2s_high, mass_low, mass_high, mass)
    limit_exp_interpolated = interpolate(limit_exp_low, limit_exp_high, mass_low, mass_high, mass)
    limit_p1s_interpolated = interpolate(limit_p1s_low, limit_p1s_high, mass_low, mass_high, mass)
    limit_p2s_interpolated = interpolate(limit_p2s_low, limit_p2s_high, mass_low, mass_high, mass)
    limit_obs_interpolated = interpolate(limit_obs_low, limit_obs_high, mass_low, mass_high, mass)

    return limit_m1s_interpolated, limit_m2s_interpolated, limit_exp_interpolated, limit_p1s_interpolated, limit_p2s_interpolated, limit_obs_interpolated


def interpolate(limit_low, limit_high, mass_low, mass_high, mass):

    limit_low = float(limit_low)
    limit_high = float(limit_high)
    mass_high = float(mass_high)
    mass_low = float(mass_low)

    slope = (limit_high - limit_low)/(mass_high - mass_low)
    dmass = mass - mass_low
    limit = limit_low + dmass * slope

    return limit


def get_failed_jobs_from_config_file_path(job_manager_config_path):

    with open(job_manager_config_path, 'r') as cfg:
        job_manager_cfg = json.load(cfg)

    failed_jobs = get_failed_jobs(job_manager_cfg)
    return failed_jobs


def get_failed_jobs(job_manager_config):

    number_of_all_jobs    = len(job_manager_config['jobs'])
    number_of_failed_jobs = 0
    number_of_succeeded_jobs = 0

    failed_jobs = {}

    for job, options in job_manager_config['jobs'].items():
        job_processed_pts_path = options['job_processed_pts_path']
        job_scan_pts_path = options['job_scan_pts_path']

        if os.path.isfile(job_processed_pts_path):
            number_of_final_processed_pts = sum(1 for line in open(job_processed_pts_path)) - 1
        else:
            number_of_final_processed_pts = -777
        if os.path.isfile(job_scan_pts_path):
            number_of_to_be_processed_pts = sum(1 for line in open(job_scan_pts_path)) - 1
        else:
            number_of_to_be_processed_pts = -999
        if number_of_final_processed_pts == number_of_to_be_processed_pts:
            print("PASS: {0} seems to have finished.".format(job))
            number_of_succeeded_jobs += 1
        else:
            print("FAIL: {0} has not processed all of the assigned points! done/todo={1}/{2}".format(job,number_of_final_processed_pts,number_of_to_be_processed_pts))
            failed_jobs[job] = options
            number_of_failed_jobs += 1
    print("----------------------------")
    print("Pass: {0}/{1}, Fail: {2}/{1}".format(number_of_succeeded_jobs, number_of_all_jobs,
            number_of_failed_jobs))

    return failed_jobs


def resubmit_failed_jobs(previous_job_manager_config_path, new_job_manager_config_path,
        new_points_path, machines, resources, batch='sge'):

    with open(previous_job_manager_config_path, 'r') as prev_cfg:
        previous_job_manager_cfg = json.load(prev_cfg)

    new_job_manager_cfg = previous_job_manager_cfg
    new_job_manager_cfg['result_pts_path'] = new_points_path
    new_job_manager_cfg['job_manager_config_path'] =  new_job_manager_config_path
    new_job_manager_cfg['machines'] = machines
    new_job_manager_cfg['resources'] = resources

    failed_jobs = get_failed_jobs(previous_job_manager_cfg)
    new_job_manager_cfg['jobs'] = failed_jobs

    # - Delete failed job results
    for job, options in failed_jobs.items():
        job_processed_pts_path = options['job_processed_pts_path']
        if os.path.isfile(job_processed_pts_path):
            os.remove(job_processed_pts_path)

    with open(new_job_manager_config_path, 'w') as new_cfg:
        json.dump(new_job_manager_cfg, new_cfg, indent=2) 

    model_scan_mgr = model_scan_manager.from_manager_config(new_job_manager_config_path)
    model_scan_mgr.full_config = new_job_manager_cfg
    if batch == 'sge':
        model_scan_mgr.submit_jobs_sge()
    if batch == 'condor':
        model_scan_mgr.submit_jobs_condor()
    else:
        print "The requested batch system does not exist: " + batch
