library(RCurl)
library(shiny)
library(RJSONIO)

# Limit the query to 500 items to speed up shiny app (nbd for now)

shinyServer(function(input, output) {
  s <- getURL(URLencode('http://129.152.144.84:5001/rest/native/?query="select * from DIAMONDS where ROWNUM <= 15000"'), 
              httpheader=c(DB='jdbc:oracle:thin:@129.152.144.84:1521:orcl', 
                           USER='C##cs370_nos98', 
                           PASS='orcl_nos98', 
                           MODE='native_mode', 
                           MODEL='model',
                           returnDimensions = 'False',
                           returnFor = 'JSON'), 
              verbose = TRUE) 
  
  sd <-fromJSON(s)
  sdf <<- do.call("rbind", sd)
  data_frame <- sdf[-1,]
  colnames(data_frame) <- sdf[1,]

  # a large table, reative to input$show_vars
  output$mytable1 <- renderDataTable({
    library(ggplot2)
    data_frame[, ]
  })  
})