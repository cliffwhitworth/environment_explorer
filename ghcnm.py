#######
# Dashboard of low and high yearly average temperatures given the country
# Data collected from Global Historical Climatology Network-Monthly (https://www.ncdc.noaa.gov/ghcnm/v3.php)
#######

# Import libraries
import dash
# https://dash.plot.ly/dash-core-components
import dash_core_components as dcc
# https://github.com/plotly/dash-html-components/tree/master/src/components
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import pickle

app = dash.Dash()

# ghcnm.tavg.v3.3.0.20170710.qca.dat ends up to be 75+ Mb file and can be created from ghcnm.ipynb at https://github.com/cliffwhitworth/environment_explorer
# Unable to upload to Github but has more data than the ghcnm_means.pkl file below
# with open('./ghcnm.tavg.v3.3.0.20170710.qca.dat.pkl', 'rb') as qca_file:
#     qca_temps = pickle.load(qca_file)

with open('./global_means.pkl', 'rb') as global_means_file:
    global_means = pickle.load(global_means_file)

df = global_means[global_means['YEAR'] == 2014]

# Able to upload to Github
with open('./ghcnm_means.pkl', 'rb') as qca_file:
    qca_temps = pickle.load(qca_file)

qca_temps.reset_index(inplace=True)
# Get country names from code
# countries = pd.read_csv('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3/country-codes', names=['codes'], header=None)
# countries[['CountryCode','Country']] = countries["codes"].str.split(" ", 1, expand=True)
# countries.drop('codes', axis = 'columns', inplace = True)
with open('./countrycodes.pkl', 'rb') as countrycodes:
    countries = pickle.load(countrycodes)

countries['CountryCode'] = countries['CountryCode'].astype('int64')
countries = countries.sort_values('Country', ascending = True)

pd.options.mode.chained_assignment = None  # default='warn'

cntrycode = 101
# mask2 = qca_temps['Country'].str.strip() == 'ALGERIA'
# Here are the country codes: ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3/country-codes
df_on_cntrycode = qca_temps[qca_temps['CountryCode'] == cntrycode]

codes = []
for CountryCode, Country in countries.iterrows():
#     print (CountryCode, Country)
    codes.append({'label': Country.Country.strip(), 'value': Country.CountryCode})

sorted_years = df_on_cntrycode.sort_values("YEAR", ascending = True)
available_years = sorted_years.YEAR.unique()

# drop observations without all 12 months; read documentation regarding missing values
df_on_cntrycode.replace(-9999, np.NaN, inplace=True)
df_on_cntrycode.dropna(inplace=True)

# years to compare
loYear = df_on_cntrycode['YEAR'] == 1856
hiYear = df_on_cntrycode['YEAR'] == 2016
temps_min = df_on_cntrycode[loYear]
temps_max = df_on_cntrycode[hiYear]

app.layout = html.Div([
    html.Div([
        html.H1('Global Historical Climatology Network-Monthly'),
        html.P('Compare low and high yearly average temperatures given the country'),
        html.A('Code on Github', href='https://github.com/cliffwhitworth/environment_explorer'),
        html.Br(),
        html.A('GHCNM site', href='https://www.ncdc.noaa.gov/ghcnm/v3.php'),
        html.Br(),
        html.A('Observing stations', href='https://www.wmo.int/cpdb/volume_a_observing_stations/list_stations')
    ]),
    html.Hr(),
    html.Div([
        html.Div([
            html.H3('Select Country:'),
            dcc.Dropdown(
                id='country_code',
                options=codes,
                value='101' # sets a default value
            )
        ], style={'width': '30%', 'display':'inline-block', 'padding-right': '13px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}),
        # style={'display':'inline-block', 'padding-right': '13px', 'overflow': 'hidden', 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}),
        html.Div([
            html.H3('Select Lo Year:'),
            dcc.Dropdown(
                id='lo_year',
                options=[{'label': i, 'value': i} for i in available_years],
                value='1856'
            )
        ], style={'display':'inline-block', 'padding-right': '13px'}),
        html.Div([
            html.H3('Select Hi Year:'),
            dcc.Dropdown(
                id='hi_year',
                options=[{'label': i, 'value': i} for i in available_years],
                value='2016'
            )
        ], style={'display':'inline-block'}),
        html.Div([
            html.Button(
                id='submit-button',
                n_clicks=0,
                children='Submit'
            ),
        ], style={'margin-top':'10px'}),
    ], style={'padding': '7px'}),
    html.Hr(),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                # the commented lines below are for the ghcnm.tavg.v3.3.0.20170710.qca.dat.pkl file
                # {'name': 'Lo Year Average', 'x': np.arange(0, 12, 1), 'y': temps_min.iloc[:,4:16].mean().tolist()},
                # {'name': 'Hi Year Average', 'x': np.arange(0, 12, 1), 'y': temps_max.iloc[:,4:16].mean().tolist()}
                {'name': 'Lo Year Average', 'x': np.arange(0, 12, 1), 'y': temps_min.iloc[:,2:14].values.flatten()},
                {'name': 'Hi Year Average', 'x': np.arange(0, 12, 1), 'y': temps_max.iloc[:,2:14].values.flatten()}
            ]
        }
    ),
    html.Hr(),
    html.Div([
        html.H1('Global Means')
    ]),
    html.Div([
        html.H3('Select Year:'),
        dcc.Dropdown(
            id='global_year',
            options=[{'label': i, 'value': i} for i in available_years],
            value='2016'
        )
    ], style={'display':'inline-block', 'padding-right': '13px'}),
    dcc.Graph(
        id='my_graph2',
        figure={
            'data': [
                dict(
                    type = 'choropleth',
                    colorscale = 'Rainbow',
                    reversescale = True,
                    locations = df['Country'],
                    locationmode = "country names",
                    z = df['YearAvg'],
                    text = df['Country'],
                    colorbar = {'title' : 'Global Means'},
                  )
            ],
            'layout': {
                'title':'Global Means',
                'geo':dict(
                    showframe = False,
                    projection = {'type':'natural earth'}
                )
            }
        }
    )
], style={'padding': '0px', 'margin': '0px'})

def resetYears(code):
    df_on_cntrycode = qca_temps[qca_temps['CountryCode'] == int(code)]

    # drop observations without all 12 months; read documentation regarding missing values
    df_on_cntrycode.replace(-9999, np.NaN, inplace=True)
    df_on_cntrycode.dropna(inplace=True)
    sorted_years = df_on_cntrycode.sort_values("YEAR", ascending = True)
    available_years = sorted_years.YEAR.unique()
    options=[{'label': i, 'value': i} for i in available_years]
    return options

@app.callback(
    Output('lo_year', 'options'),
    [Input('country_code', 'value')])
def callback_lo(cntrycode):
    return resetYears(cntrycode)

@app.callback(
    Output('hi_year', 'options'),
    [Input('country_code', 'value')])
def callback_hi(cntrycode):
    return resetYears(cntrycode)

@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('country_code', 'value'),
    State('lo_year', 'value'),
    State('hi_year', 'value')])
def update_graph(n_clicks, cntrycode, loYear, hiYear):
    df_on_cntrycode = qca_temps[qca_temps['CountryCode'] == int(cntrycode)]

    # drop observations without all 12 months; read documentation regarding missing values
    df_on_cntrycode.replace(-9999, np.NaN, inplace=True)
    df_on_cntrycode.dropna(inplace=True)

    # years to compare
    a_loYear = df_on_cntrycode['YEAR'] == int(loYear)
    a_hiYear = df_on_cntrycode['YEAR'] == int(hiYear)
    temps_min = df_on_cntrycode[a_loYear]
    temps_max = df_on_cntrycode[a_hiYear]

    fig = {
        'data': [
            # the commented lines below are for the ghcnm.tavg.v3.3.0.20170710.qca.dat.pkl file
            # {'name': 'Lo Year Average', 'x': np.arange(0, 12, 1), 'y': temps_min.iloc[:,4:16].mean().tolist()},
            # {'name': 'Hi Year Average', 'x': np.arange(0, 12, 1), 'y': temps_max.iloc[:,4:16].mean().tolist()}
            {'name': 'Lo Year Average', 'x': np.arange(0, 12, 1), 'y': temps_min.iloc[:,2:14].values.flatten()},
            {'name': 'Hi Year Average', 'x': np.arange(0, 12, 1), 'y': temps_max.iloc[:,2:14].values.flatten()}
        ],
        'layout': {
            'title':'Lo Hi Year Comparison',
            'xaxis': {'title': 'Month'},
            'yaxis': {'title': 'Hundredths degree celcius'}
            }
    }
    return fig

@app.callback(
    Output('my_graph2', 'figure'),
    [Input('global_year', 'value')])
def update_graph(value):
    df = global_means[global_means['YEAR'] == value]

    fig = {
        'data': [
            dict(
                type = 'choropleth',
                colorscale = 'Rainbow',
                reversescale = True,
                locations = df['Country'],
                locationmode = "country names",
                z = df['YearAvg'],
                text = df['Country'],
                colorbar = {'title' : 'Global Means'},
              )
        ],
        'layout': {
            'title':'Global Means',
            'geo':dict(
                showframe = False,
                projection = {'type':'natural earth'}
            )
        }
    }
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
