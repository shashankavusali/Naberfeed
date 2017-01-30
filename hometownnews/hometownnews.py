# hometownnews.py
import urllib2
import csv
from bs4 import BeautifulSoup

hometownnews = "http://www.hometownnews.com/"
page = urllib2.urlopen(hometownnews)
soup = BeautifulSoup(page, "html.parser")
dropdown = soup.find('select')

state_acronyms = ["AL","AK","AZ","AR","CA","CO","CT",
	"DE","DC","FL","GA","HI","ID","IL","IN","IA",
	"KS","KY","LA","ME","MD","MA","MI","MN","MS",
	"MO","MT","NE","NV","NH","NJ","NM","NY","NC",
	"ND","OH","OK","OR","PA","RI","SC","SD","TN",
	"TX","UT","VT","VA","WA","WV","WI","WY"]

states_full = [
"Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
"Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois",
"Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
"Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
"Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
"North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
"Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
"Vermont","Virgina","Washington","West Virginia","Wisconsin","Wyoming"
]

state = []
name = []
URL  = []

for tag in dropdown.find_all('option', selected=False):
		statepage = urllib2.urlopen(tag['value'])
		statesoup = BeautifulSoup(statepage, "html.parser")

		header = statesoup.find('h3')
		aState = header.next
		current_state = state_acronyms[states_full.index(str(aState).strip())]

		table = statesoup.find('table')

		for cell in table.find_all('td'):
			# print(cell['data-link'])
			# print(cell.get_text().strip())
			newsPage = urllib2.urlopen(cell['data-link'])
			if newsPage.geturl() != "http://www.hometownnews.com/home/default":
				state.append(current_state)
				name.append(cell.get_text().strip())
				newsSoup = BeautifulSoup(newsPage, "html.parser")
				link = newsSoup.find('a', target='_blank')
				URL.append(link['href'])
				# print(link['href'])
				# print("\n")

################################################
#BY STATE FILE
################################################
			# with open ('./by_state/' + current_state + '.csv','w') as csvfile:
			# # with open(current_state + '.csv','w') as csvfile:
			# 	writer_0 = csv.writer(csvfile,delimiter=',')
			# 	for i in range(len(name)):
			# 		writer_0.writerow([current_state,name[i],URL[i]])

################################################
#SINGLE FILE 'allstates.csv'
################################################
with open('all.csv','w') as csvfile:
	writer_0 = csv.writer(csvfile,delimiter=',')
	for i in range(len(name)):
		writer_0.writerow([state[i],name[i],URL[i]])
