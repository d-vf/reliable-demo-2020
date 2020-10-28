import os
import pathlib

import json
import dash
import os
import pathlib
from urllib.request import urlopen
import json
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
map_df = pd.read_csv(DATA_PATH.joinpath("map_df0717.csv"),sep=',',error_bad_lines=False)

# mapbox token
mapbox_accesstoken = 'pk.eyJ1IjoiZC12ZiIsImEiOiJjazZuNTM4NnkwcjE0M3RsaTFtYTFoeWJnIn0.LWr2mmAYaNCG2CBk_PcD9Q'

with urlopen('https://raw.githubusercontent.com/d-vf/dash/master/data/map_df.json') as response:
    counties = json.load(response)

#latitude and longitude values
latitude = 41.785061
longitude = -7.781880

i=0
for feature in counties["features"]:
  feature ['id'] = str(i).zfill(0)
  i += 1

BGRI11 = map_df['LUG11DESIG'].str.title().tolist()

map_df = map_df.rename(columns={'day 1': '18/07/2020', 'day 2': '19/07/2020', 'day 3': '20/07/2020', 'day 4': '21/07/2020', 'day 5': '22/07/2020', 'day 6': '23/07/2020', 'day 7':'24/07/2020'})

Types = ['18/07/2020','19/07/2020','20/07/2020','21/07/2020','22/07/2020','23/07/2020','24/07/2020'] 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1(
        'Reliable - Montalegre',
        style={
            'paddingLeft' : 50
            }
        ),
    html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': k, 'value': k} for k in Types],
        value=Types[0]
    ),
    html.Hr(),
    dcc.Graph(id='display-selected-values')
    ])
    ])


@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('day-dropdown', 'value')]
)
def update_output(value):
    fig = px.choropleth_mapbox(map_df,geojson=counties,
                    locations=map_df['Freguesias'], color= value,
                    range_color =[20,40],
                    mapbox_style='carto-positron',
                    zoom=9, center = {'lat': 41.785061, 'lon': -7.781880})
    fig.update_layout(title=f"<b>{value}</b>", title_x=0.5, width=1000, height=600)
    return fig    

fig.layout.images = [dict(
        source="https://raw.githubusercontent.com/d-vf/reliable-demo-2020/data/logos_reliable.png",
        xref="paper", yref="paper",
        x=0.5, y=-0.35,
        sizex=0.3, sizey=0.3,
        xanchor="center", yanchor="top"
      )]

py.iplot(fig, fileopt='overwrite', filename='data/logos_reliable.png')


if __name__ == '__main__':
    app.run_server(debug=True)
