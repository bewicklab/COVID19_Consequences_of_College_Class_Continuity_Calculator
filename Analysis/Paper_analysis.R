fips <- c(1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56)
states <- c('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming')

dataset <- read.csv('output_school_data_for_analysis_worst.csv',header=TRUE)
datasetchange <- read.csv('output_school_data_for_analysis_worstdelay.csv',header=TRUE)
mean(dataset$meantot)
median(dataset$meantot)
mean(dataset$meaNActive)
median(dataset$meaNActive)
mean(dataset$meanincub)
median(dataset$meanincub)
mean(dataset$meantot/dataset$real_size)
median(dataset$meantot/dataset$real_size)
mean(dataset$meaNActive/dataset$real_size)
median(dataset$meaNActive/dataset$real_size)
mean(dataset$meanincub/dataset$real_size)
median(dataset$meanincub/dataset$real_size)
mean(dataset$meanprob)
median(dataset$meanprob)
hist(log10(dataset$meantot),5)
hist(log10(dataset$meantot/dataset$real_size),10,xlim=c(-4.5,-1.5))
qplot(x=real_size, y=meantot, data = dataset1)+geom_smooth(method="lm")

dataset2 <- subset(dataset, select = c(meantot,real_size,status))

dataset1 <- na.omit(dataset2)

dataset3 <- subset(dataset, select = c(meantot,real_size,state))
dataset4 <- na.omit(dataset3)

howbad <- c()
for (i in 1:length(states)){
  datasettemp <- subset(dataset4,gsub('NA','na',state) == states[i])
  howbad <- c(howbad,mean(datasettemp$meantot))
  print(states[i])
  print(mean(datasettemp$meantot))
  
}

state_size <-tibble(fips,states,howbad)

plot_usmap(data = state_size, values = "howbad") +  scale_fill_gradient(low = "#FFFFFF",high ="#FF0000",  
                                                                                     guide = "colourbar") 
howbad2 <- c()
for (i in 1:length(states)){
  datasettemp <- subset(dataset4,gsub('NA','na',state) == states[i])
  howbad2 <- c(howbad2,mean(datasettemp$meantot/datasettemp$real_size))

}

state_size2 <-tibble(fips,states,howbad2)

plot_usmap(data = state_size2, values = "howbad2") +  scale_fill_gradient(low = "#FFFFFF",high ="#FF0000",  
                                                                        guide = "colourbar") 

dataset3change <- subset(datasetchange, select = c(meantot,real_size,state))
dataset4change <- na.omit(dataset3change)

ontime<-dataset4$meantot
delaytime <-dataset4change$meantot
percent_change <- 100*(delaytime-ontime)/ontime
dataset4$percent_change = percent_change

howbadchange <- c()
for (i in 1:length(states)){
  datasettemp <- subset(dataset4,gsub('NA','na',state) == states[i])
  datasettemp <- subset(datasettemp,is.finite(percent_change))
  howbadchange <- c(howbadchange,mean(datasettemp$percent_change,na.rm=TRUE))
  print(states[i])
  print(mean(datasettemp$percent_change,na.rm=TRUE))
  
}

state_change <-tibble(fips,states,howbadchange)

plot_usmap(data = state_change, values = "howbadchange") +  scale_fill_gradient2(low = "blue",mid = "white",high ="red",  midpoint = 0,
                                                                          guide = "colourbar") 

plot_usmap(data = state_change, values = "howbadchange") +  scale_fill_gradient2(low="blue",mid="white",high="red",space="Lab",
                                                                                 guide = "colourbar") 


inner<-dataset$instate
outer <-dataset$outstate
intoout <- 100*(outer)/(outer+inner)
dataset$intoout = intoout


outstater <- c()
for (i in 1:length(states)){
  datasettemp <- subset(dataset,gsub('NA','na',state) == states[i])
  datasettemp <- subset(datasettemp,is.finite(intoout))
  outstater <- c(outstater,mean(datasettemp$intoout,na.rm=TRUE))
}

state_out <-tibble(fips,states,outstater)

plot_usmap(data = state_out, values = "outstater") +  scale_fill_gradient(low = "#FFFFFF",high ="#FF0000",  
                                                                          guide = "colourbar") 



