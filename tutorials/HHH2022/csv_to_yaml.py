import pandas as pd
import yaml, csv, os
from pdb import set_trace

class hepYaml:
    def __init__(self, config):
        self.independent_variables = config.get('independent_variables', None)
        self.dependent_variables = config.get('dependent_variables', None)
        self.independent_unit = config.get('independent_unit', '')
        self.independent_name = config.get('independent_name', '')
        self.dependent_unit = config.get('dependent_unit', '')
        self.yaml_file = config.get('yaml_file', None)
        self.name_map = {
            '0': 'Expected',
            '1': '$1 \sigma$',
            '2': '$2 \sigma$',
            '-1': '$-1 \sigma$',
            '-2': '$-2 \sigma$',
            'obs': 'Observed',
        }

    def construct_data(self):
        self.data = {
            'independent_variables': [
                {
                    'header': {'name': self.independent_name, 'units': self.independent_unit},
                    'values': [
                        {'value': i} for i in self.independent_variables
                    ],
                }
            ],
            'dependent_variables': [
                {
                    'header': {'name': self.name_map.get(j, j), 'units': self.dependent_unit},
                    'values': [
                        {'value': float(i)} for i in self.dependent_variables[j]
                    ],
                } for j in self.dependent_variables.keys()
            ]
        }

    def save_yaml(self):
        with open(self.yaml_file, 'w') as outfile:
            yaml.dump(self.data, outfile, default_flow_style=False)
            print('Save to', self.yaml_file)

    def run(self):
        self.construct_data()
        self.save_yaml()

class hepwriter:
    def __init__(self):
        self.yaml_file = None
        self.reset()

    def run(self):
        if self.yaml_file is None:
            if isinstance(self.csv_files, dict):
                key = list(self.csv_files.keys())[0]
                self.yaml_file = os.path.splitext(self.csv_files[key])[0] + '.yaml'
            elif isinstance(self.csv_files, list):
                self.yaml_file = os.path.splitext(self.csv_files[0])[0] + '.yaml'
        else:
            self.yaml_file = yaml_file

        self.config = {
            'independent_variables': self.independent_variables,
            'dependent_variables': self.dependent_variables,
            'independent_unit': self.independent_unit,
            'dependent_unit': self.dependent_unit,
            'yaml_file': self.yaml_file,
            'independent_name': self.independent_name,
        }

        hepyaml = hepYaml(self.config)
        hepyaml.run()
    
    def reset(self):
        self.dependent_variables = {}
        self.independent_variables = ''
        self.independent_unit = ''
        self.dependent_unit = ''
        self.independent_name = 'X'

    def zeroD_limit(self, csv_file, remove_row=['mass', 'inj'], yaml_file=None, unit=''):
        '''
        independent variable | dependent variable A | dependent variable B | ...
        independent value 1  | dependent value 1    | dependent value 1    | ...
        independent value 2  | dependent value 2    | dependent value 2    | ...
        ...
        '''
        self.reset()
        self.yaml_file = yaml_file
        self.csv_files = [csv_file]
        with open(csv_file, 'r') as fp:
            datareader = csv.reader(fp)
            for row in datareader:
                if row[0] in remove_row: continue
                if row[0] == '':
                    self.independent_variables = row[1:]
                else:
                    self.dependent_variables[row[0]] = row[1:]
        self.dependent_unit = unit
        self.dependent_name = 'Channel'
        self.run()

    def xsec_scan(self, csv_files, scan_range=(-10, 15), param_name='klambda', yaml_file=None):
        self.reset()
        self.yaml_file = yaml_file
        self.csv_files = csv_files
        dfs = {}
        nrow = 0
        for key in csv_files:
            print('key', key, csv_files[key])
            dfs[key] = pd.read_csv(csv_files[key])
            dfs[key].loc[(dfs[key][param_name] >= scan_range[0]) & (dfs[key][param_name] <= scan_range[1])] # select in scan_range
            if nrow == 0:
                nrow = dfs[key].shape[0]
            else:
                assert(nrow == dfs[key].shape[0])
            self.independent_variables = list(dfs[key][param_name])
            if key == 'individual':
                for col in dfs[key]:
                    if col == param_name: # remove independent variable
                        continue
                    self.dependent_variables[col] = list(dfs[key][col])
            elif key == 'combined':
                self.dependent_variables[key+' $-2 \sigma$'] = list(dfs[key]['-2'])
                self.dependent_variables[key+' $-1 \sigma$'] = list(dfs[key]['-1'])
                self.dependent_variables[key+' $1 \sigma$'] = list(dfs[key]['1'])
                self.dependent_variables[key+' $2 \sigma$'] = list(dfs[key]['2'])
        
        self.dependent_name = param_name
        self.dependent_unit = 'fb'
        self.run()

    def likelihood_scan(self, csv_file, scan_range=(-6, 12), param_name='klambda', yaml_file=None, extra_name=''):
        self.reset()
        self.yaml_file = yaml_file
        self.csv_files = [csv_file]
        df = pd.read_csv(csv_file)
        df.loc[(df[param_name] >= scan_range[0]) & (df[param_name] <= scan_range[1])] # select in scan_range
        self.independent_variables = list(df[param_name])
        self.dependent_variables[extra_name] = list(df['qmu'])
        self.independent_name = r'$\kappa_\lambda$' if param_name == 'mu' else param_name
        self.run()

    def twoD_scan(self, csv_file, x_scan_range=(-6, 12), y_scan_range=(-6, 12), param_names='klambda_kt', extra_name=''):
        self.reset()
        self.csv_files = [csv_file]
        self.independent_name, self.dependent_name = tuple(param_names.split('_'))
        self.yaml_file = None
        df = pd.read_csv(csv_file)
        df.loc[(df[self.independent_name] >= x_scan_range[0]) & (df[self.independent_name] <= x_scan_range[1])]
        df.loc[(df[self.dependent_name] >= y_scan_range[0]) & (df[self.dependent_name] <= y_scan_range[1])]
        self.independent_variables = list(df[self.independent_name])
        self.dependent_variables[self.dependent_name + ' ' + extra_name] = list(df[self.dependent_name])
        self.run()


def submission():
    outfolder = 'hepdata'
    os.makedirs(outfolder, exist_ok=True)
    writer = hepwriter()
    submission_all = []
    submission_info = {}
    submission_info['additional_resources'] = [{
        'location': 'https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HDBS-2022-03',
        'description': 'web page with auxiliary material',
    }]
    # submission_info['hepdata_doi'] = 'https://doi.org/10.17182/hepdata.135471',
    submission_info['comment'] = 'ATLAS Run 2 single H and diHiggs combination for Higgs 10 years symposium.'
    submission_all.append(submission_info)

    # start individual figures
    common_keywords = [
        {
            'name': 'reactions',
            'values': ['P P --> H, P P --> H H, P P --> H H j j'],
        },
        {
            'name': 'cmenergies',
            'values': ['13000.0'],
        },
        {
            'name': 'phrases',
            'values': ['diHiggs', 'single Higgs', 'kappa framework', 'combination'],
        },
    ]

    #### SM limit ####
    csv_files = [
        f'all/outputs_HHH2022_20220701_noSgHparam_mu_figures_SM_final/SM_limit_mu_final.csv',
        f'all/outputs_HHH2022_20220701_noSgHparam_xsec_figures_SM_final/SM_limit_realxsec_final.csv'
        ]
    figures = ['3', 'Aux 1']
    remove_row = ['mass', 'inj']
    
    for figure, csv_file in zip(figures, csv_files):
        submission_info = {}
        writer.zeroD_limit(csv_file, unit='' if '_mu_' in csv_file else 'fb')
        
        submission_info['keywords'] = common_keywords + [
            {
                'name': 'observables',
                'values': ['signal strength'],
            },
        ]
        submission_info['name'] = f'Figure {figure}'
        submission_info['data_file'] = os.path.join(os.path.basename(writer.yaml_file))
        os.system(f'mv -f {writer.yaml_file} {outfolder}')

        submission_info['additional_resources'] = [{
            'description': submission_info['name'],
            'location': f'{os.path.basename(csv_file.replace(".csv", ".png"))}'
        }]
        os.system(f'sips -s format png {csv_file.replace(".csv", ".pdf")} --out {outfolder}/{submission_info["additional_resources"][0]["location"]}')

        if figure == '3':
            submission_info['description'] = 'Observed and expected 95% CL upper limits on the signal strength for double-Higgs production.'
        elif figure == 'Aux 1':
            submission_info['description'] = 'Observed and expected 95% CL upper limits on the cross section for double-Higgs production.'
        submission_all.append(submission_info)

    #### xsec scan ####
    plot_path = 'all/outputs_HHH2022_20220701_noSgHparam_xsec_figures_xsection_scan_final'
    figures = ['4a', '4b']
    for figure, var in zip(figures, ['klambda', 'k2V']):
        csv_files = {
            'combined': f'{plot_path}/{var.lower()}_limit_parameterised_ws_combined_withindiv_final.csv',
            'individual': f'{plot_path}/{var.lower()}_limit_parameterised_ws_combined_withindiv_final_individual.csv',
        }
        remove_row = ['mass', 'inj']
        submission_info = {}
        writer.xsec_scan(csv_files, param_name=var)

        submission_info['name'] = f'Figure {figure}'
        submission_info['data_file'] = os.path.join(os.path.basename(writer.yaml_file))
        os.system(f'mv -f {writer.yaml_file} {outfolder}')

        submission_info['additional_resources'] = [{
            'description': submission_info['name'],
            'location': f'{var.lower()}_limit_parameterised_ws_combined_withindiv_final.png'
        }]
        os.system(f'sips -s format png {plot_path}/{submission_info["additional_resources"][0]["location"].replace(".png", ".pdf")} --out {outfolder}/{submission_info["additional_resources"][0]["location"]}')
            
        if var == 'klambda':
            submission_info['keywords'] = common_keywords + [
                {
                    'name': 'observables',
                    'values': [r'$\kappa_\lambda$'],
                },
            ]
            submission_info['description'] = r'Observed and expected exclusion limits on ggF and VBF as a function of $\kappa_lambda$.'
        elif var == 'k2V':
            submission_info['keywords'] = common_keywords + [
                {
                    'name': 'observables',
                    'values': ['$\kappa_{2V}$'],
                },
            ]
            submission_info['description'] = r'Observed and expected exclusion limits on VBF as a function of $\kappa_{2V}$.'
        submission_all.append(submission_info)

    #### likelihood scan ####
    figures = ['Aux 3', 'Aux 4']
    plot_path = 'all/outputs_HHH2022_20220701_with_BR_decorrelation_figures_likelihood_scan_final'
    for figure, var in zip(figures, ['klambda', 'k2V']):
        for chan in ['bbbb', 'bbtautau', 'bbyy', 'combined']:
            for subfigure, job in zip(['a', 'b'], ['observed', 'expected']):
                submission_info = {}
                csv_file = f'{plot_path}/likelihood_scan_{var}_{job}_final_{var}_{job}_{chan}.csv'
                
                writer.likelihood_scan(csv_file, scan_range=(-100, 100), param_name=var, extra_name=chan)
                submission_info['name'] = f'Figure {figure}{subfigure} {chan} {job}'
                submission_info['data_file'] = os.path.join(os.path.basename(writer.yaml_file))
                os.system(f'mv -f {writer.yaml_file} {outfolder}')

                submission_info['additional_resources'] = [{
                    'description': submission_info['name'],
                    'location': f'likelihood_scan_{var}_{job}_final.png'
                }]
                os.system(f'sips -s format png {plot_path}/{submission_info["additional_resources"][0]["location"].replace(".png", ".pdf")} --out {outfolder}/{submission_info["additional_resources"][0]["location"]}')

                if var == 'klambda':
                    submission_info['keywords'] = common_keywords + [
                        {
                            'name': 'observables',
                            'values': ['$\kappa_\lambda$'],
                        },
                    ]
                    submission_info['description'] = r'Observed and expected exclusion limits on ggF and VBF as a function of $\kappa_lambda$'
                elif var == 'k2V':
                    submission_info['keywords'] = common_keywords + [
                        {
                            'name': 'observables',
                            'values': ['$\kappa_{2V}$'],
                        },
                    ]
                    submission_info['description'] = r'Observed and expected exclusion limits on VBF as a function of $\kappa_{2V}$'
                submission_all.append(submission_info)

    #### likelihood scan HHH ####
    plot_path = 'all/HHHresults_figures_final'
    plot_name = {
        'exp': 'H_HH_k2Vfixed_asimov_final.pdf',
        'obs': 'H_HH_k2Vfixed_data_final.pdf'
    }
    for var in ['mu']:
        for chan in ['HHH', 'diHiggs', 'singleH', 'generic']:
            for figure, job in zip(['5a', '5b'], ['obs', 'exp']):
                submission_info = {}
                csv_file = f'{plot_path}/1D_{job}_{chan}.csv'
                writer.likelihood_scan(csv_file, scan_range=(-100, 100), param_name=var, extra_name=f'{chan} {job}')
                submission_info['name'] = f'Figure {figure} {chan} {job}'
                submission_info['data_file'] = os.path.join(os.path.basename(writer.yaml_file))
                os.system(f'mv -f {writer.yaml_file} {outfolder}')

                submission_info['additional_resources'] = [{
                    'description': submission_info['name'],
                    'location': f'{plot_name[job].replace(".pdf", ".png")}'
                }]
                os.system(f'sips -s format png {plot_path}/{submission_info["additional_resources"][0]["location"].replace(".png", ".pdf")} --out {outfolder}/{submission_info["additional_resources"][0]["location"]}')

                submission_info['keywords'] = common_keywords + [
                    {
                        'name': 'observables',
                        'values': ['$\kappa_\lambda$'],
                    },
                ]
                submission_info['description'] = r'Observed and expected of the test statistic ($-2 \ln \Lambda$), as a function of the $\kappa_lambda$'
                submission_all.append(submission_info)

    #### likelihood scan 2D ####
    plot_path = 'all/HHHresults_figures_final'
    plot_name = {
        'k2V_kV_exp': 'HH_kV_k2V_exp_final.pdf',
        'k2V_kV_obs': 'HH_kV_k2V_obs_final.pdf',
        'klambda_kt_exp': 'H_HH_HHH_kl_kt_2D_asimov_final.pdf',
        'klambda_kt_obs': 'H_HH_HHH_kl_kt_2D_data_final.pdf',
    }
    figures = [('6a', '6b'), ('Aux 5a', 'Aux 5b')]
    for fig, var in zip(figures, ['klambda_kt', 'k2V_kV']):
        for chan in ['HHH', 'diHiggs', 'singleH']:
            if var == 'k2V_kV' and chan != 'diHiggs':
                continue
            for figure, job in zip(fig, ['exp', 'obs']):
                for level, value in zip(['68%', '95%'], ['2.3', '5.99']):
                    submission_info = {}
                    csv_file = f'{plot_path}/2D_{job}_{var}_{chan}_{value}.csv'
                    writer.twoD_scan(csv_file, x_scan_range=(-100, 100), y_scan_range=(-100, 100), param_names=var, extra_name=f'{job} {level}')
                    submission_info['name'] = f'Figure {figure} {chan} {job} {level}'
                    submission_info['data_file'] = os.path.join(os.path.basename(writer.yaml_file))
                    os.system(f'mv -f {writer.yaml_file} {outfolder}')

                    submission_info['additional_resources'] = [{
                        'description': submission_info['name'],
                        'location': f'{plot_name[var+"_"+job].replace(".pdf", ".png")}'
                    }]
                    os.system(f'sips -s format png {plot_path}/{submission_info["additional_resources"][0]["location"].replace(".png", ".pdf")} --out {outfolder}/{submission_info["additional_resources"][0]["location"]}')

                    submission_info['keywords'] = common_keywords + [
                        {
                            'name': 'observables',
                            'values': ['$\kappa_\lambda$', '$\kappa_2V$'],
                        },
                    ]
                    submission_info['description'] = f'{job} constraints in the 2D plane.'
                    submission_all.append(submission_info)

    submission_all[1:] = sorted(submission_all[1:], key=lambda d: d['name'])
    with open(f"{outfolder}/submission.yaml", "w") as stream:
        yaml.dump_all(submission_all, stream, default_flow_style=False)


submission()
