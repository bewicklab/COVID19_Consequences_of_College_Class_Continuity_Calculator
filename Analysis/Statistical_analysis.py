# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#this code collects school data and does analysis
#this code calculates:
#a) the expected number of students returning from each state with an active infection
#b) the expected number of students returning from each state who are in the incubation phase of a COVID-19 infection
#c) the expected total number of students returning from each state carrying the COVID-19 virus
#d) the expected total number of returning students (from all states) with active, incubating and active+incubating COVID-19 infections
#e) the probability that at least one student returns carrying the COVID-19 virus
#f) the probability that at least one student carrying COVID-19 will not be detected based on the school's required quarantine, testing levels and assumed false-negative rate

import csv
import numpy
import re
import os


#define a list of all states (and DC) in alphabetical order
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
#define a list of the populations of all states and DC in alphabetical order (https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population, accessed on July 21, 2020)
pops = [4903185, 731545, 7278717, 3017825, 39512223, 5758736, 3565287, 973764, 705749, 21477737, 10617423, 1415872, 1787065, 12671821, 6732219, 3155070, 2913314, 4467673, 4648794, 1344212, 6045680, 6949503, 9986857, 5639632, 2976149, 6137428, 1068778, 1934408, 3080156, 1359711, 8882190, 2096829, 19453561, 10488084, 762062, 11689100, 3956971, 4217737, 12801989, 1059361, 5148714, 884659, 6833174, 28995881, 3205958, 623989, 8535519, 7614893, 1792147, 5822434,578759]
#fips code (necessary for R mapping function) for all states and DC in alphabetical order
fips = [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]

tots=[]
with open('output_school_metadata.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',') 
    for row in readCSV:
        tots.append(row)


#parameters that are read in from the Rshiny app
infection_length = 10                            #length of time that a person is infectious after developing a COVID-19 infection (time to recovery)
incubation_length = 5                           #length of time between when a person is exposed to the virus and when they develop a COVID-19 infection (incubation period)
target_date=20200919                                        #date students return to campus (assume a single date, although we realize students will come back over a period of 1-2 weeks)
scenario='best'                                            #choice of IHME model (potentially other models?) to use for predicting COVID-19 infection rates in the future
#school = re.sub('\.',' ',re.sub('\"','ZZZZZ',re.sub('&','XXXXX',re.sub(' - ','YYYYY',school_in))))    #University or College of interest
quarantine=0                                        #length of time students are required to stay in their room prior to testing
testing = 100                                            #percentage of students that will be tested following the quarantine period
false_negative_rate = 10                                       #presumed false-negative rate associated with testing

#'get_matching' defines a function that calculates the probabilities and expected numbers of students from each state and across all states who will be COVID-19 carriers based on a set time period (infectious period, incubation period, infecitous period + incubation period)
def get_matching(start_point,end_point,dater,date_seter,locationer,meaner,upperer,lowerer,stater, infection_lengther,popser,attendancer):
    
    #find IHME predictions of new COVID-19 cases over the relevant time period (infectious period, incubation period or total infectious and incubation period)
    xmatching_dates_ind=[]  #find dates within the period if interest (infectious period, incubation period or total infectious and incubation period)
    for k in range(start_point,end_point):  #from the first date of interest to the last date of interest...
        xmatching_dates_ind=xmatching_dates_ind+[i for i, e in enumerate(dater) if e == date_seter[k]]  #find the indices in the relevant csv file for all of the IHME predictions for the date range of interest
        
    xmatching=[]                #this will store all output for the 'get_matching' function
    
    xmatching_locations=[]      #this stores the state for the IHME prediction
    xmatching_dates=[]          #this stores the date for the IHME prediction      
    xmatching_means=[]          #this stores the mean estimate for the number of new COVID-19 cases that the IHME model predicts for that state on that date
    xmatching_lowers=[]         #this stores the low estimate for the number of new COVID-19 cases that the IHME model predicts for that state on that date
    xmatching_uppers=[]         #this stores the high estimate for the number of new COVID-19 cases that the IHME model predicts for that state on that date
    
    for k in range(0,len(xmatching_dates_ind)):                             #for all dates within the period of interest...
        xmatching_locations.append(locationer[xmatching_dates_ind[k]])      #store the state
        xmatching_means.append(meaner[xmatching_dates_ind[k]])              #store the date
        xmatching_lowers.append(lowerer[xmatching_dates_ind[k]])            #store the mean number of infections in the state on that date
        xmatching_uppers.append(upperer[xmatching_dates_ind[k]])            #store the low number of infections in the state on that date
        xmatching_dates.append(dater[xmatching_dates_ind[k]])               #store the high number of infections in the state on that date
#    print(xmatching_dates)
    #find the total number of new COVID-19 cases in each state over the time period of interest
    xmean_by_state=[]                   #this stores the mean estimate for the total number of new COVID-19 cases that the IHME model predicts for each state over the whole period of interest
    xupper_by_state=[]                  #this stores the low estimate for the total number of new COVID-19 cases that the IHME model predicts for each state over the whole period of interest
    xlower_by_state=[]                  #this stores the high estimate for the total number of new COVID-19 cases that the IHME model predicts for each state over the whole period of interest
    for k in range(0,len(stater)):      #for each state...
        xmatching_states_ind=[i for i, e in enumerate(xmatching_locations) if e == stater[k]]   #find all of the stored (see above) IHME predictions from the focal state
        if len(xmatching_states_ind)<infection_lengther:                                        #if there are fewer stored IHME predictions than the length of the period of interest, print a warning
            print('warning dates missing'+states[k])
        xtotal_mean_infected_temp=0                             #initialize counters for mean, lower and upper estimates of total new infections over the whole period of interest
        xtotal_upper_infected_temp=0
        xtotal_lower_infected_temp=0
        for j in range(0,len(xmatching_states_ind)):            #for each IHME prediction for the focal state
            if xmatching_means[xmatching_states_ind[j]]!='':    #as long as there is a prediction...
                xtotal_mean_infected_temp=xtotal_mean_infected_temp+float(xmatching_means[xmatching_states_ind[j]])     #add the estimates for number of new infections for each day over the entire period of interest
                xtotal_upper_infected_temp=xtotal_upper_infected_temp+float(xmatching_uppers[xmatching_states_ind[j]])
                xtotal_lower_infected_temp=xtotal_lower_infected_temp+float(xmatching_lowers[xmatching_states_ind[j]])
        xmean_by_state.append(xtotal_mean_infected_temp/float(popser[k]))   #to calculate a probability of a person returning from a state with a COVID-19 infection, divide the total number of new infections over the period of interest by the total number of people in the state
        xupper_by_state.append(xtotal_upper_infected_temp/float(popser[k]))
        xlower_by_state.append(xtotal_lower_infected_temp/float(popser[k]))

    #calculate the (low IHME estimate for the) probability of at least one returning student harboring COVID-19, as well as the expected number of students returning with COVID-19
    xlower_prob_no_infection=1              #initialize the probability that there are no students returning with COVID-19
    xlower_number_infected=0                #initialize the expected number of students returning with COVID-19
    for k in range(0,len(attendancer)):     #for each state...
        xlower_prob_no_infection=xlower_prob_no_infection*((1-xlower_by_state[k])**round(float(attendancer[k])))    #multiple the probability of having no returning students with COVID-19 by (1-P)^n where P is the probability of being infected (or exposed, or both) in the state, and n is the number of students returning from the state
        xlower_number_infected=xlower_number_infected+xlower_by_state[k]*float(attendancer[k])                      #add P*n to the expected number of returning students with COVID-19, where P is the probability of being infected (or exposed, or both) in the state, and n is the number of students returning from the state
    xlower_prob_infection=1-xlower_prob_no_infection    #probaiblity of having at least one returning students infected is 1 - probability of having no returning students infected
    
    #repeat calculation for mean IHME estimate
    xmean_prob_no_infection=1
    xmean_number_infected=0
    for k in range(0,len(attendancer)):
        xmean_prob_no_infection=xmean_prob_no_infection*((1-xmean_by_state[k])**round(float(attendancer[k])))
        xmean_number_infected=xmean_number_infected+xmean_by_state[k]*float(attendancer[k])
    xmean_prob_infection=1-xmean_prob_no_infection
    
    #repeat calculation for high IHME estimate
    xupper_prob_no_infection=1
    xupper_number_infected=0
    for k in range(0,len(attendancer)):
        xupper_prob_no_infection=xupper_prob_no_infection*((1-xupper_by_state[k])**round(float(attendancer[k])))
        xupper_number_infected=xupper_number_infected+xupper_by_state[k]*float(attendancer[k])
    xupper_prob_infection=1-xupper_prob_no_infection



    #output all of the values of interest
    xmatching.append(xmean_by_state)            #mean number of students returning with COVID-19 from each state
    xmatching.append(xlower_number_infected)    #low IHME estimate for total number of students returning with COVID-19
    xmatching.append(xlower_prob_infection)     #low IHME estimate for probability of at least one student returning with COVID-19
    xmatching.append(xmean_number_infected)     #mean IHME estimate for total number of students returning with COVID-19
    xmatching.append(xmean_prob_infection)      #mean IHME estimate for probability of at least one student returning with COVID-19
    xmatching.append(xupper_number_infected)    #high IHME estimate for total number of students returning with COVID-19
    xmatching.append(xupper_prob_infection)     #high IHME estimate for probability of at least one student returning with COVID-19
    
    
    return xmatching

     
school_meanprob=[]
school_lowprob=[]
school_highprob=[]
school_meanactive=[]
school_lowactive=[]
school_highactive=[]
school_meanincub=[]
schoollowincub=[]
schoolhighincub=[]
school_meantot=[]
school_lowtot=[]
schoolhightot=[]
school_in=[]
school_out=[]
totsin=[]

for kjk in range(1,len(tots)):
    if tots[kjk][3] in states:
        totsin.append(tots[kjk])
        school = tots[kjk][0]
        #print(school)
        
        #read in the IHME model predictions
        location=[]     #stores the state for the prediction
        date=[]         #stores the date for the prediction
        mean=[]         #stores the mean estimate for the prediction
        lower=[]        #stores the low estimate for the prediction
        upper=[]        #stores the high estimate for the prediction
        
        #choose the IHME model based on user input and read in IHME predictions
        if scenario == 'best':  #Universal Masks Model
            with open('best_US.csv') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')    #read in predictions
                for row in readCSV:
                    if 'date' not in row:           #store the predictions (as long as it's not the header)
                        location.append(row[0])
                        date.append(int(row[1].split('-')[0]+row[1].split('-')[1]+row[1].split('-')[2]))    #store the date as a converted integer
                        mean.append(row[2])
                        lower.append(row[3])
                        upper.append(row[4])
        elif scenario == 'reference':   #Current Projection Model
            with open('reference_US.csv') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    if 'date' not in row:
                        location.append(row[0])
                        date.append(int(row[1].split('-')[0]+row[1].split('-')[1]+row[1].split('-')[2]))
                        mean.append(row[2])
                        lower.append(row[3])
                        upper.append(row[4])
        elif scenario == 'worst':   #Mandates Easing Model
            with open('worst_US.csv') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    if 'date' not in row:
                        location.append(row[0])
                        date.append(int(row[1].split('-')[0]+row[1].split('-')[1]+row[1].split('-')[2]))
                        mean.append(row[2])
                        lower.append(row[3])
                        upper.append(row[4])
        
        #choose the school of interest, and read in the breakdown of students by state
        school_data=[]    
        with open('totals_by_state_per_school.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')    #read in students by state
            for row in readCSV:
                school_data.append(row)
        find_school=school_data[0].index(school)            #find the index for the state of interest
        attendance=[]       #stores the number of students from each state
        for k in range(1,len(school_data)):
            attendance.append(school_data[k][find_school])
        
        #sort the dates of interest in increasing order (remember, date is stored as an integer... but conversion is 1:1, so increasing integer means later date)
        date_set=numpy.sort(list(set(date)))
        
        #Calculate the number arriving infectious
        end_date = [i for i, e in enumerate(date_set) if e == target_date]  #infectious students developed their infections either on the day of arrival... 
        first_date=end_date[0]-infection_length                             #...or else up to X days earlier, where X is the total length of the infectious period
        #call the get_matching function to find expected values and probabilities for the infectious period (from X days before day of arrival to day of arrival)
        matching_out=get_matching(first_date+1,end_date[0]+1,date,date_set,location,mean,upper,lower, states, infection_length,pops,attendance)
        mean_by_state=matching_out[0]
        lower_number_infected=matching_out[1]
        mean_number_infected=matching_out[3]
        upper_number_infected=matching_out[5]
            
        
        #Calculate the number arriving incubating the virus
        ifirst_date = [i for i, e in enumerate(date_set) if e == target_date]   #incubating students will develop an infection from the day after arrival 
        iend_date=ifirst_date[0]+incubation_length #...to Y days after arrival, where Y is the length of the incubation period (i.e., these students were exposed up to the day before they arrived, and developed the infection Y days later... so we are looking for infections that would have started in their home state from the day after arrival to Y days later)
        #call the 'get_matching' function to find the expected values and probabilities for the incubation period (from the day after arrival to Y days after arrival)
        imatching_out=get_matching(ifirst_date[0]+1,iend_date+1,date,date_set,location,mean,upper,lower,states,incubation_length,pops,attendance)
        imean_by_state=imatching_out[0]
        ilower_number_infected=imatching_out[1]
        imean_number_infected=imatching_out[3]
        iupper_number_infected=imatching_out[5]
           
        
        
        #Calculate the total number arriving with the virus
        tfirst_date = [i for i, e in enumerate(date_set) if e == target_date]   #students arriving with the virus could be infectious or incubating... they were exposed up to X days before arrival, and may develop the infection up to Y days after arrival
        fend_date=tfirst_date[0]+incubation_length
        tend_date = [i for i, e in enumerate(date_set) if e == target_date]
        ffirst_date=tend_date[0]-infection_length
        #call the 'get_matching' function to find the expected values and probabilities for the total incubation period + infecitous period (from X days before arrival to Y days after arrival)
        ttmatching_out=get_matching(ffirst_date+1,fend_date+1,date,date_set,location,mean,upper,lower,states,infection_length+incubation_length,pops,attendance)
        ttlower_prob_infection=ttmatching_out[2]
        ttmean_prob_infection=ttmatching_out[4]
        ttupper_prob_infection=ttmatching_out[6]
        
        
        totmean_number_cases=[]
        threshold_states=[]
        case_counts=[]
        for k in range(0,len(attendance)):
            totmean_number_cases.append(str(fips[k])+','+states[k]+','+str((imean_by_state[k]+mean_by_state[k])*float(attendance[k]))+'\n')
            student_cases=numpy.round((imean_by_state[k]+mean_by_state[k])*float(attendance[k]),0)        
            if student_cases>1:
                threshold_states.append(states[k]+','+str(int(student_cases))+'\n')
                case_counts.append(int(student_cases))
           
        instate=0
        outstate=0
        sind=states.index(tots[kjk][3])
        for ss in range(0,len(mean_by_state)):
            if ss == sind:
                instate=instate+(imean_by_state[ss]+mean_by_state[ss])*float(attendance[ss])
            else:
                outstate=outstate+(imean_by_state[ss]+mean_by_state[ss])*float(attendance[ss])

        #Calculate the total number missing detection
        if quarantine < incubation_length:
            qend_date = end_date[0]+quarantine
            qfirst_date=first_date+quarantine
            siend_date = iend_date
            sifirst_date = qend_date
            qmatching_out=get_matching(qfirst_date+1,qend_date+1,date,date_set,location,mean,upper,lower, states, infection_length,pops,attendance)
            qlower_number_infected=qmatching_out[1]
            qmean_number_infected=qmatching_out[3]
            qupper_number_infected=qmatching_out[5]
            miss_them_lower = qlower_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
            miss_them_mean = qmean_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
            miss_them_upper = qupper_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
            simatching_out=get_matching(sifirst_date+1,siend_date+1,date,date_set,location,mean,upper,lower, states, siend_date-sifirst_date,pops,attendance)
            silower_number_infected=simatching_out[1]
            simean_number_infected=simatching_out[3]
            siupper_number_infected=simatching_out[5]
            miss_them_lower = miss_them_lower+silower_number_infected
            miss_them_mean = miss_them_mean+simean_number_infected
            miss_them_upper = miss_them_upper+siupper_number_infected
        elif quarantine < incubation_length+infection_length:
            qend_date = iend_date
            qfirst_date = first_date+quarantine
            qmatching_out=get_matching(qfirst_date+1,qend_date+1,date,date_set,location,mean,upper,lower, states, qend_date-qfirst_date,pops,attendance)
            qlower_number_infected=qmatching_out[1]
            qmean_number_infected=qmatching_out[3]
            qupper_number_infected=qmatching_out[5]
            miss_them_lower = qlower_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
            miss_them_mean = qmean_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
            miss_them_upper = qupper_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
        else:
            miss_them_mean = 0
            miss_them_lower = 0
            miss_them_upper = 0
        
        
        school_meanprob.append(numpy.round(100*(ttmean_prob_infection),2))
        school_lowprob.append(numpy.round(100*(ttlower_prob_infection),2))
        school_highprob.append(numpy.round(100*(ttupper_prob_infection),2))
        school_meanactive.append(int(numpy.round(mean_number_infected,0)))
        school_lowactive.append(int(numpy.round(lower_number_infected,0)))
        school_highactive.append(int(numpy.round(upper_number_infected,0)))
        school_meanincub.append(int(numpy.round(imean_number_infected,0)))
        schoollowincub.append(int(numpy.round(ilower_number_infected,0)))
        schoolhighincub.append(int(numpy.round(iupper_number_infected,0)))
        school_meantot.append(int(numpy.round(imean_number_infected,0))+int(numpy.round(mean_number_infected,0)))
        school_lowtot.append(int(numpy.round(ilower_number_infected,0))+int(numpy.round(lower_number_infected,0)))
        schoolhightot.append(int(numpy.round(iupper_number_infected,0))+int(numpy.round(upper_number_infected,0)))   
        school_in.append(instate)
        school_out.append(outstate)
    #    probability= 'There is a '+str(percent_probability)+'% chance that at least one student will bring COVID-19 to campus (range: '+str(lower_percent_probability)+'% - '+str(upper_percent_probability)+'%)<br/><br/>'
    #    active='.....  '+str(int(numpy.round(mean_number_infected,0)))+' of these students will have active COVID-19 infections (range: '+str(int(numpy.round(lower_number_infected,0)))+' - '+str(int(numpy.round(upper_number_infected,0)))+')<br/>'
    #    incubating='.....  '+str(int(numpy.round(imean_number_infected,0)))+' of these students will still be in the incubation phase (range: '+str(int(numpy.round(ilower_number_infected,0)))+' - '+str(int(numpy.round(iupper_number_infected,0)))+')<br/><br/>'
    #    totals=str(int(numpy.round(mean_number_infected+imean_number_infected,0)))+' students are predicted to arrive on campus carrying the COVID-19 virus (range: '+str(int(numpy.round(lower_number_infected+ilower_number_infected,0)))+' - '+str(int(numpy.round(upper_number_infected+iupper_number_infected,0)))+')<br/>'
    #    missers = 'The proposed testing strategy is expected to miss '+str(int(numpy.round(miss_them_mean)))+' students carrying the COVID-19 virus (range: '+str(int(numpy.round(miss_them_lower)))+' - '+str(int(numpy.round(miss_them_upper)))+')<br/><br/>'
    #    outputing=probability+totals+active+incubating+missers
   
liner=['school,real_size,size,state,setting,status,meanprob,lowprob,highprob,meanactive,lowactive,highactive,meanincub,lowincub,highincub,meantot,lowtot,hightot,instate,outstate\n']
for k in range(0,len(school_out)):
    liner.append(totsin[k][0]+','+totsin[k][1]+','+totsin[k][2]+','+totsin[k][3]+','+totsin[k][4]+','+totsin[k][5]+','+str(school_meanprob[k])+','+str(school_lowprob[k])+','+str(school_highprob[k])+','+str(school_meanactive[k])+','+str(school_lowactive[k])+','+str(school_highactive[k])+','+str(school_meanincub[k])+','+str(schoollowincub[k])+','+str(schoolhighincub[k])+','+str(school_meantot[k])+','+str(school_lowtot[k])+','+str(schoolhightot[k])+','+str(school_in[k])+','+str(school_out[k])+'\n')

j = open("output_school_data_for_analysis.csv","w")
for u in range(0,len(liner)):
    j.write(re.sub('na','NA',liner[u]))
j.close()

    