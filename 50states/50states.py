from bs4 import BeautifulSoup,element
import urllib.request
import re

baseurl ='http://www.50states.com'
page = urllib.request.urlopen(baseurl+'/news')

soup = BeautifulSoup(page,'lxml')
# print(soup.prettify())

file = open('50states_2.csv','w')

# for statelist in soup.find_all('ul',class_='listStates'):
# 	for column in statelist.find_all('ul'):
# 		for state in column.find_all('a'):
# 			state_name = state.get_text()
# 			print(state_name)
# 			childpage = urllib.request.urlopen(baseurl+state['href'])
# 			childsoup =  BeautifulSoup(childpage,'lxml')
# 			# print(childsoup.prettify())
# 			citylist = childsoup.find_all(re.compile("ul"),id='newsList')[0]
# 			for news_link in  citylist.select('li a'):
# 				try:
# 					url = news_link['href']
# 					name = news_link.get_text();
# 					city_name = news_link.next_sibling
# 					if city_name !=None and city_name != '' and not isinstance(city_name,element.Tag) :
# 						try:
# 							city_name = city_name.strip().replace('[','').replace(']','')
# 							file.write(state_name + ',' + url +',' + name + ','+ city_name + '\n')
# 						except Exception:
# 							print('exception occured for :' + url)
# 							continue
# 				except Exception:
# 					print(news_link)
#
# file.close()

def scrape_list(state_name,iterable):
	for news_link in iterable:
		try:
			url = news_link['href']
			name = news_link.get_text();
			city_name = news_link.next_sibling
			if city_name !=None and city_name !=' ' and not isinstance(city_name,element.Tag) :
				try:
					city_name = city_name.strip().replace('[','').replace(']','')
					file.write(state_acronyms[states_full.index(state_name)] +
						',' + url +',' + name + ','+ city_name + '\n')
				except Exception:
					print('exception occured for :' + url)
					continue
		except Exception:
			print(news_link)

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
"Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
]

for statelist in soup.find_all('ul',class_='listStates'):
	for column in statelist.find_all('ul'):
		for state in column.find_all('a'):
			state_name = state.get_text()
			print(state_name)
			childpage = urllib.request.urlopen(baseurl+state['href'])
			childsoup =  BeautifulSoup(childpage,'lxml')
			citylist = childsoup.find_all(re.compile("ul"),id='newsList')[0]
			if state_name=="California":
				scrape_list(state_name,citylist.select('li a')[2:-2])
				linkJR = citylist.select('li a')[0]
				linkSZ = citylist.select('li a')[1]
				page2  = urllib.request.urlopen(baseurl+'/news/'+linkJR['href'])
				page2soup = BeautifulSoup(page2,'lxml')
				citylist2 = page2soup.find_all(re.compile("ul"),id='newsList')[0]
				scrape_list(state_name,citylist2.select('li a')[2:-2])
				page3 = urllib.request.urlopen(baseurl+'/news/'+linkSZ['href'])
				page3soup = BeautifulSoup(page3,'lxml')
				citylist3 = page3soup.find_all(re.compile("ul"),id='newsList')[0]
				scrape_list(state_name,citylist3.select('li a')[2:-2])
			else:
				scrape_list(state_name,citylist.select('li a'))
file.close()
