import urllib2
from bs4 import BeautifulSoup

hometownnews = "http://www.hometownnews.com/home/state/al"

page = urllib2.urlopen(hometownnews)

soup = BeautifulSoup(page)

table = soup.find('table')

for cell in table.find_all('td'):
	print(cell['data-link'])	
	print(cell.get_text().strip())