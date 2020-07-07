import os
import pathlib

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from urllib.request import urlopen

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

map_df = pd.read_csv(DATA_PATH.joinpath("map_df0708.csv"),sep=',',error_bad_lines=False)

# mapbox token
mapbox_accesstoken = 'pk.eyJ1IjoiZC12ZiIsImEiOiJjazZuNTM4NnkwcjE0M3RsaTFtYTFoeWJnIn0.LWr2mmAYaNCG2CBk_PcD9Q'

with urlopen('https://raw.githubusercontent.com/d-vf/dash/master/data/map_df.json') as response:
    counties = json.load(response)

i=0
for feature in counties["features"]:
  feature ['id'] = str(i).zfill(0)
  i += 1

BGRI11 = map_df['LUG11DESIG'].str.title().tolist()

pl_deep=[[0.0, 'rgb(253, 253, 204)'],
         [0.1, 'rgb(201, 235, 177)'],
         [0.2, 'rgb(145, 216, 163)'],
         [0.3, 'rgb(102, 194, 163)'],
         [0.4, 'rgb(81, 168, 162)'],
         [0.5, 'rgb(72, 141, 157)'],
         [0.6, 'rgb(64, 117, 152)'],
         [0.7, 'rgb(61, 90, 146)'],
         [0.8, 'rgb(65, 64, 123)'],
         [0.9, 'rgb(55, 44, 80)'],
         [1.0, 'rgb(39, 26, 44)']]

Types = ['day 1','day 2','day 3','day 4','day 5','day 6','day 7'] 

TypesI = ['Discomfort day 1','Discomfort day 2','Discomfort day 3','Discomfort day 4','Discomfort day 5','Discomfort day 6', 'Discomfort day 7'] 

trace1 = []    

    
# order should be the same as "id" passed to location
for q in Types:
    trace1.append(go.Choroplethmapbox(
        geojson = counties,
        locations = map_df['Freguesias'].tolist(), 
        z = map_df[q].tolist(),
        colorscale = ["blue", "orange", "red"],
        text = BGRI11, 
        colorbar = dict(thickness=20, ticklen=3),
        zmin=20, zmax=30,
        marker_line_width=0, marker_opacity=0.7,
        visible=False,
        subplot='mapbox1',
        hovertemplate = "<b>%{text}</b><br><br>" +
                        "Temp: %{z}<br>" +
                        "<extra></extra>")) # "<extra></extra>" means we don't display the info in the secondary box, such as trace id.
    
trace1[0]['visible'] = True

trace2 = []    
    
# Suburbs order should be the same as "id" passed to location
for q in TypesI:
    trace2.append(go.Bar(
        x=map_df.sort_values([q], ascending=False).head(10)[q],
        y=map_df.sort_values([q], ascending=False).head(10)['LUG11DESIG'].str.title().tolist(),
        xaxis='x2',
        yaxis='y2',
        showlegend=False,
        marker=dict(
            color='rgba(255, 250, 250)',
            line=dict(
                color='rgba(91, 207, 135, 2.0)',
                width=0.5)
        ),
        visible=False,
        name='Nº {} Discomfort hours'.format(q),
        orientation='h',
    ))
    
trace2[0]['visible'] = True

#latitude and longitude values
latitude = 41.785061
longitude = -7.781880


layout = go.Layout(
    title = {'text': 'RELIABLE - Montalegre',
    		 'font': {'size':28, 
    		 		  'family':'Arial'}},
    autosize = True,
    width=1300,
    height =650,
    
    mapbox1 = dict(
        domain = {'x': [0.3, 1],'y': [0, 1]},
        center = dict(lat=latitude, lon=longitude), 
        accesstoken = mapbox_accesstoken, 
        zoom = 10 
        ),

    xaxis2={
        'zeroline': False,
        "showline": False,
        "showticklabels":True,
        'showgrid':True,
        'domain': [0, 0.25],
        'side': 'left',
        'anchor': 'x2',
    },
    yaxis2={
        'domain': [0.4, 0.9],
        'anchor': 'y2',
        'autorange': 'reversed',
    },
    margin=dict(l=20, r=20, t=50, b=50),
    paper_bgcolor='rgb(235, 235, 232)',
    plot_bgcolor='rgb(32, 44, 82)')

layout.update(updatemenus=list([
    dict(x=1,
         y=1.1,
         xanchor='left',
         yanchor='middle',
         direction="down",
         pad={"r": 10, "t": 10},
        showactive=True,
         buttons=list([
             dict(
                 args=['visible', [True, False, False, False, False, False, False]],
                 label='2020-07-08',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, True, False, False,False, False, False]],
                 label='2020-07-09',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, False, True, False,False, False, False]],
                 label='2020-07-10',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, False, False, True,False, False, False]],
                 label='2020-07-11',
                 method='restyle'
                ),
             dict(
                 args=['visible', [False, False, False, False,True, False, False]],
                 label='2020-07-12',
                 method='restyle'
                ),
             dict(
                 args=['visible', [False, False, False, False, False, True,False]],
                 label='2020-07-13',
                 method='restyle'
                 ),
            dict(
                 args=['visible', [False, False, False, False, False, False, True]],
                 label='2020-07-14',
                 method='restyle'
                 )
            ]),
        )]))
        

fig=go.Figure(data=trace2 + trace1, layout=layout)

# This is the part to initiate Dash app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children=''),

    dcc.Graph(
        id='example-graph-1',
        figure=fig
    ),

    html.Div(children='''
        IN+/IST | July 2020
    ''')
])

if __name__ == '__main__':
    app.run_server(debug=True)
