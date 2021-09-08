import ROOT
from quickstats.components import AnalysisObject, ExtendedModel, ExtendedMinimizer
filename = "/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210903_CI/output_mu_unblind/rescaled/nonres/bbyy//asimov_temp-2.root"

model = ExtendedModel(filename)

plt = model.plot_distributions(category='SM_1',
        current_distributions=True,
        datasets=['asimovData_0', 'asimovData_1', 'dataset_temp']
            )
plt.savefig('line_plot.pdf') 
