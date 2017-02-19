import os
import json
from pprint import pprint
import newspaper
from newspaper import NewsPool, Config

# urls = ['http://www.mopress.com/','http://www.columbiatribune.com/','http://www.columbiamissourian.com/'];
sources = []

with open('output.json') as file:
	data = json.load(file)
# pprint(data)

mo_papers = data["MO"]
como_papers = mo_papers["Buffalo"]
papers = []
for key in filter(lambda a: not a == 'zips', como_papers.keys()):
	
	url = como_papers[key][0]
	try:
		source = newspaper.build(url)
		sources.append(source)
		papers.append({key:como_papers[key]})
	except Exception as e:
		print(str(e))
config = Config()
config.memorize_articles = False
news_pool = NewsPool(config)
news_pool.set(sources, threads_per_source = 3)

for i in range(0,len(papers)):
	for directory_name,paper_links in papers[i].items():
		directory_name = 'news/'+directory_name
		if not os.path.exists(directory_name):
			os.makedirs(directory_name)
		source = sources[i]
		for i in range(0,source.size()):
			article = source.articles[i]
			article.parse()
			f =  open(directory_name+'/article_'+str(i)+'.txt','w')
			f.write(article.text)
			f.close()
print('Hello')