import numpy as np
from scipy.cluster.hierarchy import linkage, cut_tree
from collections import Counter

class Clustering(object):
    """docstring for ."""
    def __init__(self, dists):
        super(Clustering,self).__init__()
        self.dists = dists
        self.Z = ''

    def unique_ele_count(self,arr):
        return len(np.unique(arr))

    def get_optimal_clustering(self):
        X = range(20,40)
        c = cut_tree(self.Z, height = X)
        Y = np.apply_along_axis(self.unique_ele_count, axis = 0,arr=c )
        optimal_cluster_count = Counter(Y).most_common(1)[0][0]
        idx =  max(np.where(Y==optimal_cluster_count)[0])
        return c[:,idx]

    def get_clusters_at(self, height):
        self.Z = linkage(self.dists,method='complete')
        return cut_tree(self.Z, height = height)

    def cluster(self):
        self.Z = linkage(self.dists,method='complete')
        return self.get_optimal_clustering()
