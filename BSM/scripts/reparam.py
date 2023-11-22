from BSM_utils import TaskPipelineBSM
from BSM_utils import TaskCombBSM
import yaml

config_file='/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/BSM/utils/BSMconfig.yaml'
with open(config_file, "r") as f:
            config = yaml.safe_load(f)

# channels = ['bbbb','bbtautau','bbyy']
channels = ['bbtautau','bbyy']
# channels = ['bbbb']

#Modification
for channel in channels:
    print("Start reparamterization of "+channel)
    task_config = {}
    task_config['channel'] = channel
    dataset              = config.get('dataset', {})
    _define_parameters   = config.get('define_parameters', {})
    _rename_parameters   = config.get('rename_parameters', {})
    _fix_parameters      = config.get('fix_parameters', {})
    _reparam_pois        = config.get('reparam_pois',{})
    task_config['old_poiname'] = ''
    task_config['define_parameters'] = _define_parameters.get(channel, None)
    task_config['rename_parameters'] = _rename_parameters.get(channel, None)
    task_config['reparam_pois'] = _reparam_pois.get(channel,None)
    task_config['old_dataname'] = 'combData'
    task_config['new_dataname'] = 'combData'
    task_config['input_dir'] = '/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/BSM/20221118'
    task_config['output_dir'] = '/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/BSM/20230912'
    task_config['resonant_type'] = 'spin0'
    # task_config['file_expr'] = '<mass[F]>'
    task_config['filter_expr'] = 'mass=450'


    pipeline = TaskPipelineBSM(**task_config)
    pipeline.modify()
#End of modification