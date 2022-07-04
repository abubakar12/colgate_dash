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
import sqlalchemy
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
# import dask.dataframe as dd
# from pandarallel import pandarallel
from dash.exceptions import PreventUpdate
import dash
selected_chart_template='simple_white'
ai_green="#228779"
ai_gray="#bab0ac"
color="white"
import pyodbc
import dash_pivottable
from dash import Dash,dcc, html, Input, Output, callback,dash_table


df=pd.read_csv(r"D:\colgate_abubakar_dash\abc_segmentation.csv")
df=df.rename(columns={'SKU ':"SKU"})


###############################################Page 1##############################
segmentation_options=["xyz code","abc code"]
segmentation_measure_options=["actual_quantity","demand","actual_revenue"]
calculation_level_options=["product_id"]
periodicity=["daily","weekly","monthly","yearly"]
time_scope_options=["past","future","past&future"]
calculation_horizon=[1,2,3,4,5,6,7,8,9,10]
offset_for_calculation_horizon_options=[1,2,3,4,5,6,7,8,9,10]

###############################################Page 2##############################
calculation_strategy=["variation","aggregate_over_periods"]
calculation_method=["CV","CV_squared"]
segmentation_method=["pareto(sorted&accumulated%)","pareto(sorted&accumulated)",\
                     "No_of_items","threshhold"]
currency_to_id=["USD"]
unit_of_measure_to_id=[0,1,2,3,4,5,6,7,8,9,10]

######################################################################################

option_selected = dbc.Container(
    
    
    dbc.Row([     
                dbc.Row(dbc.Col(
                    html.Div([
                    html.H6("segmentation_options"),
                    dcc.Dropdown(
                    id='segmentation_options',
                    options=segmentation_options,
                    value=segmentation_options[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=6
                )),
                dbc.Row(dbc.Col(
                    html.Div([
                    html.H6("segmentation_measure_options"),
                    dcc.Dropdown(
                    id='segmentation_measure_options',
                    options=segmentation_measure_options,
                    value=segmentation_measure_options[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=6
                )),
                dbc.Row(dbc.Col(
                    html.Div([
                    html.H6("calculation_level_options"),
                    dcc.Dropdown(
                    id='calculation_level_options',
                    options=calculation_level_options,
                    value=calculation_level_options[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=6
                )),
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("periodicity"),
                        dcc.Dropdown(
                            id="periodicity",
                            options=periodicity,
                            value=periodicity[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=6
                )),
                
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("time_scope_options"),
                        dcc.Dropdown(
                            id="time_scope_options",
                            options=time_scope_options,
                            value=time_scope_options[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=6
                )),
                
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("calculation_horizon"),
                        dcc.Dropdown(
                            id="calculation_horizon",
                            options=calculation_horizon,
                            value=calculation_horizon[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=6
                )),
                
                
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("offset_for_calculation_horizon_options"),
                        dcc.Dropdown(
                            id="offset_for_calculation_horizon_options",
                            options=offset_for_calculation_horizon_options,
                            value=offset_for_calculation_horizon_options[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=6
                )),
            


        
        ]),
    

    
    
        
   
)

my_dict={"X":10,"Y":20,"Z":"not_max"}
dfs=pd.DataFrame(my_dict.items(),columns=["name","threshold"])

option_selected2 = dbc.Container(

    
    dbc.Row([     
                    dbc.Row(dbc.Col(
                        html.Div([
                        html.H6("calculation_strategy"),
                        dcc.Dropdown(
                        id='calculation_strategy',
                        options=calculation_strategy,
                        value=calculation_strategy[0]
                        ,style={"color":"#546e7a","font-weight": "bold"})
                        # md=6,
                        ],),md=6
                    )),
                    dbc.Row(dbc.Col(
                        html.Div([
                        html.H6("calculation_method"),
                        dcc.Dropdown(
                        id='calculation_method',
                        options=calculation_method,
                        value=calculation_method[0]
                        ,style={"color":"#546e7a","font-weight": "bold"})
                        # md=6,
                        ],),md=6
                    )),
                    dbc.Row(dbc.Col(
                        html.Div([
                        html.H6("segmentation_method"),
                        dcc.Dropdown(
                        id='segmentation_method',
                        options=segmentation_method,
                        value=segmentation_method[0]
                        ,style={"color":"#546e7a","font-weight": "bold"})
                        # md=6,
                        ],),md=6
                    )),
                    dbc.Row(dbc.Col(
                        html.Div([
                            html.H6("currency_to_id"),
                            dcc.Dropdown(
                                id="currency_to_id",
                                options=currency_to_id,
                                value=currency_to_id[0]
                                ,style={"color":"#546e7a","font-weight": "bold"}
                                
                            )
                        ]),md=6
                    )),
                    
                    dbc.Row(dbc.Col(
                        html.Div([
                            html.H6("unit_of_measure_to_id"),
                            dcc.Dropdown(
                                id="unit_of_measure_to_id",
                                options=unit_of_measure_to_id,
                                value=unit_of_measure_to_id[0]
                                ,style={"color":"#546e7a","font-weight": "bold"}
                                
                            )
                        ]),md=6
                    )),
                    
                    dbc.Row(dbc.Col(dbc.Button("Update Threshold Table",id="refresh_cfr_table",n_clicks=0,color="primary"),md=2)),
                    dbc.Row(dbc.Col(dash_table.DataTable(
                            dfs.to_dict('records'), [{"name": i, "id": i} for i in dfs.columns],
                            id='editable_pivottable',
                             
                            editable=True
                        )))

            ])
    
        
   
)
#################################################################################################################


# ])
# app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])
main_page_var = dbc.Container(
    [   dcc.Store(id='threshold_xyz',storage_type='memory'),
        dbc.Row(dbc.Col(html.H4("Colgate Table"))),
        html.Hr(),
        dbc.Row(dbc.Col(dcc.Markdown(id="text_xyz_setup",style={"white-space": "pre"}))),
        html.Hr(),
        option_selected,
        html.Hr(),
        dbc.Row(dbc.Col(dcc.Markdown(id="text2_xyz_setup",style={"white-space": "pre"}))),
        html.Hr(),
        option_selected2,
        html.Hr(),
    ]
)

# app.layout = main_page_var
@callback(
    Output("text_xyz_setup", "children"), 
    Input("segmentation_options","value"),
    Input("segmentation_measure_options", "value"),
    Input("calculation_level_options", "value"),
    Input('periodicity', 'value'),
    Input('time_scope_options', 'value'),
    Input('calculation_horizon', 'value'),
    Input('offset_for_calculation_horizon_options', 'value'),
    Input("threshold_xyz", "data"),prevent_initial_call=True
    )
def options1(segmentation_options,segmentation_measure_options,calculation_level_options,\
                  periodicity,time_scope_options,calculation_horizon,\
                      offset_for_calculation_horizon_options,threshold):


    threshold=pd.DataFrame(threshold)
    threshold=threshold.set_index("name")
    x=threshold.loc["X"]["threshold"]
    y=threshold.loc["Y"]["threshold"]
    z=threshold.loc["Z"]["threshold"]
    
    output="segmentation_options:**{}** --- segmentation_measure_options:**{}** --- calculation_level_options:**{}**\n \
        periodicity:**{}**--- time_scope_options:**{}**--- calculation_horizon:**{}**--- offset_for_calculation_horizon_options:**{}**\
           \n X:{}--Y:{}--Z:{}".format(segmentation_options,segmentation_measure_options,\
        calculation_level_options,periodicity,time_scope_options,calculation_horizon,\
            offset_for_calculation_horizon_options,x,y,z)
    return output



@callback(
    Output("text2_xyz_setup", "children"), 
    Input("calculation_strategy","value"),
    Input("calculation_method", "value"),
    Input("segmentation_method", "value"),
    Input('currency_to_id', 'value'),
    Input('unit_of_measure_to_id', 'value'),
    Input("threshold_xyz", "data"),prevent_initial_call=True
    )
def options2(calculation_strategy,calculation_method,segmentation_method,\
                  currency_to_id,unit_of_measure_to_id,threshold):

    threshold=pd.DataFrame(threshold)
    threshold=threshold.set_index("name")
    x=threshold.loc["X"]["threshold"]
    y=threshold.loc["Y"]["threshold"]
    z=threshold.loc["Z"]["threshold"]

    output="calculation_strategy:**{}** --- calculation_method:**{}** --- segmentation_method:**{}**\n \
        currency_to_id:**{}**--- unit_of_measure_to_id:**{}**---\n \
        X:{}--Y:{}--Z:{}".format(calculation_strategy,calculation_method,\
        segmentation_method,currency_to_id,unit_of_measure_to_id,x,y,z)
    return output


@callback(
    Output("threshold_xyz", "data"),
    Input("refresh_cfr_table", "n_clicks"),
    State('editable_pivottable','data')
    )
def edit_casefulfilment_table(refresh_table,pivot_data):
    df_copy=pivot_data
    df_copy=pd.DataFrame(df_copy)
    return df_copy.to_dict('records')


# server = app.server
# if __name__ == '__main__':
#     app.run_server(debug=True,port=3100)