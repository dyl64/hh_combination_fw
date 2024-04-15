import pandas as pd
import sys
import json
import numpy as np

np_name = sys.argv[1] if len(sys.argv) > 1 else 'correlation_base.json'

with open(np_name) as f:
    dic = json.load(f)

dfs = []
chans = []
for channel in dic.keys():
    dic_chan = dic[channel]
    dic_chan = { i: dic_chan[i] for i in dic_chan.keys() if not i.startswith('gamma_')}
    renamed_np = [i.replace('ATLAS_', '') for i in dic_chan.values()]
    df = pd.DataFrame(list(zip(renamed_np, [1]*len(renamed_np))), columns =[channel, '\\'+channel]).set_index(channel)
    df = df.loc[~df.index.duplicated(keep='first')]
    chans.append(channel)
    dfs.append(df)

df = pd.concat(dfs, axis=1).sort_index()
df.loc[:, 'keep'] = df.sum(axis=1)
df.insert(len(df.columns), 'Description', '')
df = df.drop(['keep'], axis=1)
df = df.replace([1.0, np.nan], ['*', ''], regex=True)
df.index = df.index.str.replace('_', ' ')
df = df.reset_index()
df.index += 1

df.to_csv("check_corr.csv")
df.to_latex("check_corr.tex")

#cat = '^THEO\w+HH4b\w?'
#df_others = df[df.index.str.contains(cat, regex= True)]
#df = df[~df.index.str.contains(cat, regex= True)]

#df_others = []
#excludes = ['^THEO\w+HH4b\w?', '^THEO\w+Had$']
#for cat in excludes:
#    df_others.append(df[df.index.str.contains(cat, regex= True)])
#    df = df[~df.index.str.contains(cat, regex= True)]
#
##categories = ['^EG', '^EL', '^FT', '^JET', '^MUON', '^TAUS', '^THEO', '^PH']
#categories = {'HH': '^THEO\w+HH\w?', 'H': '^THEO\w+H\w?', 'THEO': '^THEO\w+$'}
#for k, cat in categories.items():
#    df_sub = df[df.index.str.contains(cat, regex= True)]
#    df = df[~df.index.str.contains(cat, regex= True)]
#    df_sub = df_sub.drop(['keep'], axis=1)
#    df_sub = df_sub.replace([1.0, np.nan], ['*', ''], regex=True)
#    df_sub.to_latex(f'np_share_{k}.tex')
#
#set_trace()
#df = df.append(pd.concat(df_others))
#df = df.replace([1.0, np.nan], ['*', ''], regex=True)
#df = df.drop(['keep'], axis=1)
#df.to_latex(f'np_share_Others.tex')
#