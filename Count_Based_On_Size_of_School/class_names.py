# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 05:30:02 2020

@author: sharon
"""

#this code scrapes data about the number of students from each state from a large list of universities
#this code uses the College Factual website (https://www.collegefactual.com/) as its source of data
#data is currently for 2017-2018
#this code only has to be run once (possibly in segments to prevent crashing); once the data has been recorded this will not change for at least one year
#This code was written in Python 2, and does not use bytes; conversion from bytes to strings will be required to run on Python 3

import requests
from bs4 import BeautifulSoup
import re
import numpy

#list of states
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia','Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

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
        name.append(str(keepme[k].split('\"')[5].encode('utf-8')))
        #store the school code
        code.append(str(keepme[k].split('\"')[9].encode('utf-8')))

#find the school-specific web-page with state-by-state breakdown of college composition
temp_state_data=[]
temp_state_data_code=[]
temp_state_data_name=[]
for k in range(0,len(code)):
    #locate the school specific web-page 
    page_diversity=requests.get("https://www.collegefactual.com/colleges/"+code[k]+"/student-life/diversity/chart-geographic-diversity.html")
    page_diversity
    #read in web-page
    soup_diversity = BeautifulSoup(page_diversity.content, 'html.parser')
    pretty_diversity=soup_diversity.prettify()
    #determine whether the flag for state-by-state breakdown of the student body exists, and if it does, pull out the line with this information
    if 'data.addColumn("number", "Undergraduates");' in soup_diversity.prettify().encode('utf-8'):
        if len(soup_diversity.prettify().encode('utf-8').split('data.addColumn("number", "Undergraduates");')[1].split('var formatter = new google.visualization.')[0].lstrip().rstrip())>0:
            print(k,name[k])
            #store the html line with the state-by-state breakdown
            temp_state_data.append(soup_diversity.prettify().encode('utf-8').split('data.addColumn("number", "Undergraduates");')[1].split('var formatter = new google.visualization.')[0].lstrip().rstrip())
            #store the school code
            temp_state_data_code.append(code[k])
            #store the school name
            temp_state_data_name.append(name[k])

#for each school with information available, first find the total number of students at the school
state_total=[]
state_data=[]
state_data_code=[]
state_data_name=[]
for k in range(0,len(temp_state_data)):
    #locate the school specific web-page with total enrollment
    page_number=requests.get("https://www.collegefactual.com/colleges/"+temp_state_data_code[k]+"/")
    page_number
    #read in web-page
    soup_number = BeautifulSoup(page_number.content, 'html.parser')
    pretty_number=soup_number.prettify().encode('utf-8')
    #determine whether the relevant information is on the web-site, and if it is, store the information
    if 'During the 2017' in pretty_number:
        #total number of students
        state_total.append(float(re.sub('full-time','',re.sub(',','',re.sub('full time','',pretty_number.split('During the 2017-2018 academic year, there were')[1].split('undergraduates at')[0].split('>')[1]).lstrip().rstrip()))))
        #html line holding state-by-state breakdown
        state_data.append(temp_state_data[k])
        #store the school code
        state_data_code.append(temp_state_data_code[k])
        #store the school name
        state_data_name.append(temp_state_data_name[k])

#for each school with information available, find the state-by-state breakdown
stater=[]
counter=[]
fraction=[]
totals=[]
#for each school in the list
for k in range(0,len(state_data)):
    #pull out each state name and associated number of students
    temp=state_data[k].split('data.addRow(')
    temp_stater=[]
    temp_counter=[]
    temp_fraction=[]
    temp_totals=[]
    for j in range(1,len(temp)):
        #store web-reported counts by state
        temp_counter.append(int(re.sub('\"','',temp[j].split('[')[1].split(',')[1]).split(']')[0]))
        #store state name
        state_name=re.sub('\"','',temp[j].split('[')[1].split(',')[0])
        temp_stater.append(state_name[1:len(state_name)-1])
    #find the total number of students at the school based on web-reported counts by state (these seem to differ from overall student body size, so we rescale)
    summer=numpy.sum(temp_counter)
    for j in range(0,len(temp_counter)):
        #find the fraction of students at the school from each state
        temp_fraction.append(float(temp_counter[j])/float(summer))
        #re-scale the fraction by the total size of the student body
        temp_totals.append(float(temp_counter[j])*state_total[k]/float(summer))
    #store state name
    stater.append(temp_stater)
    #store web reported state counts
    counter.append(temp_counter)
    #store fraction from each state
    fraction.append(temp_fraction)
    #store rescaled total number from each state
    totals.append(temp_totals)

#write out the information for each school and each state
schools=' '+','
for k in range(0,len(state_data_name)):
    schools=schools+state_data_name[k]+','
schools=schools+'\n'

counter_out=[]
fraction_out=[]
totals_out=[]
for k in range(0,len(states)):
    writeme_counter=states[k]+','
    writeme_fraction=states[k]+','
    writeme_totals=states[k]+','
    for j in range(0,len(stater)):
        if states[k] in stater[j]:
            ind=stater[j].index(states[k])
            writeme_counter=writeme_counter+str(counter[j][ind])+','
            writeme_fraction=writeme_fraction+str(fraction[j][ind])+','
            writeme_totals=writeme_totals+str(numpy.round(totals[j][ind]))+','
        else:
            writeme_counter=writeme_counter+str('0')+','
            writeme_fraction=writeme_fraction+str('0')+','
            writeme_totals=writeme_totals+str('0')+','
    counter_out.append(writeme_counter+'\n')
    fraction_out.append(writeme_fraction+'\n')
    totals_out.append(writeme_totals+'\n')

# j = open("name_of_file_totals.csv","w")
# j.write(schools)
# for u in range(0,len(totals_out)):
#     j.write(totals_out[u])
# j.close()

# j = open("name_of_file_counter.csv","w")
# j.write(schools)
# for u in range(0,len(totals_out)):
#     j.write(counter_out[u])
# j.close()

# j = open("name_of_file_fraction.csv","w")
# j.write(schools)
# for u in range(0,len(totals_out)):
#     j.write(fraction_out[u])
# j.close()