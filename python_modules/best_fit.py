from math import sqrt, fabs, erf
import click
import json
from quickstats.components import Likelihood
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from itertools import repeat
from glob import glob
from os import path
from pdb import set_trace

@click.command(name='best_fit')
@click.option('-i', '--input_path', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-p', '--parallel', required=False, type=int, default=-1, help='number of parallel jobs')
@click.option('-s', '--snapshot', required=False, type=str, default=None, help='number of parallel jobs')
@click.option('-c', '--correlation/--no-correlation', default=False, help='retrive and draw correlation matrix')
def best_fit(input_path, poi_name, dataset, parallel, snapshot, correlation):
    input_files = []
    if input_path.endswith('.root'):
        input_files.append(input_path)
    else:
        input_files = glob(input_path + '/*[0-9].root')
    if len(input_files) == 0:
        assert(0), 'no input found'
    if parallel == 0:
        for input_file in input_files:
            _best_fit(input_file, poi_name, dataset, snapshot, correlation)
    else:
        if parallel == -1:
            max_workers = min(multiprocessing.cpu_count(), len(input_files))
        else:
            max_workers = parallel

        arguments = (input_files, repeat(poi_name), repeat(dataset), repeat(snapshot), repeat(correlation))
        import utils
        utils.parallel_run(_best_fit, *arguments, max_workers=max_workers)

def _best_fit(input_file, poi_name, dataset, snapshot, correlation):
    poi_val = 0
    likelihood = Likelihood(input_file, data_name=dataset, poi_name=poi_name)
    likelihood.evaluate(poi_val=poi_val, unconditional=True, snapshot_name=snapshot)
    nll_mu_free = likelihood.minNll
    poi = likelihood.poi

    # analysis = AnalysisObject(input_file, data_name=dataset, poi_name=poi_name)
    # poi = analysis.model.get_poi()
    # analysis.minimizer.minimize()

    if correlation:
        threshold = 0
        df = _get_correlation(likelihood, threshold=threshold)
        df.to_csv(path.dirname(input_file) + f'/correlation_{threshold}.csv')
        print('Correlation matrix', df.shape)
        print('Save to', path.dirname(input_file) + f'/correlation_{threshold}.csv')

    dic = {
        'best_mu': poi.getVal(),
        }
    print(dic)

def _get_correlation(likelihood, threshold):
    import numpy as np
    import ROOT
    import uproot
    import uuid
    import os
    correlation_hist = likelihood.fit_result.correlationHist()
    uniq_name = '/tmp/'+str(uuid.uuid4())+'.root'
    print('Save to', uniq_name)
    correlation_hist.SaveAs(uniq_name)
    #correlation_hist.Draw("colz")
    #ROOT.gROOT.GetListOfCanvases().At(0).SaveAs("test.pdf")
    #ROOT.gROOT.GetListOfCanvases().At(0).SaveAs("test.C")
    infile = uproot.open(uniq_name)
    hist = infile['correlation_matrix']
    np_names = hist.xlabels

    ''' Keep the `count` column, unstack the multi-index and remove the first/last columns/rows '''
    df = hist.pandas().unstack(level=0)['count'].iloc[1:-1 , 1:-1]
    df.columns = np_names
    np_names.reverse()
    df.index = np_names
    #set_trace()
    #df[(df < threshold) & (df > -threshold)] = 0
    #df = df.loc[(df.sum(axis=1) > 1), (df.sum(axis=0) > 1)]
    os.remove(uniq_name)

    print('Delete', uniq_name)
    return df
