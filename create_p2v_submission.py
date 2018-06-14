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
trackuris=pd.read_csv('pid-artist-trackuri-track.csv')
trackuris = trackuris[['pid','track_uri']]
pidtotracks = defaultdict(list)
count = 0

with open('pidtotracks.pickle', 'rb') as pick:
    pidtotracks=pickle.load(pick)

def findkey(lvalue):                                       
    try:
        withname=names.loc[lvalue]
        return withname['pid'].tolist()
    except Exception as e:
        print str(e)
        return []


def get_songs(plname):
    print "get song for PLAYLIST ",
    print plname
    isongs = []
    iartists=[]
    pids = findkey(plname)
    if not type(pids) == list:
        pids = [pids]
    pids = set(pids)
    for count, pid in enumerate(pids):
        vs = pidtotracks[pid]
        isongs=np.append(isongs,vs)
        if count > 100 and len(isongs) >= 600:
            break
    return isongs, iartists

from collections import Counter
def most_sim_pl(name):
     print "INPUT PLAYLIST:",
     print name
     songs = []
     artist = []
     try:
         mos_sim = model.docvecs.most_similar(name, topn=50)
     except Exception as e:
         print str(e)
         print "lets infer"
         mos_sim = model.docvecs.most_similar(model.infer_vector([name], steps=50,  alpha=0.025), topn=50)
     for n in mos_sim:
         isongs, iartists = get_songs(n[0])
         for i in isongs:
             songs.append(i)
     c=Counter(songs)
     return c.most_common(600)

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

