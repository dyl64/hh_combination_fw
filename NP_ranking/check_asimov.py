## check the NP values and global values in a workspace
import ROOT
from quickstats.components import ExtendedModel, ExtendedMinimizer

model = ExtendedModel('/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output_mu_unblind/combined/nonres/A-bbtautau_bbyy-fullcorr/asimov1.0.root', data_name='asimovData_1')
#model = ExtendedModel('/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/batches/v140invfb_20210821_CI/output_mu_unblind/rescaled/nonres/bbyy/asimov0.0.root', data_name='asimovData_0')
print('before xsec_br', model.workspace.var("xsec_br").getVal())
for np in model.nuisance_parameters:
    print("NP={:60s} {}".format(np.GetName(), np.getVal()))

for glob in model.global_observables:
    print("Globs={:60s} {}".format(glob.GetName(), glob.getVal()))




minimizer = ExtendedMinimizer("minimizer", model.pdf, model.data)
nll_commands = [ROOT.RooFit.NumCPU(1, 3),
                        ROOT.RooFit.Constrain(model.nuisance_parameters),
                        ROOT.RooFit.GlobalObservables(model.global_observables),
                        ROOT.RooFit.Offset(True)]
minimizer.minimize(nll_commands=nll_commands, default_strategy=1)

print('after xsec_br', model.workspace.var("xsec_br").getVal())
for np in model.nuisance_parameters:
    print("NP={:60s} {}".format(np.GetName(), np.getVal()))

for glob in model.global_observables:
    print("Globs={:60s} {}".format(glob.GetName(), glob.getVal()))
