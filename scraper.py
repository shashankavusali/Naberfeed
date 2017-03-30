import os
import json
import newspaper
from newspaper import NewsPool, Config
from joblib import Parallel, delayed
from datetime import datetime
import time

def scrape_state(state_name, cities):
	for city,city_papers in cities.items():
		papers = []
		sources = []
		for key in filter(lambda a: not a == 'zips', city_papers.keys()):
			url = city_papers[key][0]
			try:
				source = newspaper.build(url)
				sources.append(source)
				papers.append({key:city_papers[key]})
			except Exception as e:
				print(str(e))
		config = Config()
		config.memorize_articles = True
		config.fetch_images = False
		news_pool = NewsPool(config)
		news_pool.set(sources)
		news_pool.join()
		for i in range(len(papers)):
			key,val = papers[i].popitem()
			source = sources[i]
			store_articles(key, source, state_name)

def store_articles(paper_name,source,state_name):
	directory_name = 'news/'+state_name+'/'+paper_name
	if not os.path.exists(directory_name):
		os.makedirs(directory_name)
	for i in range(0,source.size()):
		article = source.articles[i]
		article.parse()
		with open(directory_name+'/article_'+str(i)+'.txt','w') as f:
			f.write(article.text)
		article.nlp()
		with open(directory_name+'/article_'+str(i)+'_keywords.txt','w') as f:
			f.write('\n'.join(article.keywords))

if __name__ == '__main__':
	with open('output.json') as file:
		data = json.load(file)
	Parallel(n_jobs=4)(delayed(scrape_state)(key,val) for (key,val) in data.items())
	print('Done scraping')
