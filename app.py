#################################################################
# RBAD data portal v1.0
#################################################################

import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from collections import OrderedDict

import openpyxl

app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server

#################################################################
# Plots
#################################################################

df_Q = pd.read_excel('data_deploy/INDICATORS_Q.xlsx')
df_M = pd.read_excel('data_deploy/INDICATORS_M.xlsx')
df_rrp = pd.read_excel('data_deploy/sdir.xlsx')


## Changing dates

df_M['PERIOD'] = df_M['PERIOD'].dt.strftime('%m/%d/%Y')
df_Q['PERIOD'] = df_Q['PERIOD'].dt.strftime('%m/%d/%Y')
df_rrp['date'] = df_rrp['date'].dt.strftime('%m/%d/%Y')

df_Q['PERIOD'] = pd.to_datetime(df_Q['PERIOD'])
df_M['PERIOD'] = pd.to_datetime(df_M['PERIOD'])
df_rrp['date'] = pd.to_datetime(df_rrp['date'])

## Macroeconomic indicators

gdp = df_Q.loc[:, ['PERIOD', 'Gross Domestic Product (constant 2018 prices)']]
inf = df_M.loc[:, ['PERIOD', 'Inflation rate (2018=100), all items']]
usd = df_M.loc[:, ['PERIOD', 'FOREX: USD to PHP, end of period']]
rrp = df_rrp.loc[:, ['date', 'rrpovernight']]


gdp = gdp.rename(columns = {'Gross Domestic Product (constant 2018 prices)': 'rgdp'})
inf = inf.rename(columns = {'Inflation rate (2012=100), all items': 'inflation'})
usd = usd.rename(columns = {'FOREX: USD to PHP, end of period': 'usdphp'})


gdp = gdp.loc[(gdp['PERIOD'] <= "2021-10-01"),]
gdp['rgdpgr'] = 100*(gdp['rgdp'].pct_change(4))

# Filter dates to 2010

gdp = gdp.loc[(gdp['PERIOD'] >= "2010-01-01"),]
inf = inf.loc[(inf['PERIOD'] >= "2019-01-01"),]
usd = usd.loc[(usd['PERIOD'] >= "2010-01-01"),]
rrp = rrp.loc[(rrp['date'] >= "2010-01-01"),]


# Define plotting function


fig_gdp = go.Figure(go.Scatter(
    x = gdp['PERIOD'],
    y = gdp['rgdpgr']
))
fig_gdp.update_layout(
    title = 'Gross Domestic Product (Constant 2018 prices), y-o-y%',
    font = dict(
        family = 'Helvetica',
        size = 16,
        color = 'black'
    ),
    xaxis = dict(
        title = 'Quarter',
        linecolor = 'black',
        showgrid=False,
        tickformat ='%b %Y'),
    yaxis = dict(
        title = 'y-o-y % growth',
        linecolor = 'black',
        showgrid = False,
        zeroline = False),
        plot_bgcolor = 'white',
    )

fig_inf = go.Figure(go.Scatter(
    x = inf['PERIOD'],
    y = inf['inflation'],
    marker_color = "red"
))
fig_inf.update_layout(
    title = 'Inflation rate (2018 = 100), y-o-y%',
    font = dict(
        family = 'Helvetica',
        size = 16,
        color = 'black'
    ),
    xaxis = dict(
        title = 'Month',
        linecolor = 'black',
        showgrid=False,
        tickformat ='%b %Y',
        color = 'black'),
    yaxis = dict(
        title = 'y-o-y %',
        linecolor = 'black',
        showgrid = False,
        zeroline = False,
        color = 'black'),
        plot_bgcolor = 'white'
    )
    


fig_usd = go.Figure(go.Scatter(
    x = usd['PERIOD'],
    y = usd['usdphp'],
    marker_color = 'navy'
))
fig_usd.update_layout(
    title = 'USD-PHP exchange rates',
    font = dict(
        family = 'Helvetica',
        size = 16,
        color = 'black'
    ),
    xaxis = dict(
        title = 'Month',
        linecolor = 'black',
        showgrid=False,
        tickformat ='%b %Y'),
    yaxis = dict(
        title = 'PHP per USD',
        linecolor = 'black',
        showgrid = False,
        zeroline = False),
        plot_bgcolor = 'white',
    )   


fig_rrp = go.Figure(go.Scatter(
    x = rrp['date'],
    y = rrp['rrpovernight'],
    marker_color = 'green'
))
fig_rrp.update_layout(
    title = 'RRP overnight rates',
    font = dict(
        family = 'Helvetica',
        size = 16,
        color = 'black'
    ),
    xaxis = dict(
        title = 'Month',
        linecolor = 'black',
        showgrid=False,
        tickformat ='%b %Y'),
    yaxis = dict(
        title = '%',
        linecolor = 'black',
        showgrid = False,
        zeroline = False),
        plot_bgcolor = 'white',
    )       


#################################################################
# Forecast table (from Economic Weather Report)
#################################################################

fcast = OrderedDict(
    [
        ("Indicators", ["GDP growth (2018 = 100)", "Inflation (2018 = 100)", "Foreign Exchange Rate (EOP)", "O/N RRP rate (EOP)", "Budget Deficit (% of GDP)", "Gross International Reserves (billion USD)"]),
        ("2021", [5.6, 3.9, 50.8, 2.0, -7.6, 110.1]),
        ("2022F", [6.8, 3.4, 52.1, 2.5, -7.7, 112.0]),
        ("2023F", ["6-7", "3-4", 53.4, 3.0, -6.1, 116.0]),

    ]
)

fcastdf = pd.DataFrame(fcast)


 
#################################################################
# Style code
#################################################################

# Header

navbar = dbc.NavbarSimple(
    children=[
        #dbc.NavItem(dbc.NavLink("About", href="#")),
        dbc.Button("Download code", color="primary", className="me-1",
        href = "https://dlsuedu-my.sharepoint.com/:t:/g/personal/renz_calub_dlsu_edu_ph/EZ58ajrNicZHkkf9OX94IkgBk5XN1n0H_nzQvcd3CoMZLA?e=rr3qST",
        download = "dash_code.txt",
        external_link = True,
        ),
        
    ],
    brand="RBAD Macroeconomic Indicators",
    brand_href="#",
    color="dark",
    dark=True,
)


head = html.Div(
    [
    html.H3("Research and Business Analytics Department", style={'text-align': 'left'}),
    html.H4("Macroeconomic indicators", style={'text-align': 'left'}),
    ]   
)


# Graph panels

ROW0DBC = dbc.Row(
    [
     dbc.Col([
         dbc.Table.from_dataframe(fcastdf, striped = True, bordered = True, hover = True, class_name = "eight columns")
     ])   
    ]
)

ROW1DBC = dbc.Row(
    [
        dbc.Col(
            [
             dcc.Graph(id = "GDP", figure = fig_gdp, className = "six columns"),   
            ]
        ),
        dbc.Col(
            [
             dcc.Graph(id = "infl", figure = fig_inf, className = "six columns")   
            ]
        )
    ], className = "g-0",
)

ROW2DBC = dbc.Row(
    [
       dbc.Col(
           [
            html.Div(dcc.Graph(id = "usd", figure = fig_usd, className = "six columns")   )
           ]
       ),
       dbc.Col(
           [
            dcc.Graph(id = "rrp", figure = fig_rrp, className = "six columns")   
           ]
       ) 
    ]
)


ROW1 = html.Div(children = [
dcc.Graph(id = "GDP", figure = fig_gdp, className = "five columns"),
dcc.Graph(id = "infl", figure = fig_inf, className = "five columns"), #dash graph element
],)

ROW2 = html.Div(children = [
dcc.Graph(id = "usd", figure = fig_usd, className = "five columns"), #dash graph element
dcc.Graph(id = "rrp", figure = fig_rrp, className = "five columns"),
],)


colors = {"background": "#011833", "text": "#7FDBFF"}
app.layout = html.Div(children = [navbar, ROW1DBC, ROW2DBC, ROW0DBC], style={"text-align": "center"})
    
#################################################################
# Callbacks
#################################################################


if __name__ == '__main__':
    app.run_server(debug = True)


