'''paperboy.py'''
'''
Scraper for www.paperboy.com site. Timeouts occur frequently, so the script
executes by requesting user input on which states to scrape. The scraping is
sequential starting with 'first state to scrape' and ending with 'last state
to scrape.' For each state a file 'xx.csv' is created, where xx is the acronym
for a given state.
'''
#LIBRARIES
from bs4 import BeautifulSoup
import csv
import requests
import time
import os.path


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

#INPUT STATES TO SCRAPE TO RETRY FOR TIMEOUTS
print(state_acron)
user_input  = input("Enter acronym of first state to scrape: ")
user_input2 = input("Enter acronym of last state to scrape: ")
index       = state_acron.index(user_input)
index_last  = state_acron.index(user_input2)

#ITERATE OVER LIST OF STATES
for j in range(index,index_last+1):
	print(state_name[j])
	news_names  = []
	news_acron  = []
	news_urls   = []
	news_cities = []
	#RETRIEVE LIST OF NPs IN STATE
	state_url  = state_links[j]
	state_page = requests.get(root_url + state_url)
	state_soup = BeautifulSoup(state_page.content,'lxml')
	strong = state_soup.select('strong')[3:-1]
	#ITERATE OVER NP LINKS AND APPEND NP URLS TO ARRAYS
	for i in strong:
		news_names.append(i.next) #name of newspaper
		news_acron.append(state_acron[j]) #attach state acronym
		link      = requests.get(root_url + i.previous['href'])
		link_soup = BeautifulSoup(link.content,'lxml')
		news_urls.append(link_soup.h1.a['href']) #actual URL
		news_cities.append(
			i.find_parent('tr').select('td')[1].get_text().strip()) #city
		print([state_acron[j],i.next])
	with open('./by_state/' + state_acron[j]+ '.csv','w') as csvfile:
		writer1 = csv.writer(csvfile,delimiter=',')
		for k in range(len(news_urls)):
			writer1.writerow(
				[news_acron[k],news_cities[k],news_names[k],news_urls[k]])
