from BSM_utils import TaskPipelineBSM
from BSM_utils import TaskCombBSM
import yaml

config_file='/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/BSM/utils/BSMconfig.yaml'
with open(config_file, "r") as f:
            config = yaml.safe_load(f)

# channels = ['bbbb','bbtautau','bbyy']
channels = ['bbtautau','bbyy']

##Combination
task_config = {}
task_config['channels'] = channels
dataset              = config.get('dataset', {})
comb_pois        = config.get('comb_pois',{})

task_config['correlation_scheme'] = '/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/configs/correlation_schemes/Legacy2022/spin0_v2.json'
task_config['data_name'] = 'combData'
task_config['input_dir'] = '/afs/cern.ch/work/y/yuhao/public/DiHiggs/hh_combination_fw/BSM/20230912'
task_config['comb_pois'] = comb_pois
task_config['resonant_type'] = 'spin0'
task_config['filter_expr'] = 'mass=450'


pipeline=TaskCombBSM(**task_config)
pipeline.combine()