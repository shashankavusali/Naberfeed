from joblib import Parallel, delayed
from pymongo import MongoClient
from scipy.spatial.distance import pdist
from clustering import Clustering
from article_distance import ArticleDistance
import numpy as np
import time


if __name__=='__main__':
    client = MongoClient('mongodb://naberfeed.com:27017')
    db = client['naberfeed']
    unq_sources = list(db.articles.aggregate([{'$group':{'_id':'$sourceUrl','count':{'$sum':1}}}]))
    urls  =  [source['_id'] for source in unq_sources]
    counts = [source['count'] for source in unq_sources]
    for url in urls:
        articles = list(db.articles.find({'sourceUrl':url},{'keywords':1,'_id':0}))
        keywords = [a['keywords'] for a in articles]
        cluster = Clustering()
