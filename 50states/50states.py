from bs4 import BeautifulSoup,element
import urllib.request
import re


baseurl ='http://www.50states.com'
page = urllib.request.urlopen(baseurl+'/news')

soup = BeautifulSoup(page,'lxml')
# print(soup.prettify())

file = open('50states.csv','w')

for statelist in soup.find_all('ul',class_='listStates'):
	for column in statelist.find_all('ul'):
		for state in column.find_all('a'):
			state_name = state.get_text()
			print(state_name)
			childpage = urllib.request.urlopen(baseurl+state['href'])
			childsoup =  BeautifulSoup(childpage,'lxml')
			# print(childsoup.prettify())
			citylist = childsoup.find_all(re.compile("ul"),id='newsList')[0]
			for news_link in  citylist.select('li a'):
				try:
					url = news_link['href']
					city_name = news_link.next_sibling
					if city_name !=None and city_name != '' and not isinstance(city_name,element.Tag) :
						try:
							city_name = city_name.strip().replace('[','').replace(']','')
							file.write(state_name + ',' + url+','+city_name+'\n')
						except Exception:
							print('exception occured for :' + url)
							continue
				except Exception:
					print(news_link)

file.close()