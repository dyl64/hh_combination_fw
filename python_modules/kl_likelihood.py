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
@click.option('--combine/--skip-combine', default=True, help='include or skip combined')
@click.option('--hypothesis_type', default=1, type=click.Choice(['0', '1', '2']), required=True, 
              help='case 0: Test against kl=0;  case 1: Test against kl=1; case 2: using obsData;')

def kl_likelihood(**kwargs):
    input_file, output, poi, channels, scheme, kl_options, hypo_type = kwargs['input_folder'], kwargs['output'], kwargs['poi'], kwargs['channels'], kwargs['scheme'], kwargs['kl_options'], int(kwargs['hypothesis_type'])
    # output = '/'.join([output, 'kl1' if kwargs['splusb'] else 'kl0'])
    output = '/'.join([output, f'kl{hypo_type}'])
    channels = sorted(channels.split(','), key=lambda x: (x.casefold(), x.swapcase()))
    scan_min, scan_max, scan_step = kwargs['scan_min'], kwargs['scan_max'], kwargs['scan_step']
    outdir = f'{input_file}/{output}/'

    if kwargs['include_chan']:
        input_files = [f'{input_file}/rescaled/nonres/{channel}/0_kl.root' for channel in channels]
        outnames = [f'{channel}_{poi}.json' for channel in channels]
    else:
        input_files, outnames = [], []

    # append combined
    if kwargs['combine']: 
        input_files.append(f'{input_file}/combined/nonres/A-{"_".join(channels)}-{scheme}/0_kl.root')
        outnames.append(f'combined_{poi}.json')

    other_options = ''
    other_options += ('--cache' if kwargs['cache'] else '--no-cache')

    print(input_files)
    for input_file, outname in zip(input_files, outnames):
        # if input_file != "/lustre/collider/zhangyulei/ATLAS/HHHCombination/hh_combination_fw/output/kl_likelihood/combined/nonres/A-bbtautau_bbyy-fullcorr/0_kl.root":
        #     continue
        # generate asimov using CLI tool
        # output_file = input_file.replace(".root", ('_poi_1' if kwargs['splusb'] else '_poi_0') + ".root")
        # fix_param = f'xsec_br=1,{poi}=1' if kwargs['splusb'] else f'xsec_br=1,{poi}=0'
        # asimovDataType = -2 if kwargs['splusb'] else -1

        
        output_file = input_file
        outDataSetName = 'combData'
        if hypo_type != 2:
            output_file = input_file.replace(".root", f'_poi_{hypo_type}' + ".root")
            fix_param = f'xsec_br=1,{poi}={hypo_type}'
            asimovDataType = -1 - hypo_type
            outDataSetName = f"asimovData_{hypo_type}_NP_Nominal"
            command = f'quickstats generate_standard_asimov -t {asimovDataType} -p {poi} -d combData -i {input_file} -o {output_file} --fix {fix_param}'
            print(command)
            os.system(command)

        # scan likelihood using CLI tool
        fix_param = 'xsec_br=1'
        command = f'quickstats likelihood_scan -i {output_file} --param_expr "{poi}={scan_min}_{scan_max}_{scan_step}" -d {outDataSetName} --parallel -1 --print_level 1 -o {outname} {other_options} --outdir {outdir} --fix {fix_param} {kl_options}'
        print(command)
        os.system(command)
