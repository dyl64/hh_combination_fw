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
@click.option('--expected', default=None, type=click.Choice(['0', '1']), help='run expected or observed p-value')
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

def _nll_exp(input_file, poi_name, dataset, poi_val, uncap=True):
    '''
        Instead of calling evaluate_nll(), run the fit manually for better control
    '''
    def _evaluate_nll(input_file, poi_name, poi_val, unconditional=False):
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
        # despite the profiled value, asimov always contains 1 signal
        asimov_data = obj.model.generate_asimov(poi_name=poi_name, poi_val=1, poi_profile=poi_val, do_conditional=True)
        # for best fit - instead of create asimov data, take the input dataset
        # asimov_data = obj.model.workspace.data(obj.model.data_name)

        obj.model.workspace.loadSnapshot("conditionalGlobs_0")
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
        obs_nll  = obj.model.pdf.createNLL(asimov_data, *obj.minimizer.nll_command_list)
        obj.minimizer.minimize(obs_nll, hesse=True)
        nll_mu = obj.minimizer.fit_result.minNll()
        poi_value = obj.model.workspace.var(poi_name).getVal()
        poi.setConstant(0) # free POI

        return nll_mu, poi_value

    nll_mu_0, poi_0 = _evaluate_nll(input_file, poi_name, poi_val, unconditional = False)
    print('nll_mu_0, poi_0', nll_mu_0, poi_0)

    nll_mu_free, poi_free = _evaluate_nll(input_file, poi_name, poi_val, unconditional = True)
    print('nll_mu_free, poi_free', nll_mu_free, poi_free)

    output_file = input_file[::-1].replace('.root'[::-1], f'_pvalue_exp{poi_val}.json'[::-1], 1)[::-1]
    _pvalue(nll_mu_0, nll_mu_free, poi_free, uncap, output_file=output_file)

    #nll_mu_0, poi_0 = my_evaluate_nll(obj, unconditional = False)
    #nll_mu_free, poi_free = my_evaluate_nll(obj, unconditional = True)

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

#def my_evaluate_nll(obj:str, unconditional=False):
#    obj.model.workspace.loadSnapshot("conditionalGlobs_0")
#
#    poi = 'xsec_br'
#    data='combData'
#    snapshot:str=None
#    hesse:bool=False
#    minos:bool=True
#    constrain:bool=True
#    minimizer_type:str='Minuit2'
#    minimizer_algo:str='Migrad'
#    num_cpu:int=1
#    binned:bool=True
#    eps:float=1.0
#    strategy:int=0
#    fix_cache:bool=True
#    fix_multi:bool=True
#    mpsplit:int=3
#
#    verbose:int=0
#    max_calls:int=-1
#    max_iters:int=-1
#    optimize:int=2
#    offset:bool=False
#    outname:str=None
#
#    poi_val = 0
#    vmin, vmax = 10, 10
#    model = obj.model #ExtendedModel(fname=input_file, ws_name=workspace, mc_name=model_config,
#            #              data_name=data, binned_likelihood=binned, snapshot_name=snapshot, 
#            #              fix_cache=fix_cache, fix_multi=fix_multi)
#    if poi:
#        poi = model.workspace.var(poi)
#    else:
#        poi = model.pois.first()
#    poi_min, poi_max = poi_val-abs(vmin), poi_val+abs(vmax)
#    poi.setRange(poi_min, poi_max)
#    if unconditional:
#        poi.setConstant(0)
#        hesse = True
#    else:
#        poi.setVal(poi_val)
#        poi.setConstant(1)
#
#    minimizer = obj.minimizer# ExtendedMinimizer("minimizer", model.pdf, model.data)
#    # configure minimize options
#    nll_commands = [ROOT.RooFit.NumCPU(num_cpu, mpsplit), 
#                    ROOT.RooFit.GlobalObservables(model.global_observables), 
#                    ROOT.RooFit.Offset(offset)]
#
#    if constrain:
#        nll_commands.append(ROOT.RooFit.Constrain(model.nuisance_parameters))
#    minimize_options = {
#        'minimizer_type'   : minimizer_type,
#        'minimizer_algo'   : minimizer_algo,
#        'default_strategy' : strategy,
#        'opt_const'        : optimize,
#        'eps'              : eps,
#        'max_calls'        : max_calls,
#        'max_iters'        : max_iters,
#        'hesse'            : hesse,
#        'verbose'          : verbose
#    }
#    if minos:
#        minimize_options['minos']     = True
#        minimize_options['minos_set'] = ROOT.RooArgSet(poi)
#    # perform the fit
#    minimizer.minimize(nll_commands=nll_commands, **minimize_options)
#    nll = minimizer.fit_result.minNll()
#    if unconditional:
#        print('INFO: Unconditional NLL for POI "{}": {}'.format(poi.GetName(), nll))
#    else:
#        print('INFO: NLL for POI "{}" at {:.2f}: {}'.format(poi.GetName(), poi_val, nll))
#    
#    results = {
#        'nll': nll,
#        'poi': poi.GetName(),
#        'constrain': int(constrain),
#        'poi_value': poi_val,
#        'poi_min': poi_min,
#        'poi_max': poi_max,
#        'unconditional': int(unconditional)
#    }
#    poi_val = poi.getVal()
#    results['poi_bestfit'] = poi_val
#    
#    # save results
#    if outname is not None:
#        with open(outname, 'w') as outfile:
#            json.dump(results, outfile)
#        print('INFO: Saved NLL result to {}'.format(outname))
#        
#    return nll, poi_val
#
