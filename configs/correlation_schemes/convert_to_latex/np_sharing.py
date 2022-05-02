import pandas as pd
import sys
import json
from pdb import set_trace
import numpy as np

job = sys.argv[1]
if job == 'nonres':
    np_name = '../HHH2022/nonres_kl_v11.json'
elif job == 'spin0':
    np_name = '/Users/zhangrui/Work/Code/HHcomb/hh_combination_fw/configs/np_map_spin0_v7.json'
else:
    print('python np_sharing.py nonres|spin0')
    assert(0)

with open(np_name) as f:
    dic = json.load(f)

dfs = []
chans = []
for channel in dic.keys():
    #if channel == 'bbbb' and job == 'nonres':
    #    continue
    dic_chan = dic[channel]
    dic_chan = { i: dic_chan[i] for i in dic_chan.keys() if not i.startswith('gamma_')}
    renamed_np = [i.replace('ATLAS_', '') for i in dic_chan.values()]
    df = pd.DataFrame(list(zip(renamed_np, [1]*len(renamed_np))), columns =[channel, '\\'+channel]).set_index(channel)
    df = df.loc[~df.index.duplicated(keep='first')]
    chans.append(channel)
    dfs.append(df)

df = pd.concat(dfs, axis=1).sort_index()
df.loc[:, 'keep'] = df.sum(axis=1)
df.insert(0, 'Description', '')

#cat = '^THEO\w+HH4b\w?'
#df_others = df[df.index.str.contains(cat, regex= True)]
#df = df[~df.index.str.contains(cat, regex= True)]

df_others = []
excludes = ['^THEO\w+HH4b\w?', '^THEO\w+Had$']
for cat in excludes:
    df_others.append(df[df.index.str.contains(cat, regex= True)])
    df = df[~df.index.str.contains(cat, regex= True)]

#categories = ['^EG', '^EL', '^FT', '^JET', '^MUON', '^TAUS', '^THEO', '^PH']
categories = {'HH': '^THEO\w+HH\w?', 'H': '^THEO\w+H\w?', 'THEO': '^THEO\w+$'}
for k, cat in categories.items():
    df_sub = df[df.index.str.contains(cat, regex= True)]
    df = df[~df.index.str.contains(cat, regex= True)]
    df_sub = df_sub.drop(['keep'], axis=1)
    df_sub = df_sub.replace([1.0, np.nan], ['*', ''], regex=True)
    df_sub.to_latex(f'np_share_{job}_{k}.tex')

df = df.append(pd.concat(df_others))
df = df.replace([1.0, np.nan], ['*', ''], regex=True)
df = df.drop(['keep'], axis=1)
df.to_latex(f'np_share_{job}_Others.tex')
