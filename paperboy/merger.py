'''merger.py'''
'''
This file merges all .csv files in the 'by_state' folder, which correspond to
the list of newspapers for each state. The output file is 'all.csv' and can be
found in the root folder.
'''
import csv
from os import listdir
import os.path

files = listdir('./by_state/')

for i in range(len(files)):
    if i==0:
        fout=open('all.csv','w')
        for line in open('./by_state/' + files[i],'r'):
            fout.write(line)
    else:
        fout=open('all.csv','a')
        for line in open('./by_state/' + files[i],'r'):
            fout.write(line)
