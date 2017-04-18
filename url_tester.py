import requests
from pymongo import MongoClient

client = MongoClient('mongodb://naberfeed.com:27017')
db = client.naberfeed
sources = list(db.sources.find({},{'url':1}))
count = 0
for source in sources:
    try:
        request = requests.get(source['url'])
        request = requests.get(source['url'])
        if request.status_code == 200:
            db.sources.update_many({'url':source['url']},{'$set':{'flagged':0}})
        else:
            count = count + 1
            db.sources.update_many({'url':source['url']},{'$set':{'flagged':1}})
    except Exception as e:
            count = count + 1
            db.sources.update_many({'url':source['url']},{'$set':{'flagged':1}})
print(count)
