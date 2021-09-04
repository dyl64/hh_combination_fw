import ROOT
from math import sqrt, fabs, erf
import click
import json
from quickstats.components import AnalysisObject
from quickstats.components.likelihood import evaluate_nll
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import aux_utils as utils
from itertools import repeat
from glob import glob
from pdb import set_trace

@click.command(name='pvalue')
@click.option('-i', '--input_path', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-p', '--parallel', required=False, type=int, default=-1, help='number of parallel jobs')
@click.option('--expected', default=None, type=click.Choice(['0', '1', '-1']), help='run expected or observed p-value')
def pvalue(input_path, poi_name, dataset, parallel, expected):
    input_files = []
    if input_path.endswith('.root'):
        input_files.append(input_path)
    else:
        input_files = glob(input_path + '/[0-9]*[0-9].root')
    if len(input_files) == 0:
        assert(0), 'no input found'
    if parallel == -1:
        max_workers = min(multiprocessing.cpu_count(), len(input_files))
    else:
        max_workers = parallel

    if len(input_files) == 1:
        if expected is None:
            _nll(input_files[0], poi_name, dataset)
        else:
            _nll_exp(input_files[0], poi_name, dataset, int(expected))
    else:
        if expected is None:
            arguments = (input_files, repeat(poi_name), repeat(dataset))
            utils.parallel_run(_nll, *arguments, max_workers=max_workers)
        else:
            arguments = (input_files, repeat(poi_name), repeat(dataset), repeat(int(expected)))
            utils.parallel_run(_nll_exp, *arguments, max_workers=max_workers)

def _nll_exp(input_file, poi_name, dataset, expected, uncap=True):
    '''
        Instead of calling evaluate_nll(), run the fit manually for better control
    '''
    def _evaluate_nll(input_file, poi_name, expected, unconditional=False):
        config = {
                    'filename': input_file,
                    'data_name': "combData",
                    'binned_likelihood' : True,
                    'fix_param': None,
                    'profile_param': None,
                    'ws_name': None,
                    'mc_name': None,
                    'snapshot_name': None,
                    'strategy': 1,
                    'num_cpu': 1,
                    'offset': False,
                    'optimize': 2,
                    'strategy': 1,
                    'eps': 1,
                    'constrain_nuis': True,
                }
    
        obj = AnalysisObject(**config)
        # despite the profiled value, asimov always contains 1 (?) signal
        if expected == -1:
            print('Generate unconditional Asimov dataset')
            asimov_data = obj.model.generate_asimov(poi_name=poi_name, poi_val=0.0, poi_profile=1.0, 
                    conditional_mle=False, do_import=True, globs_np_matching=True, asimov_name='dataset_temp',
                    snapshot_names={'conditional_globs': 'customised_globs', 'conditional_nuis': 'customised_nuis'})
        else:
            print(f'Generate conditional POI={expected} Asimov dataset')
            asimov_data = obj.model.generate_asimov(poi_name=poi_name, poi_val=0.0, poi_profile=expected, 
                    conditional_mle=True, do_import=True, globs_np_matching=True, asimov_name='dataset_temp',
                    snapshot_names={'conditional_globs': 'customised_globs', 'conditional_nuis': 'customised_nuis'})
        obj.model.workspace.writeToFile(f'asimov_temp{expected}.root')
        # for best fit - instead of create asimov data, take the input dataset
        # asimov_data = obj.model.workspace.data(obj.model.data_name)

        poi = obj.model.workspace.var(poi_name)
        poi_val = 0

        if unconditional:
            poi.setConstant(0)
            # the range slightly affect the fit result; +-10 is consistent with the likelihood.evaluate_nll()
            vmin, vmax = 10, 10
            poi_min, poi_max = poi_val-abs(vmin), poi_val+abs(vmax)
            poi.setRange(poi_min, poi_max)
        else:
            poi.setVal(poi_val)
            poi.setConstant(1)

        obj.model.workspace.loadSnapshot("customised_nuis")
        obj.model.workspace.loadSnapshot("customised_globs")

        check_asimov = False
        if check_asimov:
            obs_nll  = obj.model.pdf.createNLL(asimov_data, *obj.minimizer.nll_command_list)
            obj.minimizer.minimize(obs_nll, hesse=True, print_level=1)
            print("check_asimov best fit mu in asimov = ", obj.model.workspace.var(poi_name).getVal(), 'NLL', obj.minimizer.fit_result.minNll())

        nll_mu = obj.minimizer.fit_result.minNll()
        poi_value = obj.model.workspace.var(poi_name).getVal()
        poi.setConstant(0) # free POI

        return nll_mu, poi_value

    nll_mu_0, poi_0 = _evaluate_nll(input_file, poi_name, expected, unconditional = False)
    print('nll_mu_0, poi_0', nll_mu_0, poi_0)

    nll_mu_free, poi_free = _evaluate_nll(input_file, poi_name, expected, unconditional = True)
    print('nll_mu_free, poi_free', nll_mu_free, poi_free)

    output_file = input_file[::-1].replace('.root'[::-1], f'_pvalue_exp{expected}.json'[::-1], 1)[::-1]
    _pvalue(nll_mu_0, nll_mu_free, poi_free, uncap, output_file=output_file)

def _nll(input_file, poi_name, dataset, uncap=True):
    poi_val = 0
    nll_mu_0 = evaluate_nll(input_file, poi_val, poi_name, strategy = 1, unconditional=False, data=dataset, offset=False)
    result_free = evaluate_nll(input_file, poi_val, poi_name, strategy = 1, unconditional=True, data=dataset, offset=False, detailed_output=True)
    nll_mu_free = result_free['nll']
    poi_free = result_free['poi_bestfit']

    # Write out results next to the input file
    output_file = input_file[::-1].replace('.root'[::-1], f'_pvalue.json'[::-1], 1)[::-1]
    _pvalue(nll_mu_0, nll_mu_free, poi_free, uncap, output_file=output_file)

def _pvalue(nll_mu_0, nll_mu_free, poi_free, uncap, output_file='pvalue.json'):
    q0 = 2*(nll_mu_0 -nll_mu_free)

    if uncap and poi_free < 0:
        q0 = -q0

    sign = 0 if q0 == 0 else q0 / fabs(q0)
    q0 = fabs(q0)

    significance = sign*sqrt(q0)
    pvalue = (1-erf(significance/sqrt(2)))/2;
    # Equivalent to:
    # import ROOT
    # pvalue = 1-ROOT.Math.normal_cdf(sqrt(q0 ),1,0)
    # significance = ROOT.RooStats.PValueToSignificance(pvalue)

    dic = {
        'nll_mu_0': nll_mu_0,
        'nll_mu_free': nll_mu_free,
        'q0_orig': 2*(nll_mu_0 -nll_mu_free),
        'best_mu': poi_free,
        'q0': q0,
        'pvalue': pvalue,
        'significance': significance
        }
    with open(output_file, 'w') as f:
        json.dump(dic, f, indent=4)
    print('Save to', output_file)
    print(dic)

