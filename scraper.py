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

## TODO do not fetch images

def scrape_source(source):
	try:
		news_source = newspaper.build(source['url'])
		store_articles(source,news_source)
	except Exception as e:
		print(str(e))

def store_articles(source, news_source):
	client = MongoClient('mongodb://naberfeed.com:27017')
	db = client.naberfeed
	for i in range(0,news_source.size()):
		docs = []
		placeholder = copy.deepcopy(article_template)
		article = news_source.articles[0]
		article.download()
		article.parse()
		article.nlp()
		if article.text != '':
			placeholder['text'] = article.text
			placeholder['keywords'] = article.keywords
			placeholder['datePublished'] = article.publish_date
			placeholder['authors'] = article.authors
			placeholder['summary'] = article.summary
			placeholder['title'] = article.title
			placeholder['publisherUrl'] = source['url']
			placeholder['sourceUrl'] = article.url
			placeholder['city'] = source['city']
			placeholder['state'] = source['state']
			placeholder['zips'] = source['zip']
			placeholder['publisher'] = source['publisherName']
			docs.append(placeholder)
		if len(docs) > 0:
			db.articles.insert_many(docs)

if __name__ == '__main__':
	client = MongoClient('mongodb://naberfeed.com:27017')
	db = client.naberfeed
	sources = list(db.sources.find({'flagged':0}))
	# for source in sources:
	# 	scrape_source(source)
	Parallel(n_jobs=4)(delayed(scrape_source)(source) for source in sources)
	print('Done scraping')
