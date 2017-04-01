import numpy as np
import operator
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import linkage, cut_tree
from scipy.spatial import distance
from collections import Counter

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

def extract_topic_keywords(files):
    cluster_keywords = dict()
    for j in range(len(files)):
        filename = files[j]
        article_keywords = []
        with open(filename,'r') as f:
            words = f.read()
            if words:
                article_keywords.extend(words.split('\n'))
        for k in range(len(article_keywords)):
            word = article_keywords[k]
            cluster_keywords[word] = cluster_keywords.get(word,0)+1

    m = np.mean(list(cluster_keywords.values()))
    top_keywords = {k:v for k,v in cluster_keywords.items() if cluster_keywords[k] > m}
    topic_words = sorted(top_keywords.items(), key = operator.itemgetter(1),reverse = True)
    print(topic_words[0:5])
    return topic_words[0:5]

if __name__== '__main__':
    ## Clustering articles based on keywrods

    # Read distance matrix
    data = np.load('dissimilarity_matrix.npz')
    key = data.keys()[0]
    dist_mat = np.array(data[key])
    n = dist_mat.shape[0]
    dist_mat[range(n), range(n)] = 0
    d = distance.squareform(dist_mat)

    # Read file names
    data = np.load('article_file_names.npz')
    filenames = data[key]

    # Perform hierarchical clustering
    Z = linkage(d,method='complete')
    np.savez('cluster',Z)

    # Determine where to cut dendrogram
    c = get_optimal_clustering(Z)
    cluster_count = len(np.unique(c))
    cluster_article_count = [None]*cluster_count

    for i in range(cluster_count):
        article_count = np.sum(np.where(c==i,1,0))
        cluster_article_count[i] = (i,article_count)

    sorted_clusters = sorted(cluster_article_count, reverse = True, key = lambda x: x[1])

    ### Find the article names in each cluster
    large_clusters = sorted_clusters[0:5]

    files = [None]*5
    for i in range(5):
        t = large_clusters[i]
        cluster_id = t[0]
        article_indices = np.where(c==cluster_id)[0]
        files_in_cluster = filenames[article_indices]
        files[i] = files_in_cluster

    #Extract topics from clustered articles
    trending_topic_count = 5
    topics = [None] * trending_topic_count
    for i in range(len(files)):
        files_in_cluster = files[i]
        extract_topic_keywords(files_in_cluster)
