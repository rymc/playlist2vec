import json
import cPickle as pickle
from pprint import pprint
import gensim 
from gensim.models.doc2vec import TaggedDocument
import nltk
from nltk.corpus import stopwords

docs = []
import glob
from collections import defaultdict
pid = []
names = []
for i, j in enumerate(glob.glob("data/*.json")):
    with open(j) as f:
        data = json.load(f)

    for pl in data['playlists']:
        pid.append(pl['pid'])
        names.append(pl['name'])

import pandas as pd
df = pd.DataFrame(
        {'pid': pid,
         'names': names
        }
        ).to_csv('pid_names.csv',  encoding='utf-8')
