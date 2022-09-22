import numpy as np

## Prospects
# python gen.py ../tutorials/projection2022/commands.sh
import sys
import re
commands = sys.argv[1]
print(commands)

with open(commands) as f:
    lines = f.readlines()

process_channels_commands = [x for x in lines if 'HHComb process_channels' in x]
combine_ws_commands = [x for x in lines if 'HHComb combine_ws' in x]
print(process_channels_commands[0])
with open("process_commands.sh", 'w') as f:
    for process_channels_cmd_str in process_channels_commands:
        #f.write("Arguments = "+process_channels_cmd_str.replace(" ", "____").replace("\"", "\\\"").replace("<", "\<").replace(">", "\>")) # local run
        f.write("Arguments = "+process_channels_cmd_str.replace(" ", "____").replace("\"", "")) # condor submit
        f.write("Queue 1\n")

with open("combine_commands.sh", 'w') as f:
    for combine_ws_cmd_str in combine_ws_commands:
        #f.write("Arguments = "+combine_ws_cmd_str.replace(" ", "____").replace("\"", "\\\"").replace("<", "\<").replace(">", "\>")) # local run
        f.write("Arguments = "+combine_ws_cmd_str.replace(" ", "____").replace("\"", "")) # condor submit
        f.write("Queue 1\n")
