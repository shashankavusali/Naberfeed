import numpy as np
import operator
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import linkage, cut_tree
from scipy.spatial import distance
from collections import Counter
from pymongo import MongoClient
from bson.objectid import ObjectId

def unique_ele_count(arr):
    return len(np.unique(arr))

def get_optimal_clustering(Z):
    X = range(20,40)
    c = cut_tree(Z, height = X)
    Y = np.apply_along_axis(unique_ele_count, axis = 0,arr=c )
    #plt.plot(X,Y)
    optimal_cluster_count = Counter(Y).most_common(1)[0][0]
    idx =  max(np.where(Y==optimal_cluster_count)[0])
    return c[:,idx]

def extract_topic_keywords(keywords):
    cluster_keywords = dict()
    for article_keywords in keywords:
        for word in article_keywords:
            cluster_keywords[word] = cluster_keywords.get(word,0)+1
    m = np.mean(list(cluster_keywords.values()))
    top_keywords = [k for k,v in cluster_keywords.items() if cluster_keywords[k] >= m]
    cluster_keywords = sorted(cluster_keywords.items(), key = operator.itemgetter(1),reverse = True)
    return top_keywords[0:5],cluster_keywords

if __name__== '__main__':
    ## Clustering articles based on keywrods

    # Read distance matrix
    data = np.load('dissimilarity_matrix.npz')
    key = data.keys()[0]
    dist_mat = np.array(data[key])
    n = dist_mat.shape[0]
    dist_mat[range(n), range(n)] = 0
    d = distance.squareform(dist_mat)
    client = MongoClient('mongodb://naberfeed.com:27017')
    db = client.naberfeed

    # Read file names
    data = np.load('article_keywords.npz')
    key = data.keys()[0]
    article_keywords = data[key]

    data = np.load('article_object_ids.npz')
    article_object_ids = data[key]

    # Perform hierarchical clustering
    Z = linkage(d,method='complete')
    np.savez('cluster',Z)

    # Determine where to cut dendrogram
    c = get_optimal_clustering(Z)

    for i in range(len(np.unique(c))):
        articles = []
        article_indices = np.where(c==i)[0]
        articles.extend(article_object_ids[article_indices])
        whole_keywords = list(db.articles.find({'_id':{'$in':articles}},{'_id':0,'keywords':1}))
        whole_keywords = [k['keywords'] for k in whole_keywords]
        db.articles.update_many({'_id':{'$in':articles}},{'$set':{'cluster_id':i}})
        topic_words,cluster_word_counts = extract_topic_keywords(whole_keywords)
        topic ={'topic_words':topic_words,'doc_ids':articles,'doc_count':len(articles), 'cluster_id':i,'cluster_word_counts':cluster_word_counts}
        db.topics.insert_one(topic)

    # # sorted_clusters = sorted(cluster_article_count, reverse = True, key = lambda x: x[1])
    #
    # ### Find the article names in each cluster
    # large_clusters = sorted_clusters[0:5]
    #
    # clusterkeywords = [None]*5
    # for i in range(5):
    #     t = large_clusters[i]
    #     cluster_id = t[0]
    #     article_indices = np.where(c==cluster_id)[0]
    #     akeywords = article_keywords[article_indices]
    #     # objids = article_object_ids[article_indices]
    #     # cursor = db.articles.find({'_id':{'$in':objids}})
    #     # for doc in cursor:
    #     #     print(doc)
    #     clusterkeywords[i] = akeywords
    #
    # #Extract topics from clustered articles
    # trending_topic_count = 5
    # topics = [None] * trending_topic_count
    # for i in range(len(clusterkeywords)):
    #     extract_topic_keywords(clusterkeywords[i])
