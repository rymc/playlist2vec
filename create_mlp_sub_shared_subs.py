import gensim
import pandas as pd
import json
import cPickle as pickle
from collections import defaultdict
dd = defaultdict(dict)
names=pd.read_csv('pid_names.csv', encoding='utf-8')
names['names'] = names['names'].str.lower()
names.set_index('names', inplace=True)
model = gensim.models.Doc2Vec.load('d2v-no-tokens-sharedname400dim-all.model')
#model = gensim.models.Doc2Vec.load('d2v-no-tokens-sharedname.model')
trackuris=pd.read_csv('pid-artist-trackuri-track.csv')
trackuris = trackuris[['pid','track_uri']]
#trackuris.set_index(['pid', 'track_uri'], inplace=True)
#trackuris.sortlevel(inplace=True)
pidtotracks = defaultdict(list)
count = 0
#for name, df in trackuris.groupby('pid'):
#    if count % 1000 == 0:
#        print count
 #   pidtotracks[name] = df['track_uri'].tolist()
 #   count += 1

#for index, row in trackuris.iterrows():
#    if count % 1000 == 0:
#        print count
#    pidtotracks[row['pid']].append(row['track_uri'])
#    count += 1

with open('pidtotracks.pickle', 'rb') as pick:
    pidtotracks=pickle.load(pick)

def findkey(lvalue):                                       
    try:
        withname=names.loc[lvalue]
        return withname['pid'].tolist()
    except Exception as e:
        print str(e)
        return []


def get_songs(pid):
    print "get song for PLAYLIST ",
    print plname
    isongs = []
    iartists=[]
    return vs 

from collections import Counter
def most_sim_pl(name):
     print "INPUT PLAYLIST:",
     print name
     songs = []
     artist = []
     pids = findkey(plname)
     # pids with name
     pids = set(pids)
     mos_sims = []
     for pid in pids:
         try:
             mos_sim = model.docvecs.most_similar(pid, topn=50)
         except Exception as e:
             print str(e)
             continue
         mos_sims= np.append(mos_sim, mos_sims)
     for n in mos_sim:
         isongs = pidtotracks[pid]
         for i in isongs:
             songs.append(i)
     c=Counter(songs)
     #pprint.pprint(c.most_common(20))
     return c.most_common(600)
     


import pprint


with open('challenge/challenge_set.json', 'r') as r:
    data = json.load(r)

#import pdb
#pdb.set_trace()
import numpy as np
with open('submission-full.csv', 'w') as f:
    for plcount, pl in enumerate(data['playlists']):
        if True or pl['num_samples'] == 0:
            try:
                plname = pl['name'].lower()
                plpid = pl['pid']
                mostcommon = most_sim_pl(plname)
                if len(mostcommon) < 600:
                    continue
                f.write(str(plpid)+",")
                seeds = []
                for t in pl['tracks']:
                    seeds.append(t['track_uri'])

                count = 0
                for ele in mostcommon:
                    if count == 500:
                        break
                    if ele[0] in seeds:
                        continue
                    f.write(ele[0])
                    f.write(",")
                    count += 1
                f.write("\n")
                f.flush()
            except Exception as e:
                print str(e)





