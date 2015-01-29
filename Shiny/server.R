library(RCurl)
library(shiny)

# Limit the query to 10,000 items to speed up shiny app (nbd for now)
s <- getURL(URLencode('http://129.152.144.84:5001/rest/native/?query="select *  from DIAMONDS limit 10000"'), 
            httpheader=c(DB='jdbc:oracle:thin:@129.152.144.84:1521:orcl', 
                         USER='C##cs370_nos98', 
                         PASS='orcl_nos98', 
                         MODE='native_mode', 
                         MODEL='model', 
                         returnFor = 'R'), 
            verbose = TRUE) 

sdf <- data.frame(eval(parse(text=substring(s, 1, 2^31-1))))

shinyServer(function(input, output) {
  
  # a large table, reative to input$show_vars
  output$mytable1 <- renderDataTable({
    library(ggplot2)
    diamonds[, input$show_vars, drop = FALSE]
  })
  
  # sorted columns are colored now because CSS are attached to them
  output$mytable2 <- renderDataTable({
    mtcars
  }, options = list(orderClasses = TRUE))
  
  # customize the length drop-down menu; display 5 rows per page by default
  output$mytable3 <- renderDataTable({
    iris
  }, options = list(lengthMenu = c(5, 30, 50), pageLength = 5))
  
})