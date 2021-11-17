from quickstats.components.numerics import str_encode_value
from quickstats.components import ExtendedModel
from os import path
import numpy as np
import sys

input_file = sys.argv[1] # '/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/original/20211106_proj_all/projTheoExp_baseline/bbyy/nonres/0_kl.root'
assert(input_file.endswith('0_kl.root')), f'{input_file} is not 0_kl.root'

model = ExtendedModel(input_file, data_name='combData')
kl = model.workspace.var('klambda') 
kl.setConstant(True) 
values = np.arange(-2, 8+0.2, 0.2)
for value in values:
    kl.setVal(value) 
    output = f"{path.dirname(input_file)}/0_kl_{str_encode_value(value, n_digit=1)}.root"
    model.save(output) 
    print('Save', output)
