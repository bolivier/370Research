library(shiny)
library(ggplot2)  # for the diamonds dataset

shinyUI(fluidPage(
  title = 'Examples of DataTables',
  sidebarLayout(
    sidebarPanel(
      conditionalPanel(
        'input.dataset === "diamonds"',
        # needs to use our diamonds data
        checkboxGroupInput('show_vars', 'Columns in diamonds to show:',
                           names(sdf), selected = names(sdf))
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