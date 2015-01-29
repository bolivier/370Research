library(shiny)
library(ggplot2)  # for the diamonds dataset

shinyUI(fluidPage(
  title = 'Examples of DataTables',
  sidebarLayout(
    sidebarPanel(
      conditionalPanel(
        'input.dataset === "diamonds"',
        checkboxGroupInput('show_vars', 'Columns in diamonds to show:',
                           names(diamonds), selected = names(diamonds))
      )
    ),
    mainPanel(
      tabsetPanel(
        id = 'dataset',
        tabPanel('diamonds', dataTableOutput('mytable1'))
      )
    )
  )
))