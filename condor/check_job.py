import os, glob

id='6982775'
files = glob.glob(f'log/{id}*.err')
for name in files:
    file_size = os.stat(name).st_size
    if file_size > 0:
        with open(name.replace('err', 'out')) as f:
            lines = [i for i in f.readlines() if 'quickstats' in i]
            print(lines[0])

