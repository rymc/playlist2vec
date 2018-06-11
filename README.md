# playlist2vec

You will need a large mapping datafile which can be downloaded from:
https://seis.bris.ac.uk/~rm17770/pid-trackuri-track.csv.gz

# to run

Assuming the data is located in the 'data' directory under the directory containing the code..

Run write_pl_name.py to generate the file mapping playlist names to pids.

Download and gunzip the above file which maps pids to trackuris.

Run d2v.py

Run create_p2v_submission.py to generate playlists using the model built in the previous step.
