import operator
import numpy as np

class TopicExtractor(object):
    """docstring for TopicExtractor."""
    def __init__(self):
        super(TopicExtractor, self).__init__()

    def extract_topic_keywords(self,keywords):
        cluster_keywords = dict()
        for article_keywords in keywords:
            for word in article_keywords:
                cluster_keywords[word] = cluster_keywords.get(word,0)+1
        m = np.mean(list(cluster_keywords.values()))
        top_keywords = [k for k,v in cluster_keywords.items() if cluster_keywords[k] >= m && len(k) > 2]
        cluster_keywords = sorted(cluster_keywords.items(), key = operator.itemgetter(1),reverse = True)
        return top_keywords[0:5],cluster_keywords
