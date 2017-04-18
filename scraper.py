import os
import json
import time
import copy
import newspaper
from datetime import datetime
from pymongo import MongoClient
from joblib import Parallel, delayed
from newspaper import NewsPool
from newspaper.configuration import Configuration
from difflib import SequenceMatcher
from urllib.parse import urlparse

ZIPS = 'zips'
blocklisted = ['http://www.legacy.com/']

with open('article_template.json') as file:
	article_template = json.load(file)

alog = open('article_log1.log','a')
slog = open('sources_log1.log','a')


## TODO do not fetch images
config = Configuration()
config.fetch_images = False

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def scrape_source(source):
	try:
		news_source = newspaper.build(source['url'],config=config)
		store_articles(source,news_source)
	except Exception as e:
		slog.write('\n'+ datetime.now().isoformat() +'\t'  +str(e))

def store_articles(source, news_source):
	client = MongoClient('mongodb://naberfeed.com:27017')
	db = client.naberfeed
	article2 = None
	docs = []
	for i in range(0,news_source.size()):
		placeholder = copy.deepcopy(article_template)
		article = news_source.articles[i]
		try:
			article.build()
			if not (urlparse(article.url).netloc == urlparse(source['url']).netloc):
				break
			if urlparse(article.url).netloc in blocklisted:
				break
			if not article2 == None and similar(article2.summary,article.summary) > 0.8:
				del docs[-1]
				break
			if article.text != '':
				placeholder['text'] = article.text
				placeholder['keywords'] = article.keywords
				if article.publish_date:
					placeholder['datePublished'] = article.publish_date
				else:
					placeholder['datePublished'] = datetime.now()
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
				article2 = article
		except Exception as e:
			alog.write('\n'+ datetime.now().isoformat() +'\t'+str(e))
	if len(docs) > 0:
		db.articles.insert_many(docs)

if __name__ == '__main__':
	client = MongoClient('mongodb://naberfeed.com:27017')
	db = client.naberfeed
	sources = list(db.sources.find({'flagged':0}))
	# for source in sources:
	# 	scrape_source(source)
	Parallel(n_jobs=-1)(delayed(scrape_source)(source) for source in sources)
	print('Done scraping')
