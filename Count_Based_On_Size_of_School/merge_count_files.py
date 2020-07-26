# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 20:27:08 2020

@author: sharon
"""
#this code merges the diferent imported datasets so that there is a single dataset (multiple datasets may be generated to avoid the web scraper crashing partway through)
import csv

state1=[]
with open('university_x_state_totals1.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        state1.append(row)

state2=[]
with open('university_x_state_totals2.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        state2.append(row)

state3=[]
with open('university_x_state_totals3.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        state3.append(row)

state4=[]
with open('university_x_state_totals4.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        state4.append(row)

state5=[]
with open('university_x_state_totals5.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        state5.append(row)

output=[]

universities=''
for k in range(0,len(state1[0])):
    universities=universities+state1[0][k]+','
for k in range(1,len(state2[0])):
    universities=universities+state2[0][k]+','
for k in range(1,len(state3[0])):
    universities=universities+state3[0][k]+','
for k in range(1,len(state4[0])):
    universities=universities+state4[0][k]+','
for k in range(1,len(state5[0])):
    universities=universities+state5[0][k]+','
universities=universities+'\n'
output.append(universities)

for j in range(1,len(state1)):
    this_state=''
    for k in range(0,len(state1[j])):
        this_state=this_state+state1[j][k]+','
    for k in range(1,len(state2[j])):
        this_state=this_state+state2[j][k]+','
    for k in range(1,len(state3[j])):
        this_state=this_state+state3[j][k]+','
    for k in range(1,len(state4[j])):
        this_state=this_state+state4[j][k]+','
    for k in range(1,len(state5[j])):
        this_state=this_state+state5[j][k]+','
    this_state=this_state+'\n'
    output.append(this_state)

j = open("totals_by_state_per_school.csv","w")
for u in range(0,len(output)):
    j.write(output[u])
j.close()

    