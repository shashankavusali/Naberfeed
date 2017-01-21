from bs4 import BeautifulSoup
import urllib.request
import re

baseurl ='http://www.50states.com'
page = urllib.request.urlopen(baseurl+'/news')

# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>

# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>

# <p class="story">...</p>
# """

soup = BeautifulSoup(page,'html.parser')
# print(soup.prettify())

for ul in soup.find_all('ul',class_='listStates'):
	for ul2 in ul.find_all('ul'):
		for atag in ul2.find_all('a'):
			print(baseurl+atag['href'])
			childpage = urllib.request.urlopen(baseurl+atag['href'])
			childsoup =  BeautifulSoup(childpage,'html.parser')
			print(childsoup.find_all('a'))