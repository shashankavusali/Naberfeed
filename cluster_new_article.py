from pymongo import MongoClient
from article_distance import ArticleDistance
from topic_extractor import TopicExtractor
import numpy as np


topics = []
a = ArticleDistance()
extractor = TopicExtractor()

def assign_to_cluster(article):
    dists = []
    for topic in topics:
        cluster_keywords = topic['cluster_word_counts']
        word_freq =
        m = np.mean()
        top_keywords = {k for k,v in cluster_keywords.items() if cluster_keywords[k] >= m}
        total_count = len(article.keywords)
        diff_words = set(article.keywords).difference(top_keywords)
        dist = int(len(diff_words)*100/total_count)
        dists.append(dist)
    if min(dists) > 40:
        topic_words,cluster_keywords = extractor.extract_topic_keywords([article.keywrods])
    else:
        idx = dists.index(min(dists))
        topic = topics[idx]

if __name__=='__main__':
    client = MongoClient('mongodb://naberfeed.com:27017')
    db = client.naberfeed
    topics = list(db.topics.find({},{'cluster_word_counts':1}))
    articles = list(db.articles.find({'cluster_id':-1},{'keywords':1}))
    for article in articles:
        assign_to_cluster(article)
