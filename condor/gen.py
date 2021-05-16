import numpy as np

total = 23
step = 1
channel = 'bbbb'
job = 'spin0'
process = 'process_channels'
for i in range(0, total, step):
    print('Arguments = {0} {1} {2} {3} {4}'.format(process, job, channel, i, i+step))
    print('Queue 1')


process = 'combine'
job = 'lambdapt'
batch_tag = '../../input/20210213'
low, hi = -10, 10
step = 0.2
for i in np.arange(hi, low, -step):
    i = '{:.1f}'.format(i)
    print('Arguments = {0} {1} {2} batch_tag {3}'.format(process, job, i, batch_tag))
    print('Queue 1')
print([float('{:.1f}'.format(i)) for i in np.arange(hi, low, -step)])
