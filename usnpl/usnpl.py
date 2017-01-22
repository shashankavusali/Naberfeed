'''usnpl.py'''
#######################################
#Libraries
#######################################
from bs4 import BeautifulSoup
import requests
from lxml import html
import csv
import time

#######################################
#Load page
#######################################
res0     = requests.get('http://www.usnpl.com/aknews.php')
homepage = res0.content
soup0 = BeautifulSoup(homepage,'lxml')

#######################################
#Return list of states
#######################################
states      = []
state_links = []
statesstr0  = str(soup0.select('td'))
section0    = BeautifulSoup(statesstr0,'lxml')
for i in section0.select('a'):
	state_links.append((i['href']))
	states.append(i.next)


#######################################
#SINGLE FILE 'all.csv'
#######################################
state = []
city  = []
names = []
URL   = []
for k in range(len(state_links)-1):
	res1       = requests.get(state_links[k])
	soup       = BeautifulSoup(res1.content,'lxml')
	sectionstr = str(soup.select('div#data_box')[1])
	section    = BeautifulSoup(sectionstr,'lxml')
	for j in section.select('br')[9:len(section.select('br'))]:
		if j.find_next() != None:
			city.append(j.find_next().next)
			names.append(j.find_next().find_next().next)
			URL.append(j.find_next().find_next()['href'])
			state.append(states[k])
	print(state_links[k])
	time.sleep(5)
with open ('all.csv','w') as csvfile:
	writer_0 = csv.writer(csvfile,delimiter=',')
	for i in range(len(city)):
		writer_0.writerow([state[i].upper(),city[i],names[i],URL[i]])


#######################################
#SEPARATE FILES '/by_state/state.csv'
#######################################
# for k in range(len(state_links)-1):
# 	res1       = requests.get(state_links[k])
# 	soup       = BeautifulSoup(res1.content,'lxml')
# 	sectionstr = str(soup.select('div#data_box')[1])
# 	section    = BeautifulSoup(sectionstr,'lxml')
# 	city       = []
# 	name       = []
# 	URL        = []
# 	for j in section.select('br')[9:len(section.select('br'))]:
# 		if j.find_next() != None:
# 			city.append(j.find_next().next)
# 			name.append(j.find_next().find_next().next)
# 			URL.append(j.find_next().find_next()['href'])
# 			current_state = states[k]
# 			with open ('/by_state/' + current_state + '.csv','w') as csvfile:
# 				writer_0 = csv.writer(csvfile,delimiter=',')
# 				for i in range(len(city)):
# 					writer_0.writerow([current_state.upper(),city[i],name[i],URL[i]])
# 	print(state_links[k])
# 	time.sleep(5)


