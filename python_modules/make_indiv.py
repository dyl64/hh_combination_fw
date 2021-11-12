from quickstats.components.numerics import str_encode_value
from quickstats.components import ExtendedModel
from os import path
import numpy as np

input_file = '/afs/cern.ch/work/z/zhangr/HHcomb/FullRun2Workspaces/original/20211106_mu_all/bbyy/nonres/0_kl.root'
model = ExtendedModel(input_file, data_name='combData')
kl = model.workspace.var('klambda') 
kl.setConstant(True) 
values = np.arange(-2, 8, 0.2)
for value in values:
    kl.setVal(value) 
    output = f"{path.dirname(input_file)}/0_kl_{str_encode_value(value)}.root"
    model.save(output) 
    print('Save', output)
