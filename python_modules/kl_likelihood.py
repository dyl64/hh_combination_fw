from pdb import set_trace
import sys
import os
import re
import yaml
import click

from quickstats.clis.likelihood_scan import likelihood_scan

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
@click.option('-i', '--input_folder', required=True, help='Path to the task.')
@click.option('-s', '--scheme',  default='fullcorr', help='correlation scheme (only affect which combined workspace to pick)')
@click.option('-c', '--channels',  required=True, help='individual channels to include (comma separable); combined channel always included')
@click.option('--include-chan/--skip-chan', default=True, help='include or skip individual channels')
@click.option('-o', '--output',  default='likelihood', help='output folder')
@click.option('--kl_options',  default='', help='other likelihood_scan optioins')
@click.option('--splusb/--bonly',  default=True, help='Test against kl=1 or kl=0')
def kl_likelihood(**kwargs):
    input_file, output, poi, channels, scheme, kl_options = kwargs['input_folder'], kwargs['output'], kwargs['poi'], kwargs['channels'], kwargs['scheme'], kwargs['kl_options']
    output = '/'.join([output, 'kl1' if kwargs['splusb'] else 'kl0'])
    channels = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
    scan_min, scan_max, scan_step = kwargs['scan_min'], kwargs['scan_max'], kwargs['scan_step']
    outdir = f'{input_file}/{output}/'

    if kwargs['include_chan']:
        input_files = [f'{input_file}/rescaled/nonres/{channel}/0_kl.root' for channel in channels]
        outnames = [f'{channel}_{poi}' for channel in channels]
    else:
        input_files, outnames = [], []

    # append combined
    input_files.append(f'{input_file}/combined/nonres/A-{"_".join(channels)}-{scheme}/0_kl.root')
    outnames.append(f'combined_{poi}')

    other_options = ''
    other_options += ('--cache' if kwargs['cache'] else '--no-cache')

    print(input_files)
    for input_file, outname in zip(input_files, outnames):
        # generate asimov using CLI tool
        output_file = input_file.replace(".root", ('.poi_1' if kwargs['splusb'] else '.poi_0') + ".root")
        fix_param = 'xsec_br=1,klambda=1'
        command = f'quickstats generate_standard_asimov -t -2 -p {poi} -d combData -i {input_file} -o {output_file} --fix {fix_param} --snapshot nominalNuis'
        print(command)
        os.system(command)

        # scan likelihood using CLI tool
        fix_param = 'xsec_br=1'
        command = f'quickstats likelihood_scan -i {output_file} --min {scan_min} --max {scan_max} --step {scan_step} -d asimovData_1_NP_Nominal --parallel -1 --print_level -1 -p {poi} -o {outname} {other_options} --outdir {outdir} --fix {fix_param} {kl_options}'
        print(command)
        os.system(command)
