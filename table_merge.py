'''table_merge.py'''
#LIBRARIES
import csv

#NEWSPAPERS CSV FILES
fiftystates_file  = '50states/50states_2.csv'
hometownnews_file = 'hometownnews/all_2.csv'
paperboy_file     = 'paperboy/all.csv'
usnpl_file        = 'usnpl/all.csv'

#ZIPS CSV FILE
zips_file         = 'clean-zips.csv'

#ALL FILES TOGETHER
files = [usnpl_file,paperboy_file,fiftystates_file]
# files = [usnpl_file]

state_acronyms = ["AL","AK","AZ","AR","CA","CO","CT",
	"DE","DC","FL","GA","HI","ID","IL","IN","IA",
	"KS","KY","LA","ME","MD","MA","MI","MN","MS",
	"MO","MT","NE","NV","NH","NJ","NM","NY","NC",
	"ND","OH","OK","OR","PA","RI","SC","SD","TN",
	"TX","UT","VT","VA","WA","WV","WI","WY"]
states_dict = {}
states_zips = {}
for i in state_acronyms:
    states_dict[i] = {}
    states_zips[i] = {}

output = open('output.json','w')
fziphandler   = open(zips_file,'r')

reader = csv.reader(fziphandler)
next(reader)
for row in reader:
	state_name  = row[3]
	city_name   = row[2]
	county_name = row[4]
	zip_nr      = row[0]
	population  = row[7]
	latitude    = row[5]
	longitude   = row[6]
	state = states_zips[state_name]
	if city_name in state:
		city = state[city_name]
	else:
		city = {}
		state[city_name] = city
	this_zip = {}
	this_zip['county_name'] = county_name
	this_zip['population'] = population
	this_zip['coords'] = (latitude,longitude)
	city[zip_nr] = this_zip

fziphandler.close();

for f in files:
    fhandler = open(f,'r')
    reader = csv.reader(fhandler)
    for row in reader:
        state_name = row[0].strip()
        city_name = row[1].strip()
        paper_name = row[2].strip()
        paper_url = row[3].strip()
        state = states_dict[state_name]
        zips_state = states_zips[state_name]
        if city_name in state:
            city = state[city_name]
        else:
            city = {}
            state[city_name] = city
            zips_city = zips_state[city_name]
            city['zips'] = zips_city
        if paper_name in city:
            paper = city[paper_name]
            paper.append(paper_url)
        else:
            city[paper_name] = [paper_url]

fhandler.close()
output.close()
print('End of program')
