import json
import cPickle as pickle
from pprint import pprint
import gensim 
from gensim.models.doc2vec import TaggedDocument
import nltk

docs = []
import glob
from collections import defaultdict

class Corpus(object):
    """
    Iterable: on each iteration, return bag-of-words vectors,
    one vector for each document.
 
    Process one document at a time using generators, never
    load the entire corpus into RAM.
 
    """
    def __init__(self):
        self.total_examples = 0
 
    def __iter__(self):
        """
        Again, __iter__ is a generator => Corpus is a streamed iterable.
        """
        for i, j in enumerate(glob.glob("data/*.json")):
            with open(j) as f:
                data = json.load(f)

            for pl in data['playlists']:
                name = []
#                name.append("pid_"+str(pl['pid']))
                name.append(pl['name'].lower())
                doc =[]
                for t in pl['tracks']:
                    doc.append(t['track_uri'])
                    doc.append(t['artist_uri'])
                    doc.append(t['album_uri'])
                 #   pid_to_tracks[t['track_name']].append(pl['pid'])
                self.total_examples += 1
                yield TaggedDocument(words=doc, tags=name)



docs = Corpus()

model = gensim.models.Doc2Vec(
        docs,
        size=400,
        window=500,
        dm=0,
        workers=16)

model.train(docs, total_examples=docs.total_examples, epochs=10)
model.save("d2v-no-tokens-400dim-all.model")
