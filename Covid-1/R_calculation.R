library(tidyverse)


R_calculation <- function (infectious_period, incubation_period, date, scenario_in, school_in,quarantine_length,testing_rate,fn_rate){
  #define a list of all states (and DC) in alphabetical order
  states <- c('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming')
  #define a list of the populations of all states and DC in alphabetical order (https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population, accessed on July 21, 2020)
  pops <- c(4903185, 731545, 7278717, 3017825, 39512223, 5758736, 3565287, 973764, 705749, 21477737, 10617423, 1415872, 1787065, 12671821, 6732219, 3155070, 2913314, 4467673, 4648794, 1344212, 6045680, 6949503, 9986857, 5639632, 2976149, 6137428, 1068778, 1934408, 3080156, 1359711, 8882190, 2096829, 19453561, 10488084, 762062, 11689100, 3956971, 4217737, 12801989, 1059361, 5148714, 884659, 6833174, 28995881, 3205958, 623989, 8535519, 7614893, 1792147, 5822434,578759)
  #fips code (necessary for R mapping function) for all states and DC in alphabetical order
  fips <- c(1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56)
  
  #parameters that are read in from the Rshiny app
  infection_length <- infectious_period                           #length of time that a person is infectious after developing a COVID-19 infection (time to recovery)
  incubation_length <- incubation_period                           #length of time between when a person is exposed to the virus and when they develop a COVID-19 infection (incubation period)
  target_date <- as.Date(date)                                        #date students return to campus (assume a single date, although we realize students will come back over a period of 1-2 weeks)
  scenario=scenario_in                                           #choice of IHME model (potentially other models?) to use for predicting COVID-19 infection rates in the future
  school = school_in    #University or College of interest
  quarantine <- quarantine_length                                       #length of time students are required to stay in their room prior to testing
  testing <- testing_rate                                           #percentage of students that will be tested following the quarantine period
  false_negative_rate <- fn_rate                                       #presumed false-negative rate associated with testing
  
  get_matching <- function (start_point,end_point,dater,locationer,meaner,upperer,lowerer,stater, infection_lengther,popser,attendancer) {
    xmatching_dates_table <- subset(readCSV, date > start_point & date <= end_point)  
    xmatching_locations <- xmatching_dates_table$location_name
    xmatching_dates <- xmatching_dates_table$date
    xmatching_means <- xmatching_dates_table$deaths_mean_smoothed
    xmatching_lowers <- xmatching_dates_table$deaths_lower_smoothed
    xmatching_uppers <- xmatching_dates_table$deaths_upper_smoothed
    xmean_by_state <- vector(length=51)
    xupper_by_state <- vector(length=51)
    xlower_by_state <- vector(length=51)
    for (i in 1:length(stater)){
      state_vs <- subset(xmatching_dates_table,location_name == stater[i])
      xmean_by_state[i] <- sum(state_vs$deaths_mean_smoothed)/popser[i]
      xupper_by_state[i] <- sum(state_vs$deaths_upper_smoothed)/popser[i]
      xlower_by_state[i] <- sum(state_vs$deaths_lower_smoothed)/popser[i]
    }
    
    xlower_prob_no_infection = 1
    xlower_number_infected = 0
    for (i in 1:length(attendancer)){
      xlower_prob_no_infection = xlower_prob_no_infection*((1-xlower_by_state[i])^attendance[i])
      xlower_number_infected = xlower_number_infected + xlower_by_state[i]*attendance[i]
    }
    xlower_prob_infection = 1 - xlower_prob_no_infection
    
    xmean_prob_no_infection = 1
    xmean_number_infected = 0
    for (i in 1:length(attendancer)){
      xmean_prob_no_infection = xmean_prob_no_infection*((1-xmean_by_state[i])^attendance[i])
      xmean_number_infected = xmean_number_infected + xmean_by_state[i]*attendance[i]
    }
    xmean_prob_infection = 1 - xmean_prob_no_infection
    
    xupper_prob_no_infection = 1
    xupper_number_infected = 0
    for (i in 1:length(attendancer)){
      xupper_prob_no_infection = xupper_prob_no_infection*((1-xupper_by_state[i])^attendance[i])
      xupper_number_infected = xupper_number_infected + xupper_by_state[i]*attendance[i]
    }
    xupper_prob_infection = 1 - xupper_prob_no_infection
    
    output_list <- list(xmean_by_state,xlower_number_infected, xlower_prob_infection, xmean_number_infected, xmean_prob_infection, xupper_number_infected, xupper_prob_infection)
    return(output_list)
  }
  
  
  #choose the IHME model based on user input and read in IHME predictions
  if (scenario == 'best'){  #Universal Masks Model
    readCSV <- read.csv('best_US.csv',header=TRUE)    #read in predictions
  } else if (scenario == 'reference'){  #Universal Masks Model
    readCSV <- read.csv('reference_US.csv',header=TRUE)    #read in predictions
  } else if (scenario == 'worst'){  #Universal Masks Model
    readCSV <- read.csv('worst_US.csv',header=TRUE)    #read in predictions
  }
  
  location <- readCSV$location_name
  date <- as.Date(readCSV$date)
  mean <- readCSV$deaths_mean_smoothed
  lower <- readCSV$deaths_lower_smoothed
  upper <- readCSV$deaths_upper_smoothed
  
  schoolCSV <- read.csv('totals_by_state_per_school.csv',header = TRUE)
  attendance <- schoolCSV[,school]
  
  end_date = target_date
  first_date = end_date - infection_length
  outs_infection <- get_matching(first_date,end_date,date,location,mean,upper,lower,states,infection_length,pops,attendance)
  
  ifirst_date = target_date
  iend_date = ifirst_date + incubation_length
  outs_incubation <- get_matching(ifirst_date,iend_date,date,location,mean,upper,lower,states,infection_length,pops,attendance)
  
  outs_total <- get_matching(first_date,iend_date,date,location,mean,upper,lower,states,infection_length,pops,attendance)
  
  threshold_states <- c()
  case_counts <- c()
  totmean_number_cases <- c()
  for (i in 1:length(states)){
    student_cases = round((outs_incubation[[1]][i]+outs_infection[[1]][i])*attendance[i])
    totmean_number_cases <- c(totmean_number_cases,student_cases)
    if (student_cases>1){
      threshold_states <- c(threshold_states,states[i])
      case_counts <- c(case_counts,as.integer(student_cases))}
  }

  map_table<-tibble(fips,states,totmean_number_cases)
  table_table<-tibble(threshold_states,case_counts)
  
  if (quarantine < incubation_length){
    qend_date = end_date+quarantine
    qfirst_date = first_date+quarantine
    siend_date = iend_date
    sifirst_date = qend_date
    qouts_infection <- get_matching(qfirst_date,qend_date,date,location,mean,upper,lower,states,infection_length,pops,attendance)
    qlower_number_infected <- qouts_infection[[2]]
    qmean_number_infected <- qouts_infection[[4]]
    qupper_number_infected <- qouts_infection[[6]]
    miss_them_lower <- qlower_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
    miss_them_mean <- qmean_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
    miss_them_upper <- qupper_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
    qouts_incubation <- get_matching(sifirst_date,siend_date,date,location,mean,upper,lower,states,infection_length,pops,attendance)
    qlower_number_incubation <- qouts_incubation[[2]]
    qmean_number_incubation <- qouts_incubation[[4]]
    qupper_number_incubation <- qouts_incubation[[6]]
    miss_them_lower <- miss_them_lower + qlower_number_incubation
    miss_them_mean <- miss_them_mean + qmean_number_incubation
    miss_them_upper <- miss_them_upper + qupper_number_incubation
  } else if (quarantine < incubation_length+infection_length){
    qend_date = iend_date
    qfirst_date = first_date + quarantine
    qouts_infection <- get_matching(qfirst_date,qend_date,date,location,mean,upper,lower,states,infection_length,pops,attendance)
    qlower_number_infected <- qouts_infection[[2]]
    qmean_number_infected <- qouts_infection[[4]]
    qupper_number_infected <- qouts_infection[[6]]
    miss_them_lower <- qlower_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
    miss_them_mean <- qmean_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
    miss_them_upper <- qupper_number_infected*(1-(1-0.01*false_negative_rate)*0.01*testing)
  } else{
    miss_them_mean = 0
    miss_them_lower <- 0
    miss_them_upper <- 0
  }
  
  function_list <- list(outs_infection,outs_incubation,outs_total,miss_them_lower,miss_them_mean,miss_them_upper,threshold_states,case_counts,map_table,table_table)
  
  return(function_list)
}