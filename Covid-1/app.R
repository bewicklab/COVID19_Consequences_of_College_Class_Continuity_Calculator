library(shiny)
library(maps)
library(mapproj)
library(usmap)
library(ggplot2)
library(tibble)
library(reticulate)
library(tidyverse)
library(xtable)



source("helpers.R")
source("R_calculation.R")

# Define UI for app that asks a series of questions ----
covids <- read.csv(file = 'totals_by_state_per_school.csv', encoding = "UTF-8")
universities <- colnames(covids)
universities=universities[universities!="X"]
universities=universities[universities!="X.1"]
universities=universities[universities!="X.2"]
universities=universities[universities!="X.3"]
universities=universities[universities!="X.4"]
universities=universities[universities!="X.5"]
universities=universities[universities!="X.6"]
universities=gsub('XXXXX','&',universities)
universities=gsub('YYYYY',' - ',universities)
universities=gsub('ZZZZZ','\\"',universities)
universities=gsub('\\.',' ',universities)
#print(universities[1056])

ui <- fluidPage(
  titlePanel(h2("COVID-19 Consequences of College Continuity Calculator")),
  
  
  sidebarLayout(position = "left",
                sidebarPanel(h4("Model Parameters"),
                             
                             selectizeInput(
                               "state", "School of interest (if your school is not on the list, type in a keyword)", universities,
                               multiple = FALSE,
                               selected = 'Clemson University'
                             ),
                             
                             #dateInput("dob", "Student return date",value = "2020-08-15", min = "2020-03-01", max = "2020-11-1"),
                             
                            
                             uiOutput("moreControls"),
                             
                             sliderInput("incub", "COVID-19 incubation period* (days)", value = 5, min = 0, max = 20),      
                             
                             sliderInput("infec", "COVID-19 infectious period** (days)", value = 10, min = 0, max = 90),  
                             sliderInput("quarantine", "Mandatory quarantine length (days)", value = 0, min = 0, max = 30),  
                             sliderInput("testing", "Percentage of students tested following quarantine (%)", value = 50, min = 0, max = 100),  
                             sliderInput("fnrate", "False negative rate for COVID-19 test (%)", value = 20, min = 0, max = 100),  
                             radioButtons("model", "Scenario (based on IHME models***)",
                                          choices = list("Mandates Easing" = 1, "Current Projection" = 2,
                                                         "Universal Masks" = 3),selected = 1),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             p('This tool is brought to you by:'),
                             fluidRow(
                               column(3, offset = 2,
                               img(src = "Bewick_lab_logo.png", height = 100, width = 200)
                               ),
                             ),
                             fluidRow(p(''),
                                      p(''),
                                      ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(
                               column(3, offset = 2,
                                      img(src = "CCC.png", height = 70, width = 200)
                               ),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             p('in collaboration with researchers from:'),
                             fluidRow(
                               column(3, offset = 2,
                                      img(src = "centered_biology.png", height = 130, width = 200)
                               ),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(
                               column(3, offset = 2,
                                      img(src = "bm_HS_Math_RF2_hz_4c.png", height = 40, width = 200)
                               ),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             fluidRow(p(''),
                                      p(''),
                             ),
                             h6('*the length of time between exposure and when a person first develops symptoms or receives a positive COVID-19 test'),
                             h6('**the length of time that a person can infect others after first developing symptoms or after first receiving a positive COVID-19 test'),
                             h6('***currently using IHME models from July 14, 2020')
                             
                             
                             
                ),
                mainPanel(h4("Model Predictions*"),
                          htmlOutput("selected_var",style = "font-size:15px",style="white-space: pre-wrap"),   
                          h4("Heatmap of the states of origin of students carrying COVID-19"),
                          plotOutput("map"),
                          htmlOutput("spacer"),
                          h4("States expected to contribute at least one student carrying COVID-19"),
                          fluidRow(
                            column(5, offset = 1,
                                   tableOutput("table")
                            )
                          ),
                          fluidRow(p(''),
                                   p(''),
                          ),
                          fluidRow(p(''),
                                   p(''),
                          ),
                          p('*Predictions are based on college enrollment data from 2017-2018 (https://www.collegefactual.com) and Institute for Health Metrics and Evaluation (IHME) state-level projections of COVID-19 infection rates (https://covid19.healthdata.org/united-states-of-america)'),  
                          p('Disclaimer: The authors make no guarantee regarding the accuracy of predictions made using this tool. Persons or institutions that choose to use these predictions for decision-making purposes agree to do so at their own risk, and will not hold the authors of this tool, Clemson University, University of Maryland or Virginia Commonwealth University responsible for any real or perceived damages that result.'),
                          p('For questions, comments or additional information, please email Sharon Bewick: sbewick@clemson.edu')
                          
                )
                
  )
  
  
  
)




# Define server logic required to generate questions-
server <- function(input, output) {
  
  output$spacer <- renderText({ 
    
    returnedText = ("<br/><br/><br/>")
  })
  
  output$selected_var <- renderText({ 
    req(input$state)
    req(input$dob)
    infectious_period = input$infec
    incubation_period = input$incub
    date = input$dob
    if (input$model == 1){
      scenario = 'worst'}
    else if (input$model == 2){
      scenario = 'reference'}
    else{
      scenario = 'best'}
    school = gsub(' ','\\.',gsub('\\"','ZZZZZ',gsub(' - ','YYYYY',gsub('&','XXXXX',input$state))))
    quarantine_length = input$quarantine
    testing_rate = input$testing
    fn_rate = input$fnrate

    tempfun <- R_calculation(infectious_period, incubation_period, date, scenario, school,quarantine_length,testing_rate,fn_rate)
    s1<-'There is a'
    s2<-toString(round(100*tempfun[[3]][[5]]),3) 
    s3 <- '% chance that at least one student will bring COVID-19 to campus ( range: '
    s4 <-toString(round(100*tempfun[[3]][[3]]),3)
    s5 <-'% - '
    s6 <-toString(round(100*tempfun[[3]][[7]]),3)
    s7 <-'%)<br/><br/>'
    s8 <- toString(as.integer(tempfun[[3]][[4]]))
    s9 <- 'students are predicted to arrive on campus carrying the COVID-19 virus ( range: ' 
    s10 <- toString(as.integer(tempfun[[3]][[2]]))
    s11 <- ' - '
    s12 <- toString(as.integer(tempfun[[3]][[6]]))
    s13 <- ')<br/>'
    s14 <-'.....  '
    s15 <- toString(as.integer(tempfun[[1]][[4]])) 
    s16 <- 'of these students will have active COVID-19 infections ( range: '
    s17 <- toString(as.integer(tempfun[[1]][[2]]))
    s18 <-' - '
    s19 <- toString(as.integer(tempfun[[1]][[6]]))
    s20 <- ')<br/>.....  '
    s21 <- toString(as.integer(tempfun[[2]][[4]]))
    s22 <- 'of these students will still be in the incubation phase ( range: '
    s23 <- toString(as.integer(tempfun[[2]][[2]]))
    s24 <- ' - '
    s25 <- toString(as.integer(tempfun[[2]][[6]]))
    s26 <- ')<br/><br/>The proposed testing strategy is expected to miss '
    s27 <- toString(as.integer(tempfun[[5]]))
    s28 <- 'students carrying the COVID-19 virus (range: '
    s29 <- toString(as.integer(tempfun[[4]]))
    s30 <- ' - '
    s31 <-toString(as.integer(tempfun[[6]]))
    s32 <- ')<br/><br/>'
    returnedText = paste(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32)
    
  })
  
  
  output$map <- renderPlot({  
    req(input$state)
    req(input$dob)
    infectious_period = input$infec
    incubation_period = input$incub
    date = input$dob
    if (input$model == 1){
      scenario = 'worst'}
    else if (input$model == 2){
      scenario = 'reference'}
    else{
      scenario = 'best'}
    school = gsub(' ','\\.',gsub('\\"','ZZZZZ',gsub(' - ','YYYYY',gsub('&','XXXXX',input$state))))
    
    quarantine_length = input$quarantine
    testing_rate = input$testing
    fn_rate = input$fnrate
    tempfun <- R_calculation(infectious_period, incubation_period, date, scenario, school,quarantine_length,testing_rate,fn_rate)
    tcounties <- tempfun[[9]]

    plot_usmap(data = tcounties, values = "totmean_number_cases") +  scale_fill_gradient(low = "#FFFFFF",high ="#FF0000",  
                                                                             guide = "colourbar") 
  })
  
  
  output$table <- renderTable({  
    
    req(input$state)
    req(input$dob)
    infectious_period = input$infec
    incubation_period = input$incub
    date = input$dob
    if (input$model == 1){
      scenario = 'worst'}
    else if (input$model == 2){
      scenario = 'reference'}
    else{
      scenario = 'best'}
    school = gsub(' ','\\.',gsub('\\"','ZZZZZ',gsub(' - ','YYYYY',gsub('&','XXXXX',input$state))))
    quarantine_length = input$quarantine
    testing_rate = input$testing
    fn_rate = input$fnrate
    
    tempfun <-R_calculation(infectious_period, incubation_period, date, scenario, school,quarantine_length,testing_rate,fn_rate)
    tsickcounties <- arrange(tempfun[[10]],-case_counts)
    
    xtable(tsickcounties) 
    
    
    
  })
  
  
  
  output$moreControls <- renderUI({
    req(input$incub)
    req(input$infec)
    db <- as.Date("2020-11-1")-input$incub
    dd <- as.Date("2020-07-19")+input$infec
    other <- dd+(db-dd)/2
    if ("2020-08-15">dd){
    tagList(
      dateInput("dob", "Student return date",value = "2020-08-15", min = dd, max = db),
    )} else{
      tagList(
        dateInput("dob", "Student return date",value = dd, min = dd, max = db),
      )
    }
  })
  
  
  
  
}

shinyApp(ui = ui, server = server)