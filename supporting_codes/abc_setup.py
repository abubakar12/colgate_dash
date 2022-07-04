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
segmentation_options_abc=["xyz code","abc code"]
segmentation_measure_options_abc=["actual_quantity","demand","actual_revenue"]
calculation_level_options_abc=["product_id"]
periodicity_abc=["daily","weekly","monthly","yearly"]
time_scope_options_abc=["past","future","past&future"]
calculation_horizon_abc=[1,2,3,4,5,6,7,8,9,10]
offset_for_calculation_horizon_abc=[1,2,3,4,5,6,7,8,9,10]

###############################################Page 2##############################

use_grouping_abc=["Yes","No"]
segmentation_method_abc=["pareto(sorted&accumulated%)","pareto(sorted&accumulated)",\
                     "No_of_items","threshhold"]
attributes_for_grouping_abc=["SKU","Brand","Category"]
currency_to_id_abc=["USD"]
unit_of_measure_to_id_abc=[0,1,2,3,4,5,6,7,8,9,10]

######################################################################################

option_selected = dbc.Container(
    
    
    dbc.Row([     
                dbc.Row(dbc.Col(
                    html.Div([
                    html.H6("segmentation_options_abc"),
                    dcc.Dropdown(
                    id='segmentation_options_abc',
                    options=segmentation_options_abc,
                    value=segmentation_options_abc[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=6
                )),
                dbc.Row(dbc.Col(
                    html.Div([
                    html.H6("segmentation_measure_options_abc"),
                    dcc.Dropdown(
                    id='segmentation_measure_options_abc',
                    options=segmentation_measure_options_abc,
                    value=segmentation_measure_options_abc[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=6
                )),
                dbc.Row(dbc.Col(
                    html.Div([
                    html.H6("calculation_level_options_abc"),
                    dcc.Dropdown(
                    id='calculation_level_options_abc',
                    options=calculation_level_options_abc,
                    value=calculation_level_options_abc[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=6,
                    ],),md=6
                )),
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("periodicity_abc"),
                        dcc.Dropdown(
                            id="periodicity_abc",
                            options=periodicity_abc,
                            value=periodicity_abc[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=6
                )),
                
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("time_scope_options_abc"),
                        dcc.Dropdown(
                            id="time_scope_options_abc",
                            options=time_scope_options_abc,
                            value=time_scope_options_abc[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=6
                )),
                
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("calculation_horizon_abc"),
                        dcc.Dropdown(
                            id="calculation_horizon_abc",
                            options=calculation_horizon_abc,
                            value=calculation_horizon_abc[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=6
                )),
                
                
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H6("offset_for_calculation_horizon_abc"),
                        dcc.Dropdown(
                            id="offset_for_calculation_horizon_abc",
                            options=offset_for_calculation_horizon_abc,
                            value=offset_for_calculation_horizon_abc[0]
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
                        html.H6("use_grouping_abc"),
                        dcc.Dropdown(
                        id='use_grouping_abc',
                        options=use_grouping_abc,
                        value=use_grouping_abc[0]
                        ,style={"color":"#546e7a","font-weight": "bold"})
                        # md=6,
                        ],),md=6
                    )),
                    dbc.Row(dbc.Col(
                        html.Div([
                        html.H6("attributes_for_grouping_abc"),
                        dcc.Dropdown(
                        id='attributes_for_grouping_abc',
                        options=attributes_for_grouping_abc,
                        value=attributes_for_grouping_abc[0]
                        ,style={"color":"#546e7a","font-weight": "bold"})
                        # md=6,
                        ],),md=6
                    )),
                    dbc.Row(dbc.Col(
                        html.Div([
                        html.H6("segmentation_method_abc"),
                        dcc.Dropdown(
                        id='segmentation_method_abc',
                        options=segmentation_method_abc,
                        value=segmentation_method_abc[0]
                        ,style={"color":"#546e7a","font-weight": "bold"})
                        # md=6,
                        ],),md=6
                    )),
                    dbc.Row(dbc.Col(
                        html.Div([
                            html.H6("currency_to_id_abc"),
                            dcc.Dropdown(
                                id="currency_to_id_abc",
                                options=currency_to_id_abc,
                                value=currency_to_id_abc[0]
                                ,style={"color":"#546e7a","font-weight": "bold"}
                                
                            )
                        ]),md=6
                    )),
                    
                    dbc.Row(dbc.Col(
                        html.Div([
                            html.H6("unit_of_measure_to_id_abc"),
                            dcc.Dropdown(
                                id="unit_of_measure_to_id_abc",
                                options=unit_of_measure_to_id_abc,
                                value=unit_of_measure_to_id_abc[0]
                                ,style={"color":"#546e7a","font-weight": "bold"}
                                
                            )
                        ]),md=6
                    )),
                    
                    dbc.Row(dbc.Col(dbc.Button("Update Threshold Table",id="refresh_cfr_table_abc",n_clicks=0,color="primary"),md=2)),
                    dbc.Row(dbc.Col(dash_table.DataTable(
                            dfs.to_dict('records'), [{"name": i, "id": i} for i in dfs.columns],
                            id='editable_pivottable_abc',
                             
                            editable=True
                        )))

            ])
    
        
   
)
#################################################################################################################


main_page_var = dbc.Container(
    [   dcc.Store(id='threshold_abc',storage_type='memory'),
        dbc.Row(dbc.Col(html.H4("Colgate Table"))),
        html.Hr(),
        dbc.Row(dbc.Col(dcc.Markdown(id="text_abc_setup",style={"white-space": "pre"}))),
        html.Hr(),
        option_selected,
        html.Hr(),
        dbc.Row(dbc.Col(dcc.Markdown(id="text2",style={"white-space": "pre"}))),
        html.Hr(),
        option_selected2,
        html.Hr(),
    ]
)

# app.layout = main_page_var
@callback(
    Output("text_abc_setup", "children"), 
    Input("segmentation_options_abc","value"),
    Input("segmentation_measure_options_abc", "value"),
    Input("calculation_level_options_abc", "value"),
    Input('periodicity_abc', 'value'),
    Input('time_scope_options_abc', 'value'),
    Input('calculation_horizon_abc', 'value'),
    Input('offset_for_calculation_horizon_abc', 'value'),
    Input("threshold_abc", "data"),prevent_initial_call=True
    )
def options1(segmentation_options_abc,segmentation_measure_options_abc,calculation_level_options_abc,\
                  periodicity_abc,time_scope_options_abc,calculation_horizon_abc,\
                      offset_for_calculation_horizon_abc,threshold):


    threshold=pd.DataFrame(threshold)
    threshold=threshold.set_index("name")
    x=threshold.loc["X"]["threshold"]
    y=threshold.loc["Y"]["threshold"]
    z=threshold.loc["Z"]["threshold"]
    
    output="segmentation_options_abc:**{}** --- segmentation_measure_options_abc:**{}** --- calculation_level_options_abc:**{}**\n \
        periodicity_abc:**{}**--- time_scope_options_abc:**{}**--- calculation_horizon_abc:**{}**--- offset_for_calculation_horizon_abc:**{}**\
           \n X:{}--Y:{}--Z:{}".format(segmentation_options_abc,segmentation_measure_options_abc,\
        calculation_level_options_abc,periodicity_abc,time_scope_options_abc,calculation_horizon_abc,\
            offset_for_calculation_horizon_abc,x,y,z)
    return output



@callback(
    Output("text2", "children"), 
    Input("use_grouping_abc","value"),
    Input("attributes_for_grouping_abc", "value"),
    Input("segmentation_method_abc", "value"),
    Input('currency_to_id_abc', 'value'),
    Input('unit_of_measure_to_id_abc', 'value'),
    Input("threshold_abc", "data"),prevent_initial_call=True
    )
def options2(use_grouping_abc,attributes_for_grouping_abc,segmentation_method_abc,\
                  currency_to_id_abc,unit_of_measure_to_id_abc,threshold):

    threshold=pd.DataFrame(threshold)
    threshold=threshold.set_index("name")
    x=threshold.loc["X"]["threshold"]
    y=threshold.loc["Y"]["threshold"]
    z=threshold.loc["Z"]["threshold"]

    output="use_grouping_abc:**{}** --- attributes_for_grouping_abc:**{}** --- segmentation_method_abc:**{}**\n \
        currency_to_id_abc:**{}**--- unit_of_measure_to_id_abc:**{}**---\n \
        X:{}--Y:{}--Z:{}".format(use_grouping_abc,attributes_for_grouping_abc,\
        segmentation_method_abc,currency_to_id_abc,unit_of_measure_to_id_abc,x,y,z)
    return output


@callback(
    Output("threshold_abc", "data"),
    Input("refresh_cfr_table_abc", "n_clicks"),
    State('editable_pivottable_abc','data')
    )
def edit_casefulfilment_table(refresh_table,pivot_data):
    df_copy=pivot_data
    df_copy=pd.DataFrame(df_copy)
    return df_copy.to_dict('records')


# server = app.server
# if __name__ == '__main__':
#     app.run_server(debug=True,port=3100)