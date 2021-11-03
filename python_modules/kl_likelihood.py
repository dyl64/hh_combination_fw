import sys
from pdb import set_trace
import os
import re
import yaml
import click

from quickstats.components.likelihood import scan_nll

@click.command(name='kl_likelihood')
@click.option('-i', '--input_folder', required=True, help='Path to the task.')
@click.option('--min', 'poi_min', type=float, required=True, help='Minimum POI value to scan.')
@click.option('--max', 'poi_max', type=float, required=True, help='Maximum POI value to scan.')
@click.option('--step', 'poi_step', type=float, required=True, help='Scan interval.')
@click.option('-p', '--poi', default="klambda", help='POI to scan. If not specified, the first POI from the workspace is used.')
@click.option('--cache/--no-cache', default=True, help='Cache existing result')
@click.option('--vmin', type=float, default=10, help='Minimum range of POI relative to the central value during likelihood calculation.')
@click.option('--vmax', type=float, default=10, help='Maximum range of POI relative to the central value during likelihood calculation.')
@click.option('-w', '--workspace', default=None, help='Name of workspace. Auto-detect by default.')
@click.option('-m', '--model_config', default=None, help='Name of model config. Auto-detect by default.')
@click.option('-d', '--data', default='combData', help='Name of dataset.')
@click.option('-s', '--snapshot', default=None, help='Name of initial snapshot')
@click.option('-r', '--profile', default="", help='Parameters to profile')
@click.option('-f', '--fix', default="", help='Parameters to fix')
@click.option('--hesse/--no-hesse', default=False, help='Use Hesse error calculation')
@click.option('--minos/--no-minos', default=True, help='Use Minos error calculation')
@click.option('--constrain/--no-constrain', default=True, help='Use constrained NLL (i.e. include systematics)')
@click.option('-t', '--minimizer_type', default="Minuit2", help='Minimizer type')
@click.option('-a', '--minimizer_algo', default="Migrad", help='Minimizer algorithm')
@click.option('--binned/--unbinned', default=True, help='Binned likelihood')
@click.option('-e', '--eps', type=float, default=1.0, help='Convergence criterium')
@click.option('--strategy', type=int, default=0, help='Default minimization strategy')
@click.option('--print_level', type=int, default=-1, help='Minimizer print level')
@click.option('--fix-cache/--no-fix-cache', default=True, help='Fix StarMomentMorph cache')
@click.option('--fix-multi/--no-fix-cache',  default=True, help='Fix MultiPdf level 2')
@click.option('--mpsplit',  default=3, help='MP split mode')
@click.option('--max_calls', type=int, default=-1, help='Maximum number of function calls')
@click.option('--max_iters', type=int, default=-1, help='Maximum number of Minuit iterations')
@click.option('--optimize', type=int, default=2, help='Optimize constant terms')
@click.option('--offset/--no-offset', default=False, help='Offset likelihood')
@click.option('-s', '--scheme',  default='fullcorr', help='correlation scheme (only affect which combined workspace to pick)')
@click.option('-c', '--channels',  required=True, help='correlation scheme (only affect which combined workspace to pick)')
def kl_likelihood(**kwargs):
    input_file, poi, channels, scheme = kwargs['input_folder'], kwargs['poi'], kwargs['channels'], kwargs['scheme']
    kwargs['outdir'] = f'{input_file}/likelihood/'

    channels = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
    input_files = [f'{input_file}/rescaled/nonres/{channel}/0_kl.root' for channel in channels]
    outnames = [f'{channel}_{poi}' for channel in channels]

    # append combined
    input_files.append(f'{input_file}/combined/nonres/A-{"_".join(channels)}-{scheme}/0_kl.root')
    outnames.append(f'combined_{poi}')

    kwargs.pop('input_folder')
    kwargs.pop('channels')
    kwargs.pop('scheme')
    for input_file, outname in zip(input_files, outnames):
        kwargs['input_file'] = input_file
        kwargs['outname'] = outname
        set_trace()
        scan_nll(**kwargs)
