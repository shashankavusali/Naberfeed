'''
Replace states' full name for acronym in hometownnews.com 'all.csv' file:
'''
import csv
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
writer = csv.writer(open('all_2.csv','w'),delimiter=',')
for line in csv.reader(open('all.csv','r'),delimiter=','):
	state = state_acronyms[states_full.index(line[0].strip())]
	writer.writerow([state,line[1],line[2]])
