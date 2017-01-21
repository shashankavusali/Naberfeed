'''usnpl.py'''
from bs4 import BeautifulSoup
import scrapy

# def state_scrapper():
# 	return 1

page = "../url_template/usnpl_al.html"
soup = BeautifulSoup(open(page),"lxml")
main = soup.select("div#data_box")
print(main[1])

# 1 --> Newspapers
# 2 --> Magazines
# 3 --> College