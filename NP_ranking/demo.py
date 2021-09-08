import os
import ROOT
from quickstats.components import ExtendedModel
base_path = "/afs/cern.ch/work/c/chlcheng/public/HHComb/input_individual_v4/bbyy/nonres"
fname = os.path.join(base_path, "0_kl_1p0.root")
model = ExtendedModel(fname)
constraints = model.pair_constraints(to_str=True)
constraint = [i for i in constraints if i[1] == 'THEO_ACC_PDFalphas_HH_ggF'][0]

constraint_pdf = model.workspace.obj(constraint[0])
constraint_np = model.workspace.obj(constraint[1])
constraint_glob = model.workspace.obj(constraint[2])
