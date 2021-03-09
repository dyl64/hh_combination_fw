total = 23
step = 1
channel = 'bbbb'
job = 'spin0'
process = 'pipeline'
for i in range(0, total, step):
    print('Arguments = {0} {1} {2} {3} {4}'.format(process, job, channel, i, i+step))
    print('Queue 1')
