import json
import click
import quickstats
from quickstats.components import AnalysisBase

@click.command(name='pvalue_new')
@click.option('-i', '--input_file', required=True, help='path or file to the processed workspaces')
@click.option('-poi', 'poi_name', required=False, default='xsec_br', help='poi name in workspace')
@click.option('-d', '--dataset', required=False, default='combData', help='dataset name in workspace')
@click.option('-o', '--output', required=False, default=None, help='file to store asimov')
def pvalue_new(input_file, poi_name, dataset, output):
    uncap=True
    
    analysis = AnalysisBase(input_file, data_name=dataset, poi_name=poi_name, config={"snapshot_name":"nominalNuis"})
    analysis.generate_standard_asimov(asimov_types=[-2])
    if output:
        analysis.model.workspace.writeToFile(output)
    analysis.set_data("asimovData_1_NP_Nominal")
    fit_result = analysis.nll_fit(poi_val = 0, mode=0)
    
    # Write out results next to the input file
    output_file = input_file[::-1].replace('.root'[::-1], '_pvalue_expblind.json'[::-1], 1)[::-1]
    with open(output_file, 'w') as f:
        json.dump(fit_result, f, indent=4)
    print('Save to', output_file)
    print(fit_result)

if __name__ == '__main__':
    pvalue_new()
