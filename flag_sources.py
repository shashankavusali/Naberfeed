import numpy as np
from pymongo import MongoClient
from clustering import Clustering
from article_distance import ArticleDistance
from scipy.spatial import distance


if __name__=='__main__':
    client = MongoClient('mongodb://naberfeed.com:27017')
    db = client['naberfeed']
    unq_sources = list(db.articles.aggregate([{'$group':{'_id':'$sourceUrl','count':{'$sum':1}}}]))
    urls  =  [source['_id'] for source in unq_sources]
    counts = [source['count'] for source in unq_sources]
    flagged_sources = []
    for url in urls:
        articles = list(db.articles.find({'sourceUrl':url},{'keywords':1,'_id':0}))
        keywords = [a['keywords'] for a in articles]
        if len(articles) > 10 :
            a_dist = ArticleDistance(keywords)
            dists = a_dist.article_pdist()
            n = dists.shape[0]
            dists[range(n), range(n)] = 0
            d = distance.squareform(dists)
            cluster = Clustering(d)
            c = cluster.get_clusters_at(1)
            cluster_count = len(np.unique(c))
            if cluster_count/n < 0.5:
                flagged_sources.append(url)
    db.sources.update_many({'url':{'$in':flagged_sources}},{'$set':{'flagged':1}})
