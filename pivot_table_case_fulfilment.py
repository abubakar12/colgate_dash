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
import random

print()

df=pd.read_excel(r"D:\colgate_abubakar_dash\case_fullfilment_rate.xlsx")
df=df.rename(columns={'SKU ':"SKU"})
sku_options=df["SKU"].unique()
location_options=df["Location"].unique()
xyz_options=df["XYZ Code"].unique()
abc_options=df["ABC Code"].unique()

df=df[['SKU','Week', 'System Projections', 'Consensus Projections',
       'Actual Sales','Case Fullfilment Rate', 'Adjustment CFR', 'Location', 'ABC Code',
       'XYZ Code']]
option_selected = dbc.Container([
        dbc.Row(
            [        
                dbc.Col(
                    html.Div([
                    dcc.Store(id='cfr_file',storage_type='memory'),
                    html.H6("SKU"),
                    dcc.Dropdown(
                    id='sku',
                    options=sku_options,
                    value=sku_options[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=2,
                    ],),md=2
                ),
                dbc.Col(
                    html.Div([
                    html.H6("Location"),
                    dcc.Dropdown(
                    id='location',
                    options=location_options,
                    value=location_options[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=2,
                    ],),md=2
                ),
                
                

            ]
        ),


        
        ],
   
)

#################################################################################################################





dfs=pd.pivot_table(df,index=['SKU',"Location"],values='Adjustment CFR',columns=["Week"]).reset_index()
    
app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])
main_page_var = dbc.Container(
    [   
        html.H4("Colgate Table"),
        html.Hr(),
        html.H5(id="text"),
        html.Hr(),
        option_selected,
        html.Hr(),
        dbc.Row(dbc.Col((dcc.Graph(id="graph6")))),
        html.Hr(),
        dbc.Row([dbc.Col(id="pivot_table",md=6)]),
        html.Hr(),
        dbc.Row(dbc.Col(dbc.Button("Refresh CFR Table",id="refresh_cfr_table",n_clicks=0,color="primary"),md=2)),
        dbc.Row(dbc.Col(dash_table.DataTable(
                dfs.to_dict('records'), [{"name": i, "id": i} for i in dfs.columns],
                id='editable_pivottable',
                 
                editable=True
            )))
    ]
)

# dash_table.DataTable(df.to_dict("records"),id="editable_pivottable")

app.layout = main_page_var
@app.callback(
    Output("graph6", "figure"), 
    Output("text", "children"), 
    Output("pivot_table", "children"), 
    Input("sku", "value"),
    Input("location","value"),
    Input("cfr_file","data"),prevent_initial_call=True
    )
def new_customers(sku,location,df):
    df=pd.DataFrame(df)
    
    df_copy=df.copy()
    df_copy=df_copy[(df_copy["SKU"]==sku)&\
                (df_copy["Location"]==location)]
    
    
    
    cols=df.columns.tolist()
    new_df=pd.DataFrame([cols],columns=cols)
    data=pd.concat([new_df,df]).reset_index(drop=True)
    datas=data.values.tolist()
    pivot_table=dash_pivottable.PivotTable(
        id="%s" % datetime.datetime.now(),
        data=datas
        ,
        cols=["Week"],
        rows=['SKU',  'Location'],
        vals=['Adjustment CFR','System Projections',"System Projections","Actual Sales"]
          )
    
     
    fig = go.Figure()
    try:
        fig.add_trace(go.Bar(       x=df_copy["Week"],
                                    y=df_copy["System Projections"],
                                    name="System Projections",
                                    marker_color=ai_green
                                ))
        
        fig.add_trace(go.Bar(       x=df_copy["Week"],
                                    y=df_copy["Consensus Projections"],
                                    name="Consensus Projections",
                                    marker_color=ai_gray
                                ))
        
        fig.add_trace(go.Bar(       x=df_copy["Week"],
                                    y=df_copy["Actual Sales"],
                                    name="Actual Sales",
                                    marker_color="Blue"
                                ))
        
        # fig = px.histogram(df_melt, x="Week", y="dimension_value",color='dimensions', barmode='group',height=400)
    except:
        # fig = px.histogram(df_melt, x="Week", y="dimension_value",color='dimensions', barmode='group',height=400)
        fig.add_trace(go.Bar(       x=df_copy["Week"],
                                    y=df_copy["System Projections"],
                                    name="System Projections",
                                    marker_color=ai_green
                                ))
        
        fig.add_trace(go.Bar(       x=df_copy["Week"],
                                    y=df_copy["Consensus Projections"],
                                    name="Consensus Projections",
                                    marker_color=ai_gray
                                ))
        
        fig.add_trace(go.Bar(       x=df_copy["Week"],
                                    y=df_copy["Actual Sales"],
                                    name="Actual Sales",
                                    marker_color="Blue"
                                ))
        
    fig=fig.update_layout(template=selected_chart_template)
    # fig.update_traces(marker_color=ai_green)
    output="SKU : {}---location:{}".format(sku,location)
    return fig,output,pivot_table



@app.callback(
    Output("cfr_file", "data"),
    Input("refresh_cfr_table", "n_clicks"),
    State('editable_pivottable','data'),prevent_initial_call=True
    )
def edit_casefulfilment_table(refresh_table,pivot_data):
    df_copy=pivot_data
    df_copy=pd.DataFrame(df_copy)
    df_copy=pd.melt(df_copy,id_vars=["SKU","Location"],var_name="Week",value_name='Adjustment CFR')
    dfs=df.drop(["Week",'Adjustment CFR'],axis=1)
    df_copy=pd.merge(dfs,df_copy,on=["SKU","Location"],how="left")
    df_copy.to_csv(r"result.csv")
    return df_copy.to_dict('records')


server = app.server
if __name__ == '__main__':
    app.run_server(debug=True,port=3100)