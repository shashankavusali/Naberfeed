import os
import json
from pprint import pprint
import newspaper
from newspaper import NewsPool, Config



with open('output.json') as file:
	data = json.load(file)
# pprint(data)

# mo_papers = data["MO"]
# como_papers = mo_papers["Buffalo"]
config = Config()
config.memorize_articles = False

for state_name, cities in data.items():
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

		news_pool = NewsPool(config)
		news_pool.set(sources, threads_per_source = 2)
		news_pool.join()
		for i in range(0,len(papers)):
			for directory_name,paper_links in papers[i].items():
				directory_name = 'news/'+state_name+'/'+directory_name
				if not os.path.exists(directory_name):
					os.makedirs(directory_name)
				source = sources[i]
				for i in range(0,source.size()):
					article = source.articles[i]
					article.parse()
					with open(directory_name+'/article_'+str(i)+'.txt','w') as f:
						f.write(article.text)
print('Hello')
