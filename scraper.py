import os
import json
import time
import copy
import newspaper
from datetime import datetime
from pymongo import MongoClient
from joblib import Parallel, delayed
from newspaper import NewsPool, Config

ZIPS = 'zips'

with open('article_template.json') as file:
	article_template = json.load(file)

def scrape_state(state_name, cities):
	for city,city_papers in cities.items():
		papers = []
		sources = []
		zips = {}
		if ZIPS in city_papers.keys():
			zips = city_papers[ZIPS]
		location = {'city':city, 'state': state_name, 'zips':zips}
		for key in filter(lambda a: not a == ZIPS, city_papers.keys()):
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
			store_articles(key, source, location)

def store_articles(paper_name,source,location):
	client = MongoClient('mongodb://naberfeed.com:27017')
	db = client.naberfeed
	for i in range(0,source.size()):
		docs = []
		placeholder = copy.deepcopy(article_template)
		article = source.articles[0]
		article.parse()
		article.nlp()
		if article.text != '':
			placeholder['text'] = article.text
			placeholder['keywords'] = article.keywords
			placeholder['datePublished'] = article.publish_date
			placeholder['authors'] = article.authors
			placeholder['summary'] = article.summary
			placeholder['title'] = article.title
			placeholder['sourceUrl'] = article.source_url
			placeholder['city'] = location['city']
			placeholder['state'] = location['state']
			placeholder['zips'] = location['zips']
			docs.append(placeholder)
		if len(docs) > 0:
			db.articles.insert_many(docs)

if __name__ == '__main__':
	with open('output.json') as file:
		data = json.load(file)
	Parallel(n_jobs=4)(delayed(scrape_state)(key,val) for (key,val) in data.items())
	# for key,val in data.items():
	# 	scrape_state(key,val)
	# 	break
	print('Done scraping')
