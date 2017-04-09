from joblib import Parallel, delayed
from pymongo import MongoClient
from scipy.spatial.distance import pdist
import numpy as np
import time

class ArticleDistance(object):
    """docstring for Distance."""
    def __init__(self, article_keywords):
        super(ArticleDistance, self).__init__()
        self.article_keywords = article_keywords

    def calculate_distance(self,point1, point2):
        keyword_count = len(point1)+len(point2)
        common_count = len(set(point1).intersection(point2))
        return int(100*(keyword_count - 2 * common_count)/keyword_count)

    def pairwise_distance(self,datapoints):
        points_count = len(datapoints)
        dists = np.zeros((points_count, points_count),dtype=np.int8)
        for i in range(points_count):
            for j in range(i+1, points_count):
                dists[i,j] = self.calculate_distance(datapoints[i], datapoints[j])
                dists[j,i] = dists[i,j]
        return dists

    def article_pdist(self):
        keyword_list = [keyword for article in self.article_keywords for keyword in article]
        keywords = list(set(keyword_list))
        article_features = []
        for article in self.article_keywords:
            feature_vector = []
            feature_vector.extend([keyword_list.index(keyword) for keyword in article])
            article_features.append(feature_vector)
        start_time = time.time()
        dists = self.pairwise_distance(article_features)
        elapsed_time = time.time() - start_time
        return dists
