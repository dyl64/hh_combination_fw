import numpy as np

## Run2
#total = 23
#step = 1
#channel = 'bbbb'
#job = 'spin0'
#process = 'process_channels'
#for i in range(0, total, step):
#    print('Arguments = {0} {1} {2} {3} {4}'.format(process, job, channel, i, i+step))
#    print('Queue 1')
#
#
#process = 'combine'
#job = 'lambdapt'
#batch_tag = '../../input/20210213'
#low, hi = -10, 10
#step = 0.2
#for i in np.arange(hi, low, -step):
#    i = '{:.1f}'.format(i)
#    print('Arguments = {0} {1} {2} batch_tag {3}'.format(process, job, i, batch_tag))
#    print('Queue 1')
#print([float('{:.1f}'.format(i)) for i in np.arange(hi, low, -step)])

## Prospects
# python gen.py ../tutorials/projection/commands.sh
import sys
import re
commands = sys.argv[1]
print(commands)

with open(commands) as f:
    lines = f.readlines()

process_channels_commands = [x for x in lines if 'HHComb process_channels' in x]
combine_ws_commands = [x for x in lines if 'HHComb combine_ws' in x]
print(process_channels_commands)
with open("process_commands.sh", 'w') as f:
    for process_channels_cmd_str in process_channels_commands:
        f.write("Arguments = "+process_channels_cmd_str.replace(" ", "____").replace("\"", "\\\""))
        f.write("Queue 1\n")

with open("combine_commands.sh", 'w') as f:
    for combine_ws_cmd_str in combine_ws_commands:
        f.write("Arguments = "+combine_ws_cmd_str.replace(" ", "____").replace("\"", "\\\""))
        f.write("Queue 1\n")
