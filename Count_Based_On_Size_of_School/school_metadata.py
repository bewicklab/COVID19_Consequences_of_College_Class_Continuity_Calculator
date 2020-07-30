# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 05:30:02 2020

@author: sharon
"""

#this code scrapes data about the number of students from each state from a large list of universities
#this code uses the College Factual website (https://www.collegefactual.com/) as its source of data
#data is currently for 2017-2018
#this code only has to be run once (possibly in segments to prevent crashing); once the data has been recorded this will not change for at least one year

import requests
from bs4 import BeautifulSoup
import re
import numpy
import csv

#list of states
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia','Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

tots=[]
with open('totals_by_state_per_school.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',') 
    for row in readCSV:
        tots.append(row)

school_list=tots[0]
school_size_real=[0]

for k in range(1,len(school_list)):
    summer=0
    for j in range(1,len(tots)):
        summer=summer+int(float(tots[j][k]))
    school_size_real.append(summer)

#web-page that contains a list of all of the colleges with data on College Factual
page = requests.get("https://www.collegefactual.com/search/")
page
#read in web-page
soup = BeautifulSoup(page.content, 'html.parser')
#split web-page line-by-line
pretty=soup.prettify().split('\n')
keepme=[]
#retain any line with the name of a college
for k in range(0,len(pretty)):
    if 'collegeCanonHash' and 'name' and'slug' in pretty[k]:
        keepme.append(pretty[k])

#store the list of college/university names, along with their 'code number'; this information can be used to find the information page for each college/university
name=[]
code=[]
for k in range(0,len(keepme)):
    if len(keepme[k].split('\"'))>8:
        #store the school name
        ff=keepme[k].split('\"')[5].encode('utf-8')
        name.append(str(ff)[2:len(str(ff))-1])
        #store the school code
        gg=keepme[k].split('\"')[9].encode('utf-8')
        code.append(str(gg)[2:len(str(gg))-1])

#for each school with information available, first find the total number of students at the school
public_private=['na']
school_state=['na']
school_size=[0]
school_setting=['na']
for k in range(1,len(school_list)):
    ind=name.index(school_list[k])
    print(school_list[k])
    #locate the school specific web-page with total enrollment
    page_number=requests.get("https://www.collegefactual.com/colleges/"+code[ind]+"/")
    page_number
    #read in web-page
    soup_number = BeautifulSoup(page_number.content, 'html.parser')
    pretty_number=soup_number.prettify().encode('utf-8').decode()
    #determine whether the relevant information is on the web-site, and if it is, store the information
    if '/overview/location/' in pretty_number:
        temp1=pretty_number.split('/overview/location/')[1].split('State')[0]
        school_state.append(temp1.split('span')[1].split('\n')[1].lstrip().rstrip())
        temp2=pretty_number.split('/overview/location/')[2].split('State')[0]
        school_setting.append(temp2.split('span')[1].split('\n')[1].lstrip().rstrip())
        school_size.append(int(re.sub(',','',pretty_number.split('/overview/location/')[1].split('Full-Time')[0].split('span')[5].split('\n')[1].lstrip().rstrip())))
    else:
        school_state.append('na')     
        school_setting.append('na')
    if 'Located in' in pretty_number:
        temp3 = pretty_number.split('Located in')[1].split('.')[0]
        if 'private' in temp3 and 'public' not in temp3:
            public_private.append('private')
        elif 'private' not in temp3 and 'public' in temp3:
            public_private.append('public')
        else:
            public_private.append('na')
    else:
        public_private.append('na')

#write out the information for each school and each state
output=[]
for k in range(0,len(school_list)):
    output.append(school_list[k]+','+str(school_size_real[k])+','+str(school_size[k])+','+school_state[k]+','+school_setting[k]+','+public_private[k]+'\n')

j = open("output_school_metadata.csv","w")
for u in range(0,len(output)):
    j.write(output[u])
j.close()

