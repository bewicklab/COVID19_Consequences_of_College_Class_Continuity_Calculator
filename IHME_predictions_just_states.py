# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 00:54:49 2020

@author: sharon
"""

import csv

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia','Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

best=[]
with open('Best_mask_hospitalization_all_locs.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        best.append(row)

reference=[]
with open('Reference_hospitalization_all_locs.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        reference.append(row)

worst=[]
with open('Worse_hospitalization_all_locs.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        worst.append(row)


date_ind_best=best[0].index('date')
date_ind_reference=reference[0].index('date')
date_ind_worst=worst[0].index('date')

location_name_ind_best=best[0].index('location_name')
location_name_ind_reference=reference[0].index('location_name')
location_name_ind_worst=worst[0].index('location_name')

location_id_ind_best=best[0].index('location_id')
location_id_ind_reference=reference[0].index('location_id')
location_id_ind_worst=worst[0].index('location_id')

inf_mean_ind_best=best[0].index('est_infections_mean')
inf_mean_ind_reference=reference[0].index('est_infections_mean')
inf_mean_ind_worst=worst[0].index('est_infections_mean')

inf_lower_ind_best=best[0].index('est_infections_lower')
inf_lower_ind_reference=reference[0].index('est_infections_lower')
inf_lower_ind_worst=worst[0].index('est_infections_lower')

inf_upper_ind_best=best[0].index('est_infections_upper')
inf_upper_ind_reference=reference[0].index('est_infections_upper')
inf_upper_ind_worst=worst[0].index('est_infections_upper')

best_US=[]
best_US.append(best[0][location_name_ind_best]+','+best[0][date_ind_best]+','+best[0][inf_mean_ind_best]+','+best[0][inf_lower_ind_best]+','+best[0][inf_upper_ind_best]+'\n')
for k in range(1,len(best)):
    if best[k][location_name_ind_best] in states:
        if best[k][location_name_ind_best]=='Georgia':
            if best[k][location_id_ind_best]=='533':
                best_US.append(best[k][location_name_ind_best]+','+best[k][date_ind_best]+','+best[k][inf_mean_ind_best]+','+best[k][inf_lower_ind_best]+','+best[k][inf_upper_ind_best]+'\n')
        else:
            best_US.append(best[k][location_name_ind_best]+','+best[k][date_ind_best]+','+best[k][inf_mean_ind_best]+','+best[k][inf_lower_ind_best]+','+best[k][inf_upper_ind_best]+'\n')

reference_US=[]
reference_US.append(reference[0][location_name_ind_reference]+','+reference[0][date_ind_reference]+','+reference[0][inf_mean_ind_reference]+','+reference[0][inf_lower_ind_reference]+','+reference[0][inf_upper_ind_reference]+'\n')
for k in range(1,len(reference)):
    if reference[k][location_name_ind_reference] in states:
        if reference[k][location_name_ind_reference]=='Georgia':
            if reference[k][location_id_ind_reference]=='533':
                reference_US.append(reference[k][location_name_ind_reference]+','+reference[k][date_ind_reference]+','+reference[k][inf_mean_ind_reference]+','+reference[k][inf_lower_ind_reference]+','+reference[k][inf_upper_ind_reference]+'\n')
        else:
            reference_US.append(reference[k][location_name_ind_reference]+','+reference[k][date_ind_reference]+','+reference[k][inf_mean_ind_reference]+','+reference[k][inf_lower_ind_reference]+','+reference[k][inf_upper_ind_reference]+'\n')
            

    
worst_US=[]
worst_US.append(worst[0][location_name_ind_worst]+','+worst[0][date_ind_worst]+','+worst[0][inf_mean_ind_worst]+','+worst[0][inf_lower_ind_worst]+','+worst[0][inf_upper_ind_worst]+'\n')
for k in range(1,len(worst)):
    if worst[k][location_name_ind_worst] in states:
        if worst[k][location_name_ind_worst]=='Georgia':
            if worst[k][location_id_ind_worst]=='533':
                worst_US.append(worst[k][location_name_ind_worst]+','+worst[k][date_ind_worst]+','+worst[k][inf_mean_ind_worst]+','+worst[k][inf_lower_ind_worst]+','+worst[k][inf_upper_ind_worst]+'\n')
        else:
            worst_US.append(worst[k][location_name_ind_worst]+','+worst[k][date_ind_worst]+','+worst[k][inf_mean_ind_worst]+','+worst[k][inf_lower_ind_worst]+','+worst[k][inf_upper_ind_worst]+'\n')


j = open("best_US.csv","w")
for u in range(0,len(best_US)):
    j.write(best_US[u])
j.close()

j = open("reference_US.csv","w")
for u in range(0,len(reference_US)):
    j.write(reference_US[u])
j.close()

j = open("worst_US.csv","w")
for u in range(0,len(worst_US)):
    j.write(worst_US[u])
j.close()