from pdb import set_trace
import sys
import os
import re
import yaml
import click

from quickstats.clis.core import likelihood_scan, generate_asimov
from quickstats.components.likelihood import scan_nll

@click.command(name='kl_likelihood')
@click.option('--min', 'scan_min', type=float, required=True, 
              help='Minimum POI value to scan.')
@click.option('--max', 'scan_max', type=float, required=True, 
              help='Maximum POI value to scan.')
@click.option('--step', 'scan_step', type=float, required=True, 
              help='Scan interval.')
@click.option('-p', '--poi', default='klambda', show_default=True,
              help='POI to scan. If not specified, the first POI from the workspace is used.')
@click.option('--cache/--no-cache', default=True, show_default=True,
              help='Cache existing result')
@click.option('-f', '--fix', 'fix_param', default="mu*=1,mu_*=1,xsec_br=1", show_default=True,
              help='POI mu in bbtautau ws is floated. Note it is used in RooProduct::SigXsecOverSMVBF_modified and not regularised')
@click.option('-i', '--input_folder', required=True, help='Path to the task.')
@click.option('-s', '--scheme',  default='fullcorr', help='correlation scheme (only affect which combined workspace to pick)')
@click.option('-c', '--channels',  required=True, help='individual channels to include (comma separable); combined channel always included')
def kl_likelihood(**kwargs):
    input_file, poi, channels, scheme = kwargs['input_folder'], kwargs['poi'], kwargs['channels'], kwargs['scheme']
    fix_param = kwargs['fix_param']
    scan_min, scan_max, scan_step = kwargs['scan_min'], kwargs['scan_max'], kwargs['scan_step']
    outdir = f'{input_file}/likelihood/' # zhangr

    channels = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
    input_files = [] #[f'{input_file}/rescaled/nonres/{channel}/0_kl.root' for channel in channels]
    outnames = [] #[f'{channel}_{poi}' for channel in channels]

    # append combined
    input_files.append(f'{input_file}/combined/nonres/A-{"_".join(channels)}-{scheme}/0_kl.root')
    outnames.append(f'combined_{poi}')

    other_options = ''
    other_options += ('--cache' if kwargs['cache'] else '--no-cache')

    for input_file, outname in zip(input_files, outnames):
        # generate asimov using CLI tool
        output_file = input_file.replace(".root", ".asimov.root")
        command = f'quickstats generate_standard_asimov -t -2 -p {poi} -d combData -i {input_file} -o {output_file} --fix {fix_param} --snapshot nominalNuis'
        print(command)
        os.system(command)

        # scan likelihood using CLI tool
        command = f'quickstats likelihood_scan -i {output_file} --min {scan_min} --max {scan_max} --step {scan_step} -d asimovData_1_NP_Nominal --parallel -1 --print_level -1 -p {poi} -o {outname} {other_options} --outdir {outdir} --fix {fix_param} --snapshot nominalNuis'
        print(command)
        os.system(command)
