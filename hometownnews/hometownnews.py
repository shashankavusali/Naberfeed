import urllib2
import csv
from bs4 import BeautifulSoup

# hometownnews = "http://www.hometownnews.com/"
hometownnews = 'http://www.hometownnews.com/paper/show/B61FCB60A3774105'
page = urllib2.urlopen(hometownnews)

print(page.geturl())
soup = BeautifulSoup(page, "html.parser")

dropdown = soup.find('select')

# f = open('myfile.txt','w')

name = []
URL  = []

for tag in dropdown.find_all('option', selected=False):
	# print(tag['value'])
	# print(tag.get_text())
	statepage = urllib2.urlopen(tag['value'])
	statesoup = BeautifulSoup(statepage, "html.parser")

	header = statesoup.find('h3')
	current_state = header.next

	table = statesoup.find('table')

	for cell in table.find_all('td'):
		print(cell['data-link'])
		print(cell.get_text().strip())
		name.append(cell.get_text().strip())
		URL.append(cell['data-link'])

		with open(current_state + '.csv','w') as csvfile:
			writer_0 = csv.writer(csvfile,delimiter=',')
			for i in range(len(name)):
				writer_0.writerow([current_state,name[i],URL[i]])
		# f.write(cell['data-link'])
		# f.write(cell.get_text().strip())
		# f.write('\n')

# f.close()