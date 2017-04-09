import numpy as np
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from topic_extractor import TopicExtractor
from clustering import Clustering
from scipy.spatial import distance
from article_distance import ArticleDistance

if __name__ == '__main__':
    client = MongoClient('mongodb://naberfeed.com:27017')
    db = client.naberfeed

    articles = list(db.articles.find({},{'_id':1,'keywords':1}).limit(1000))
    article_keywords = np.array([article['keywords'] for article in articles])
    article_object_ids = np.array([article['_id'] for article in articles])

    a_dist = ArticleDistance(article_keywords)
    dists = a_dist.article_pdist()
    n = dists.shape[0]
    dists[range(n), range(n)] = 0
    d = distance.squareform(dists)

    cluster = Clustering(d)
    c = cluster.cluster()
    extractor = TopicExtractor()

    for i in range(len(np.unique(c))):
        articles = []
        indices = np.where(c==i)[0]
        articles.extend(article_object_ids[indices])
        whole_keywords = []
        whole_keywords.extend(article_keywords[indices])
        db.articles.update_many({'_id':{'$in':articles}},{'$set':{'cluster_id':i}})
        topic_words,cluster_word_counts = extractor.extract_topic_keywords(whole_keywords)
        topic ={'topic_words':topic_words,'doc_ids':articles,'doc_count':len(articles), 'cluster_id':i,'cluster_word_counts':cluster_word_counts,'date_created':datetime.now(),'date_updated':datetime.now()}
        db.topics.insert_one(topic)
