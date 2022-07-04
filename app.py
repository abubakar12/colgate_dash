import numpy as np
import plotly.express as px
import pandas as pd
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback,FileSystemStore
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default='browser'
from datetime import date, timedelta
import datetime
import numpy as np
import urllib.parse
import urllib
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate
import dash
selected_chart_template='simple_white'
ai_green="#228779"
ai_gray="#bab0ac"
color="white"
import pyodbc
import dash_pivottable
from dash import Dash,dcc, html, Input, Output, callback,dash_table
from supporting_codes import abc_setup
from supporting_codes import xyz_setup
from supporting_codes import pivot_table_case_fulfilment
from supporting_codes import abc_xyz_segmentation
filter_color="#546e7a"
font_filter={"color":"white","font-weight": "bold"}
screen_bg_color="#eceff1"
style_bg={"background-color": screen_bg_color}



#############################################################################
# Style modifications
#############################################################################
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
}

TEXT_STYLE = {"textAlign": "center"}

DROPDOWN_STYLE = {"textAlign": "left"}



style_link={ "width":"300px","margin": "0 auto","font-size": "1.2rem","font-family": "sans-serif",\
            "color":"white","border-style": "solid",}
app = app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Shopify Data Analysis"
app.layout = dbc.Container(
    [
     dcc.Location(id="url", refresh=True), 
     dbc.Row([dbc.Col(dbc.Alert(dcc.Link('abc_xyz_segmentation', href="/",className="alert-link",style=font_filter),color=filter_color)),
             dbc.Col(dbc.Alert(dcc.Link('pivot_table_case_fulfilment', href="/pivot_table_case_fulfilment/",className="alert-link",style=font_filter),color=filter_color)),
             dbc.Col(dbc.Alert(dcc.Link('xyz_setup', href="/xyz_setup/",className="alert-link",style=font_filter),color=filter_color)),
             dbc.Col(dbc.Alert(dcc.Link('abc_setup', href="/abc_setup/",className="alert-link",style=font_filter),color=filter_color))]),
     dbc.Row(dbc.Col(id="page-content",style={"padding":"0px"},width=True))
     ],
   fluid=True,
)

# Multi-page selector callback - not really used, but left in for future use
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    # Left in because I'm not sure if this will be a muli-page app at some point
    # link=f"/prod_id_page/?client_id={}"
    if pathname == "/abc_setup/":
        return abc_setup.main_page_var
    elif pathname == "/pivot_table_case_fulfilment/":
        return  pivot_table_case_fulfilment.main_page_var
    elif pathname == "/xyz_setup/":
        return  xyz_setup.main_page_var
    else:
        return abc_xyz_segmentation.main_page_var


###################################################
# Server Run
###################################################
app.config['suppress_callback_exceptions'] = True
if __name__ == '__main__':
    app.run_server(debug=True,port=3100)
