from joblib import Parallel, delayed
from pymongo import MongoClient
from scipy.spatial.distance import pdist
import numpy as np
import time

def calculate_distance(point1, point2):
    keyword_count = len(point1)+len(point2)
    common_count = len(set(point1).intersection(point2))
    # print(100*(keyword_count - 2 * common_count)/keyword_count)
    return int(100*(keyword_count - 2 * common_count)/keyword_count)

def pairwise_distance(datapoints):
    points_count = len(datapoints)
    dists = np.zeros((points_count, points_count),dtype=np.int)
    for i in range(points_count):
        for j in range(i+1, points_count):
            dists[i,j] = calculate_distance(datapoints[i], datapoints[j])
            dists[j,i] = dists[i,j]
    np.savez('dissimilarity_matrix',dists)

if __name__ == '__main__':
    client = MongoClient('mongodb://naberfeed.com:27017')
    db = client.naberfeed
    articles = list(db.articles.find({},{'_id':1,'keywords':1}).limit(1000))
    article_keywords = [ article['keywords'] for article in articles]
    article_ids = [article['_id'] for article in articles]
    np.savez('article_object_ids',article_ids)
    np.savez('article_keywords',article_keywords)
    keyword_list = [keyword for article in article_keywords for keyword in article]
    keywords = list(set(keyword_list))
    article_features = []
    for article in article_keywords:
        feature_vector = []
        feature_vector.extend([keyword_list.index(keyword) for keyword in article])
        article_features.append(feature_vector)
    start_time = time.time()
    # dists = pdist(article_features,calculate_distance)
    # np.savez('dissimilarity_matrix',dists)
    pairwise_distance(article_features)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
