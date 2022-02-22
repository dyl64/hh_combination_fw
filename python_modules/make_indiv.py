from quickstats.components.numerics import str_encode_value
from quickstats.components import ExtendedModel
from os import path
import numpy as np
import sys

input_file = sys.argv[1] # '/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/original/20211106_proj_all/projTheoExp_baseline/bbyy/nonres/0_kl.root'
param = sys.argv[2] if len(sys.argv) > 1 else 'kl'
var = 'klambda' if param == 'kl' else param
print('run', param, var)
assert(input_file.endswith(f'0_{param}.root')), f'{input_file} is not 0_{param}.root'

model = ExtendedModel(input_file, data_name='combData')
kl = model.workspace.var(var) 
kl.setConstant(True) 
values = np.arange(-2, 8+0.2, 0.2) if param == 'kl' else np.arange(-1.2, 1.2+0.1, 0.1)
for value in values:
    kl.setVal(value) 
    output = f"{path.dirname(input_file)}/0_{param}_{str_encode_value(value, n_digit=1)}.root"
    model.save(output) 
    print('Save', output)
