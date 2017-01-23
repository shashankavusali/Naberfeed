'''paperboy.py'''

#LIBRARIES
from bs4 import BeautifulSoup
import csv
import requests
import time

#VARIABLES

state_acron = ["AL","AK","AZ","AR","CA","CO","CT",
	"DE","DC","FL","GA","HI","ID","IL","IN","IA",
	"KS","KY","LA","ME","MD","MA","MI","MN","MS",
	"MO","MT","NE","NV","NH","NJ","NM","NY","NC",
	"ND","OH","OK","OR","PA","RI","SC","SD","TN",
	"TX","UT","VT","VA","WA","WV","WI","WY"]
state_links = []
state_name  = []

#HOMEPAGE REQUEST
root_url      = 'http://www.thepaperboy.com'
start_url     = 'http://www.thepaperboy.com/usa-newspapers-by-state.cfm'
homepage      = requests.get(start_url)
homepage_soup = BeautifulSoup(homepage.content,'lxml')

#SCRAPE LIST OF STATE LINKS
a_tag_array = homepage_soup.select('.mediumlink')
for i in a_tag_array:
	state_links.append(i['href'])
	state_name.append(i.next.strip())

#ITERATE OVER LIST OF STATES
for j in range(len(state_links)):
	news_names  = []
	news_cities = []	
	news_urls   = []
	news_acron  = []
	#RETRIEVE LIST OF NPs IN STATE
	state_url  = state_links[j]
	state_page = requests.get(root_url + state_url)
	state_soup = BeautifulSoup(state_page.content,'lxml')
	strong = state_soup.select('strong')[3:-1]
	#ITERATE OVER NP LINKS AND RETRIEVE NP URLS
	for i in strong:
		link      = requests.get(root_url + i.previous['href'])
		link_soup = BeautifulSoup(link.content,'lxml')
		news_urls.append(link_soup.h1.a['href']) #actual URL
		news_names.append(i.next) #name of newspaper
		news_cities.append(
			i.find_parent('tr').select('td')[1].get_text().strip())
		news_acron.append(state_acron[j])
		print([state_acron[j],i.next])
	with open('./by_state/' + state_acron[j]+ '.csv','w') as csvfile:
		writer1 = csv.writer(csvfile,delimiter=',')
		for k in range(len(news_urls)):
			writer1.writerow(
				[news_acron[j],news_cities[k],news_names[k],news_urls[k]])


# #NON-ITERATIVE
# state_url  = state_links[30]
# state_page = requests.get(root_url + state_url)
# state_soup = BeautifulSoup(state_page.content,'lxml')
# strong = state_soup.select('strong')[3:-1]
# #ITERATE OVER NP LINKS AND RETRIEVE NP URLS
# for i in strong:
# 	link      = requests.get(root_url + i.previous['href'])
# 	link_soup = BeautifulSoup(link.content,'lxml')
# 	news_urls.append(link_soup.h1.a['href']) #actual URL
# 	news_names.append(i.next) #name of newspaper
# 	news_cities.append(
# 		i.find_parent('tr').select('td')[1].get_text().strip())
# 	news_acron.append(state_acron[30])
# 	print([state_acron[30],i.next])

# with open ('all.csv','w') as csvfile:
# 	writer0 = csv.writer(csvfile,delimiter=',')
# 	for i in range(len(news_urls)):
# 		writer0.writerow([news_acron[i],news_cities[i],news_names[i],news_urls[i]])

