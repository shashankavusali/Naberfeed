import os
import json
import time
import copy
import newspaper
from datetime import datetime
from pymongo import MongoClient
from joblib import Parallel, delayed
from newspaper import NewsPool, Config

ZIPS = 'zips'

client = MongoClient('mongodb://naberfeed.com:27017')
db = client.naberfeed

with open('output.json') as file:
    data = json.load(file)
for state,state_papers in data.items():
    sources = []
    for city,city_papers in state_papers.items():
        zips = ''
        if ZIPS in city_papers.keys():
            zips = city_papers[ZIPS]
        for key in filter(lambda a: not a == ZIPS, city_papers.keys()):
            url = city_papers[key][0]
            source = {}
            source['state'] = state
            source['city'] = city
            source['url'] = url
            source['publisherName'] = key
            source['zip'] = zips
            source['flagged'] = 0
            sources.append(source)
    db.sources.insert_many(sources)
