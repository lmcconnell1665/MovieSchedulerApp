# Luke McConnell
# 2/24/20
# BZAN 544

# Movie schedule creating application

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import plotly.figure_factory as ff
import os
import re
import CreateSchedules

# Check and create schedules as needed
CreateSchedules.CheckSchedules()

# Reads in existing schedules
Schedules = [f.name for f in os.scandir("Schedules") if f.is_file() & bool(re.search(".*\.csv$",f.name))]

TheatreNames = [{'label':th.split(".",1)[0], 'value':th} for th in Schedules]

# Adding external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## 3.APPLICATION CREATION
# Create the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create the layout
app.layout = html.Div([ #contains everything on page, necessary for styling like page background etc.
    
    html.Div([
        html.H2('Movie Schedules'), #Dashboard title
        ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}), #closes title html.Div
    
    html.Div([
        html.P([
                html.Div([
                'Choose a Cinema to view the schedule:', #Dropdown instructions 
                #Cinema selection dropdown
                dcc.Dropdown(
                    id = 'Dropdown', 
                    options = TheatreNames, 
                    multi = False,
                    value = 'TB_original_Schedules.csv'
                )], style={'width': '49%', 'display': 'inline-block', 'marginBottom': 20}), #closes dropdown html.Div
        ]) #closes html.P
    ]), #closes html.Div
            
    html.Div([ #Gantt chart
        html.H5('Instructions: Mouse over the squares to see the schedule details. Click on the legend titles to hide/unhide segments'),
        dcc.Graph(id = "Graph")
    ]), #closes the graph html.div
    
    html.Div([
        html.H3('Theatre Show Schedule'),
        dash_table.DataTable(id='table') #closes the table html.div
    ]) #closes the html.Div
]) #closes layout section

#Call back section
@app.callback(
    [Output(component_id = 'Graph', component_property = 'figure'),
     Output(component_id = 'table', component_property = 'columns'),
     Output(component_id = 'table', component_property = 'data')],
    [Input(component_id = 'Dropdown', component_property = 'value')]
)

def update_graph(cinema):
    """Updates the chart and table based on the selection in the dropdown menu."""
    if cinema != None:
        schedule = pd.read_csv('Schedules/'+cinema)
        schedule_clean = schedule
        #Creates the Gantt chart
        Movies = [dict(Task= row[1].theatre, 
                       Start= row[1].startTimeDate, 
                       Finish = row[1].endTimeDate, 
                       Resource = row[1].movie) for row in schedule.iterrows()]
        
        Trailers = [dict(Task= row[1].theatre, 
                       Start= row[1].startTimeDate_Trailer, 
                       Finish = row[1].endTimeDate_Trailer, 
                       Resource = 'Trailers') for row in schedule.iterrows()]
        
        PreAds = [dict(Task= row[1].theatre, 
                       Start= row[1].startTimeDate_PreAds, 
                       Finish = row[1].endTimeDate_PreAds, 
                       Resource = 'Pre-Show Ads') for row in schedule.iterrows()]
        
        CleanUp = [dict(Task= row[1].theatre, 
                       Start= row[1].startTimeDate_CleanUp, 
                       Finish = row[1].endTimeDate_CleanUp, 
                       Resource = 'Post-Show Cleanup') for row in schedule.iterrows()]
        
        Movies = Movies + Trailers + PreAds + CleanUp
        
        gantt = ff.create_gantt(Movies, index_col='Resource', group_tasks=True, show_hover_fill = True, show_colorbar = True)
        
        schedule_clean = schedule_clean.drop(columns = ['timeUnit', "endTimeDate_Trailer", "endTimeDate_PreAds", "startTimeDate_CleanUp"])
        
        #table children
        #columns = [{"name": i, "id": i} for i in schedule.columns] #auto generate columns
        columns = [{'name' : 'Movie', "id" : 'movie'}, #manually fixing column names to show friendly names
                   {'name' : "Theatre Number", "id" : 'theatre'},
                   #{'name' : 'Time Units', "id" : 'timeUnit'}, 
                   {'name' : 'Movie Start Time', "id" : 'startTimeDate'}, 
                   {'name' : 'Movie End Time', "id" : 'endTimeDate'}, 
                   {'name' : 'Trailer Start Time', "id" : 'startTimeDate_Trailer'}, 
                   #{'name' : 'Trailer End Time', "id" : 'endTimeDate_Trailer'}, 
                   {'name' : 'Pre-Show Ad Start Time', "id" : 'startTimeDate_PreAds'}, 
                   #{'name' : 'Pre-Show Ad End Time', "id" : 'endTimeDate_PreAds'}, 
                   #{'name' : 'Clean Up Start Time', "id" : 'startTimeDate_CleanUp'}, 
                   {'name' : 'Clean Up End Time', "id" : 'endTimeDate_CleanUp'},]
        
        data = schedule_clean.to_dict('records') #fixing data to only show most relevant columns
    
        return gantt, columns, data
        
if __name__ == "__main__":
    app.run_server(debug=True)