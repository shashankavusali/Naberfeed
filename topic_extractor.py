import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, cut_ree
from scipy.spatial import distance

data = np.load('cluster.npz')
Z = data['arr_0']
