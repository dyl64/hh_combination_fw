import json, os
import click
import quickstats
from quickstats.components import AnalysisBase

@click.command(name='pvalue_new')
@click.option('-i', '--input_file', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-s', '--snapshot', required=False, default='nominalNuis', help='snapshot to load')
@click.option('--blind/--unblind', 'do_blind', default=True, show_default=True, help='Blind/unblind analysis')
@click.option('-c', '--cache', required=False, default=None, help='root file to store asimov')
@click.option('-o', '--output', required=False, default='./pvalue.json', help='json file to store')
def pvalue_new(input_file, poi_name, dataset, snapshot, do_blind, cache, output):
    uncap=True
    analysis = AnalysisBase(input_file, data_name=dataset, poi_name=poi_name, config={"snapshot_name":snapshot})

    if do_blind:
        # use S+B prefit asimov
        analysis.generate_standard_asimov(asimov_types=[-2])
        if cache:
            analysis.model.workspace.writeToFile(cache)
        analysis.set_data("asimovData_1_NP_Nominal")

    fit_result = analysis.nll_fit(poi_val = 0, mode=0)
    
    # Write out results next to the input file
    if not output.endswith('.json'):
        output += '/pvalue.json'
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        json.dump(fit_result, f, indent=4)
    print('Save to', output)
    print(fit_result)

if __name__ == '__main__':
    pvalue_new()
