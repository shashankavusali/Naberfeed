from joblib import Parallel, delayed
from pymongo import MongoClient
from scipy.spatial.distance import pdist
import numpy as np
import time


if __name__=='__main__':
    client = MongoClient('mongodb://naberfeed.com:27017')
    db = client.naberfeed
    cursor = db.articles.aggregate({'$group':{'_id':'sourceUrl','count':{'$sum',1}}})
    for source in cursor:
        
