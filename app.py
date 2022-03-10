import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

# here's the list of possible columns to choose from.
list_of_columns =['Total exports', 'Tree nuts', 'Rice', 'Feeds',
       'Dairy', 'Fresh fruit', 'Processed fruit', 'Fresh vegetables',
       'Processed vegetables', 'Soybeans', 'Corn', 'Wheat', 'Cotton']

myheading1 = "Lesson4 - Draw with plotly"
tabtitle = 'Plotly Map from US Agriculture'
sourceurl = 'https://plotly.com/python/builtin-colorscales/'
githublink = 'https://github.com/vharkar/301-old-mcdonald'


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/usa-2020-agriculture.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1(myheading1),
    html.Div([
      html.Div([
        html.H6('Select a produce:'),
        dcc.Dropdown(
            id='column-options',
            options=[{'label':i, 'value':i} for i in list_of_columns],
            value=list_of_columns[0],
        ),
      ],className='two columns'),
      html.Div([dcc.Graph(id='figure-1', figure=''),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

########## Define Callback
@app.callback(Output('figure-1', 'figure'),
             [Input('column-options', 'value')])
def draw_map(mycolumn):
    mygraphtitle = f'State wise distribution of income from {mycolumn} (in Millions USD) for 2020'
    mycolorscale = 'bluyl' # Note: The error message will list possible color scales.
    mycolorbartitle = "Millions USD"
    
    fig = go.Figure(data=go.Choropleth(
      locations=df['code'], # Spatial coordinates
      locationmode = 'USA-states', # set of locations match entries in `locations`
      z = df[mycolumn].astype(float), # Data to be color-coded
      colorscale = mycolorscale,
      colorbar_title = mycolorbartitle,
    ))

    fig.update_layout(
      title_text = mygraphtitle,
      geo_scope='usa',
      width=1200,
      height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server()
