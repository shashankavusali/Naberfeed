from joblib import Parallel, delayed
import numpy as np
import os

base_directory = 'news'

def read_keywords_state(state_name):
    state_path = base_directory+ '/'+state_name
    article_keywords = []
    file_names =[]
    papers = get_valid_dir_list(state_path)
    for paper in papers:
        path = state_path + '/' + paper
        for article in filter(lambda x: '_keywords' in x ,get_valid_dir_list(path)):
            filename = path+'/'+article
            f = open(filename,'r')
            words = f.read()
            if words:
                article_keywords.append(words.split('\n'))
                file_names.append(filename)
    return article_keywords,file_names

def get_valid_dir_list(path):
    dir_list = os.listdir(path)
    return filter(lambda x: not x.startswith('.'), dir_list)

def calculate_distance(point1, point2):
    keyword_count = len(point1)+len(point2)
    common_count = len(set(point1).intersection(point2))
    return 100*(keyword_count - 2 * common_count)/keyword_count

def pairwise_distance(datapoints):
    points_count = len(datapoints)
    dists = np.zeros((points_count, points_count))
    for i in range(points_count):
        for j in range(i+1, points_count):
            dists[i,j] = calculate_distance(datapoints[i], datapoints[j])
            dists[j,i] = dists[i,j]
    np.savez('dissimilarity_matrix',dists)


valid_dir_list = get_valid_dir_list(base_directory)
article_keywords = []
article_file_names = []
for state_name in valid_dir_list:
    [keywords, file_names] = read_keywords_state(state_name)
    article_keywords.extend(keywords)
    article_file_names.extend(file_names)

np.savez('article_file_names',article_file_names)

keyword_list = [keyword for article in article_keywords for keyword in article]
keywords = list(set(keyword_list))
article_features = []
for article in article_keywords:
    feature_vector = []
    feature_vector.extend([keyword_list.index(keyword) for keyword in article])
    article_features.append(feature_vector)
pairwise_distance(article_features)
