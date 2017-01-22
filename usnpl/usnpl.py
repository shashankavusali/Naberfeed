'''usnpl.py'''

#Libraries
from bs4 import BeautifulSoup
import scrapy
import requests
from lxml import html
import csv
import time

#Load page
res = requests.get('http://www.usnpl.com')
homepage = res.content


# page = "../url_template/usnpl_mo.html"
soup_0 = BeautifulSoup(homepage,'lxml')

#return list of states
state_links = []
statesstr = str(soup_0.select('td'))
section_0 = BeautifulSoup(statesstr,'lxml')
for j in section_0.select('a'):
	state_links.append((j['href']))
	states.append((j.next))


for


# #Retrieve newspaper names, URLs, city synchronously 
# sectionstr = str(soup.select('div#data_box')[1])
# section = BeautifulSoup(sectionstr,'lxml')
# city = []
# name = []
# URL  = []
# for i in section.select('br')[9:len(section.select('br'))]:
# 	if i.find_next() != None:
# 		city.append(i.find_next().next)
# 		name.append(i.find_next().find_next().next)
# 		URL.append(i.find_next().find_next()['href'])

# current_state = 'mo'
# with open (current_state + '.csv','w') as csvfile:
# 	writer_0 = csv.writer(csvfile,delimiter=',')
# 	for i in range(len(city)):
# 		writer_0.writerow([current_state.upper(),city[i],name[i],URL[i]])

