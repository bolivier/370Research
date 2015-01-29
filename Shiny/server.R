library(RCurl)
library(shiny)


shinyServer(function(input, output) {
  s <- getURL(URLencode('http://129.152.144.84:5001/rest/native/?query="select *  from DIAMONDS where ROWNUM <= 500"'), 
              httpheader=c(DB='jdbc:oracle:thin:@129.152.144.84:1521:orcl', 
                           USER='C##cs370_nos98', 
                           PASS='orcl_nos98', 
                           MODE='native_mode', 
                           MODEL='model', 
                           returnFor = 'R'), 
              verbose = TRUE) 
  
  sdf <- data.frame(eval(parse(text=substring(s, 1, 2^31-1))))
  
  
  
  # a large table, reative to input$show_vars
  output$mytable1 <- renderDataTable({
    sdf
  })  
})