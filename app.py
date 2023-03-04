'''
Fix Quarter issue - and consolidate function
Call image only 1 time and then update the values
separate long period component from seconds / min and hour components
'''
 
 
import datetime
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
 
# define dash app
app = dash.Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
app.title = 'OS Year Progress'
server = app.server
 
# define constants
num_of_months = 12 # month_progress = current_month / num_of_months
num_of_quarters = 4 # quarter in progress
num_of_weeks = 53 # week_progress = current_week / num_of_weeks
num_of_days = 366 # Year in progress = year_day / num_of_days
num_of_hours = 24 # day_progress = current_hour / num_of_hours
num_of_min = 60 # hour_progress = current_min / num_min
num_of_sec = 60 # in a min
num_of_days_in_week = 7 # weekday_progress = week_day / num_of_days_in_week
num_of_days_in_month = [(1,31), (2, 29), (3, 31), (4, 30), (5, 31), (6, 30),
                        (7,31), (8,31), (9,30), (10,31), (11, 30), (12,31) ] # month_progress = month_day / total_days
 
# core function
def core_time():
    return datetime.datetime.now()
 
# Quarter function
def quarter_progress(current_month, current_year_day):
    if int(current_month) in range(1,4):
        current_quarter = 1
        current_day_in_quarter = current_year_day
        total_days_in_quarter = sum([i[1] for i in num_of_days_in_month[0:3]])
        return current_day_in_quarter/total_days_in_quarter 
    if int (current_month) in range(4,7):
        current_quarter = 2
        current_day_in_quarter = current_year_day - sum([i[1] for i in num_of_days_in_month[0:3]])
        total_days_in_quarter = sum([i[1] for i in num_of_days_in_month[3:6]])
        return current_day_in_quarter / total_days_in_quarter
    if int(current_month) in range(7,10):
        current_quarter = 3
        current_day_in_quarter = current_year_day - sum([i[1] for i in num_of_days_in_month[0:3]]) - sum([i[1] for i in num_of_days_in_month[3:6]])
        total_days_in_quarter = sum([i[1] for i in num_of_days_in_month[6:9]])
        return current_day_in_quarter / total_days_in_quarter
    if int (current_month) in range(10,13):
        current_quarter = 4
        current_day_in_quarter = current_year_day - sum([i[1] for i in num_of_days_in_month[0:3]]) - sum([i[1] for i in num_of_days_in_month[3:6]]) \
            - sum([i[1] for i in num_of_days_in_month[6:9]])
        total_days_in_quarter = sum([i[1] for i in num_of_days_in_month[9:12]])
        return current_day_in_quarter / total_days_in_quarter

 
# Month Days functions
def days_in_month(num_of_days_in_month, current_month):
    for i, j in num_of_days_in_month:
        if i == int(current_month):
            return j
   
 
def progressFunc(r):
    current_month_name = r.strftime('%B')
    current_month = r.strftime('%m')
    current_week_day_name = r.strftime('%A')
    current_week_day = r.strftime('%w')
    current_year_day = r.strftime('%j')
    current_week = r.strftime('%U')
    current_day = r.day
    current_minute = r.minute
    current_hour = r.hour
    current_sec = r.second
    year_progress = int(round(int(current_year_day) / num_of_days, 2)*100)
    quart_progress = int(quarter_progress(current_month, int(current_year_day))*100)
    month_progress = int(round(int(current_day) / days_in_month(num_of_days_in_month, current_month), 2)*100)
    week_progress = (round((int(current_week_day) +1) / num_of_days_in_week, 4)*100)
    day_progress = (round(int(current_day) / num_of_days_in_week, 4)*100)
    hour_progress = (round(int(current_hour) / num_of_hours, 4)*100)
    min_progress = (round(int(current_minute) / num_of_min, 4)*100)
    sec_progress = (round(int(current_sec) / num_of_sec, 4)*100)
    timeDataOut = {
                    "current_month_name": current_month_name,
                    "current_month": current_month,
                    "current_week_day_name": current_week_day_name,
                    "current_day": current_day,
                    "year_progress": year_progress,
                    "quart_progress": quart_progress,
                    "month_progress": month_progress,
                    "week_progress":  week_progress,
                    "day_progress": day_progress,
                    "hour_progress":  hour_progress,
                    "min_progress": min_progress,
                    "sec_progress": sec_progress
 
    }
    return timeDataOut
 
# status fig function
 
def statusFig(title, v, max):
    gradbarFig = daq.GraduatedBar(
                                    showCurrentValue=True,
                                    max=100,
                                    value=v,
                                    label= title,
                                    #size=1000,
                                    step=1
                                )
    return gradbarFig 
 
 
app.layout = html.Div([
                html.Div([ # main top calendar/time row
                    
                    html.Div([
                        html.Div([
                            html.H4(id='current_month_string'),
                            html.H1(id='current_day', className='display-3'),
                            html.P(id='week_day_name')
                        ], className='text-center card col-6')
                    ], className='row col-8 offset-4'),

                    html.Div([
                        html.Div([
                            html.Br(),
                            daq.LEDDisplay(id='current_time'),
                        ], className='mx-auto col-6'),
                        dcc.Interval(
                            id='interval_component',
                            interval=1*1000,
                            n_intervals=0
                            )
                        ], className='row col-8 offset-2')

                ], className='row'),
               
                html.Div([
                
                html.Div([              # progress sections
                    html.Br(),
                    html.Div(id='year_progress'),
                    html.Br(),
                    html.Div(id='quart_progress'),
                    html.Br(),
                    html.Div(id='month_progress'),
                    html.Br(),
                    html.Div(id='week_progress'),
                    html.Br(),
                    html.Div(id='hour_progress'),
                    html.Br(),
                    html.Div(id='min_progress'),
                    html.Br(),
                    html.Div(id='sec_progress')
                ], className='col-12'),
                ], className='row'),
                html.Br(),
                html.Hr(),
                html.Div([
                    html.H6("Obsidian Steel Copyright © 2019–2020", className='mx-auto')
                ], className='row')
 
], className='container')
 
 
@app.callback(
    [Output('current_time', 'value'),
    Output('current_month_string', 'children'),
    Output('current_day', 'children'),
    Output('week_day_name', 'children'),
    Output('year_progress', 'children'),
    Output('quart_progress', 'children'),
    Output('month_progress', 'children'),
    Output('week_progress', 'children'),
    Output('hour_progress', 'children'),
    Output('min_progress', 'children'),
    Output('sec_progress', 'children'),
    ],
    [Input('interval_component', 'n_intervals')
    ])
def update_time(n):
    r = core_time()
    # send r to function and get results
    timeDataOut = progressFunc(r)
    if r.second <10:
        two_digits = "0"+str(r.second)
    else:
        two_digits = str(r.second)
    if r.minute<10:
        min_two_digits = "0"+str(r.minute)
    else: 
        min_two_digits = str(r.minute)
    clock_display = (str(r.hour) + ":" + min_two_digits + ":" + two_digits)
    return clock_display, timeDataOut['current_month_name'], \
            timeDataOut['current_day'], timeDataOut['current_week_day_name'], \
            statusFig('Year Progress', timeDataOut['year_progress'], num_of_days), \
            statusFig('Quarter Progress', timeDataOut['quart_progress'], num_of_quarters), \
            statusFig('Month Progress', timeDataOut['month_progress'], days_in_month(num_of_days_in_month, timeDataOut['current_month'])), \
            statusFig('Week Progress', timeDataOut['week_progress'], num_of_weeks), \
            statusFig('Hour Progress', timeDataOut['hour_progress'], num_of_hours), \
            statusFig('Minute Progress', timeDataOut['min_progress'], num_of_min), \
            statusFig('Seconds', timeDataOut['sec_progress'], num_of_sec)
 
 
if __name__ == '__main__':
    app.run_server(debug=True)