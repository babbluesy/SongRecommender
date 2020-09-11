# -*- encoding: utf-8 -*-
"""
pip install pymongo
"""
from pymongo import MongoClient   #mongodb 모듈 지정
import datetime
import pprint
import json
import os
import sys
from bson.objectid import ObjectId  #objectid 모듈 지정

def open_json(name):
    with open('./%s.json'%name,'r', -1, "utf-8") as f:
        dt=json.load(f)
    return dt

def open_file(name):
    with open(name, 'r', -1, "utf-8") as f:
        dt=json.load(f)
    return dt

sys.stdout.reconfigure(encoding='utf-8')

#mongodb 연결객체 생성
# client = MongoClient()
# client = MongoClient('localhost', '27017')  #접속IP, 포트
client = MongoClient('mongodb://localhost:27017/')

#데이터베이스 개체 가져오기
# db = client['------']
db = client.spotify

#컬렉션 개체 가져오기
"""
#아티스트 추가
artistsCol = db.artists

kpopArtists = open_json("data/artists/k-pop_artists_info")
for artist in kpopArtists:
    artistsCol.insert_one(artist)

"""


"""
#앨범 추가
albumsCol = db.albums
kpopAlbums = open_json("data/albums/k-pop_albums_info")
for albums in kpopAlbums:
    for album in kpopAlbums[albums]:
        albumsCol.insert_one(album)

"""


#트랙 추가
tracksCol = db.tracks
dir_l=os.listdir(u'./data/tracks/')
for artist in dir_l:
    albums = open_file('./data/tracks/' + artist)
    for album in albums['albums']:
        temp = {}
        for track in albums['albums'][album]:
            temp['id'] = track['id']
            temp['artists'] = track['artists']
            temp['duration_ms'] = track['duration_ms']
            temp['external_urls'] = track['external_urls']
            temp['name'] = track['name']
            temp['preview_url'] = track['preview_url']
            temp['track_number'] = track['track_number']
        tracksCol.insert_one(temp)



"""
tracksCol = db.tracks

for track in tracksCol.find():
    print(track)
"""
#컬렉션 확인하기
#print(db.collection_names())


#데이터 삭제하기
# result = posts.delete_one()      #조건과 일치하는 데이터중 하나만 삭제
# result = posts.delete_many()     #조건과 일치하는 데이터 모두 삭제
# result = posts.delete_many({})   #모두 삭제 (조건지정x)


#접속 해제
client.close()