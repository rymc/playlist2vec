import gensim
import pandas as pd
import json
import cPickle as pickle
from collections import defaultdict
import sys

dd = defaultdict(dict)
names=pd.read_csv('pid_names.csv', encoding='utf-8')
names['names'] = names['names'].str.lower()
names.set_index('names', inplace=True)
model = gensim.models.Doc2Vec.load(sys.argv[1])
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
         print name
         infv = model.infer_vector([name], steps=50, alpha=0.025)
         mos_sim = model.docvecs.most_similar([infv], topn=50)
        
        # mos_sim = model.docvecs.most_similar(model.infer_vector([name], steps=50,  alpha=0.025), topn=50)
     for n in mos_sim:
         isongs, iartists = get_songs(n[0])
         for i in isongs:
             songs.append(i)
     c=Counter(songs)
     return c.most_common(600)

with open('challenge/challenge_set.json', 'r') as r:
    data = json.load(r)


def write_to_file(f, pl, most_similar):
        f.write(str(pl['pid'])+",")
        seeds = []
        for t in pl['tracks']:
            seeds.append(t['track_uri'])
        count = 0
        for ele in most_similar:
            if count == 500:
                break
            if ele[0] in seeds:
                continue
            f.write(ele[0])
            f.write(",")
            count += 1
        f.write("\n")
        f.flush()

def build_uris_from_pl(pl):
    uris = []
    for t in pl['tracks']:
        uris.append(t['track_uri'])
        uris.append(t['artist_uri'])
        uris.append(t['album_uri'])
    return uris


def retrieve_k_most_similar_songs(uris, k):
    mos_sim = model.wv.most_similar(uris, topn=(k*4))
    mos_sim_tracks = []
    for sim in mos_sim:
        if sim[0].startswith('spotify:track'):
            mos_sim_tracks.append(sim[0])
        if len(mos_sim_tracks) == k:
            break
    return mos_sim_tracks

import numpy as np
with open('submission-full.csv', 'w') as f:
    for plcount, pl in enumerate(data['playlists']):
        try:
            if 'name' in pl:
                plname = pl['name'].lower()
                mostcommon = most_sim_pl(plname)
                if len(mostcommon) < 600:
                    continue
                write_to_file(f, pl, mostcommon)
            else:
                uris = build_uris_from_pl(pl)
                tracks = retrieve_k_most_similar_songs(uris, 600)
                tracks = [[x] for x in tracks] #because we write ele[0] in write_to_file, tracks needs to be a list of tuples
                write_to_file(f, pl, tracks)
        except Exception as e:
            print str(e)

