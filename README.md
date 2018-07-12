# playlist2vec

This is the code we used for the RecSys 2018 Spotify playlist recommendation challenge. 

# to run (requires the non-public dataset)

Assuming the data is located in the 'data' directory under the directory containing the code..

Run write_pl_name.py to generate the file mapping playlist names to pids.

Download and gunzip the above file which maps pids to trackuris.

Run d2v.py

Run create_p2v_submission.py to generate playlists using the model built in the previous step.
