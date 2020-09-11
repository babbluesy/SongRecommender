"""
pip3 install spotdl
"""

import os
from pymongo import MongoClient   #mongodb 모듈 지정
import tensorflow as tf
import numpy as np

client = MongoClient('mongodb://localhost:27017/')

db = client.spotify
tracksCol = db.tracks


@tf.function
def collectMP3(idx, skip_range, limit_param):
    with tf.device("/gpu:0"):
        for track in tracksCol.find(no_cursor_timeout=True).skip(skip_range).limit(limit_param):
            try:
                idx += 1
                print(idx)
                num = os.system('spotdl --overwrite force --song https://open.spotify.com/track/{}'.format(track['id']))
            except:
                idx += 1
                print('error')
    return num

collectMP3(0, 7 * 1000, 1000)
