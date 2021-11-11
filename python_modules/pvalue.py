import ROOT
from math import sqrt, fabs, erf
import click
import json
from quickstats.components import AnalysisObject
from quickstats.components.likelihood import evaluate_nll
from concurrent.futures import ProcessPoolExecutor
from quickstats.components import AsimovGenerator
import multiprocessing
import utils
from itertools import repeat
from glob import glob
from os import path
from pdb import set_trace

@click.command(name='pvalue')
@click.option('-i', '--input_path', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-s', '--snapshot', required=False, default=None, help='snapshot to load before fitting')
@click.option('-p', '--parallel', required=False, type=int, default=-1, help='number of parallel jobs')
@click.option('-e', '--expected', default=None, type=click.Choice(['0', '1', '-1']), help='run expected or observed p-value \
                                                                                            default: (None) run observed p-value, \
                                                                                            -1: profiling NPs and globs with mu floating and construct an S+B asimov, \
                                                                                             1: profiling NPs and globs with mu fixed to 1 and construct an S+B asimov, \
                                                                                             0: profiling NPs and globs with mu fixed to 0 and construct an S+B asimov, \
                                                                                            (will be multiplied by -n when generating asimov)')
@click.option('--blind/--unblind', default=False, help='unlind or unblind significance')
@click.option('-n', '--mu_1', required=False, type=float, default=1, help='normalisation in the workspace, eg 0.032776 in rescaled nonres ws in CONF (will be multiplied by -e when -e != -1)')
@click.option('--syst/--stat', default=True, help='calculate stat only (default syst)')
def pvalue(input_path, poi_name, dataset, parallel, blind, expected, mu_1, snapshot, syst):
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
        # obs significance
        if not blind and expected is None:
            _nll(input_files[0], poi_name, dataset, snapshot)
        else:
            _nll_exp(input_files[0], poi_name, dataset, blind, mu_1, expected, syst)
    else:
        if not blind and expected is None:
            arguments = (input_files, repeat(poi_name), repeat(dataset), repeat(snapshot))
            utils.parallel_run(_nll, *arguments, max_workers=max_workers)
        else:
            arguments = (input_files, repeat(poi_name), repeat(dataset), repeat(blind), repeat(mu_1), repeat(expected), repeat(syst))
            utils.parallel_run(_nll_exp, *arguments, max_workers=max_workers)

def _nll_exp(input_file, poi_name, dataset, blind, mu_1, expected=None, uncap=True, syst=True, output=None):
    print('zhangr', blind)
    '''
        Instead of calling evaluate_nll(), run the fit manually for better control
    '''
    def _evaluate_nll(input_file, poi_name, blind, expected=None, unconditional=False, mu_1 = mu_1, syst=True ):
        config = {
                    'filename': input_file,
                    'data_name': "combData",
                    'binned_likelihood' : True,
                    'fix_param': None if syst else \
                                "ATLAS_E*=0,ATLAS_F*=0,ATLAS_H*=0,ATLAS_J*=0,ATLAS_L*=0,ATLAS_P*=0,ATLAS_l*=0,alpha_*=0,THEO*=0,SPURIOUS*=0,ATLAS_M*=0,ATLAS_T*=0,ATLAS_b*=0"
                    ,
                    'profile_param': None,
                    'ws_name': None,
                    'mc_name': None,
                    'num_cpu': 1,
                    'offset': False,
                    'optimize': 2,
                    'strategy': 1,
                    'eps': 1,
                    'constrain_nuis': True,
                    'snapshot_name': "nominalNuis",
                }
        print('Fix', config['fix_param'])

        obj = AnalysisObject(**config)
    
        if blind: # blind significane, asimov no  profiling


            #gen_conf = {'asimov_name': 'asimovData_1_NP_Nominal', 'asimov_snapshot': 'asimovData_1_NP_Nominal', 'poi_val': 1.0, 'poi_profile': 1.0, 'do_fit': False, 'modify_globs': False, 'poi_name': 'xsec_br', 'minimizer_options': {'minimizer_type': 'Minuit2', 'minimizer_algo': 'Migrad', 'default_strategy': 1, 'opt_const': 2, 'precision': 0.001, 'eps': 1.0, 'eigen': False, 'max_calls': -1, 'max_iters': -1, 'print_level': -1, 'timer': False}}
            #asimov_data = obj.model.generate_asimov(**gen_conf)
            

            assert(expected is None), 'Blinded significance do not require --expected'
            print('Generate S+B prefit Asimov dataset')
            asimov_data = obj.model.generate_asimov(poi_name=poi_name, poi_val=mu_1, poi_profile=1,
                    do_fit=False, do_import=True, modify_globs=False, asimov_name='dataset_temp', 
                    snapshot_names={'conditional_globs': 'customised_globs', 'conditional_nuis': 'customised_nuis'})
        else:
            expected = int(expected)
            # despite the profiled value, asimov always contains 1 (?) signal
            if expected < 0:
                print('Generate unconditional Asimov dataset')
                asimov_data = obj.model.generate_asimov(poi_name=poi_name, poi_val=mu_1, poi_profile=None,
                        do_fit=True, do_import=True, modify_globs=True, asimov_name='dataset_temp', asimov_snapshot='dataset_temp',
                        snapshot_names={'conditional_globs': 'customised_globs', 'conditional_nuis': 'customised_nuis'})
            else:
                print(f'Generate conditional POI={expected} Asimov dataset')
                asimov_data = obj.model.generate_asimov(poi_name=poi_name, poi_val=mu_1, poi_profile=expected * mu_1, 
                        do_fit=True, do_import=True, modify_globs=True, asimov_name='dataset_temp', asimov_snapshot='dataset_temp',
                        snapshot_names={'conditional_globs': 'customised_globs', 'conditional_nuis': 'customised_nuis'})
        #obj.model.workspace.writeToFile(path.dirname(input_file) + f'/asimov_temp{expected}.root' if output is None else output)
        # for best fit - instead of create asimov data, take the input dataset
        # asimov_data = obj.model.workspace.data(obj.model.data_name)

        print('Load snapshot')
        obj.model.workspace.loadSnapshot("customised_nuis")
        obj.model.workspace.loadSnapshot("customised_globs")

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

        obs_nll  = obj.model.pdf.createNLL(asimov_data, ROOT.RooFit.GlobalObservables(obj.model.global_observables), ROOT.RooFit.Offset(True))
        obj.minimizer.minimize(obs_nll, print_level=-1)
        print("check_asimov best fit mu on asimov = ", obj.model.workspace.var(poi_name).getVal(), "+/-", obj.model.workspace.var(poi_name).getError(), 'NLL', obj.minimizer.nll.getVal())

        nll_mu = obj.minimizer.nll.getVal()

        poi_value = obj.model.workspace.var(poi_name).getVal()
        poi.setConstant(0) # free POI

        return nll_mu, poi_value

    nll_mu_0, poi_0 = _evaluate_nll(input_file, poi_name, blind, expected, unconditional = False, mu_1=mu_1, syst=syst)
    print('nll_mu_0, poi_0 {:.15f}, {:.15f}'.format(nll_mu_0, poi_0))

    nll_mu_free, poi_free = _evaluate_nll(input_file, poi_name, blind, expected, unconditional = True, mu_1=mu_1, syst=syst)
    print('nll_mu_free, poi_free {:.15f}, {:.15f}'.format(nll_mu_free, poi_free))

    output_file = input_file[::-1].replace('.root'[::-1], f'_pvalue_exp{"blind" if blind else "expected"}.json'[::-1], 1)[::-1]
    _pvalue(nll_mu_0, nll_mu_free, poi_free, uncap, output_file=output_file)

def _nll(input_file, poi_name, dataset, snapshot=None):
    uncap=True
    poi_val = 0
    nll_mu_0 = evaluate_nll(input_file, poi_val, poi_name=poi_name, strategy = 1, data_name=dataset, offset=False, snapshot_name=snapshot)
    result_free = evaluate_nll(input_file, poi_val=None, poi_name=poi_name, strategy = 1, data_name=dataset, offset=False, detailed_output=True, snapshot_name=snapshot)
    nll_mu_free = result_free['nll']
    poi_free = result_free['poi_bestfit']

    # Write out results next to the input file
    output_file = input_file[::-1].replace('.root'[::-1], f'_pvalue_{dataset}.json'[::-1], 1)[::-1]
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

