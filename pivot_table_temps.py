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
sku_options=df["SKU"].unique()
location_options=df["Location"].unique()
xyz_options=df["XYZ Code"].unique()
abc_options=df["ABC Code"].unique()
option_selected = dbc.Container([
        dbc.Row(
            [        
                dbc.Col(
                    html.Div([
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
                dbc.Col(
                    html.Div([
                    html.H6("ABC-Data"),
                    dcc.Dropdown(
                    id='abc-code',
                    options=abc_options,
                    value=abc_options[0]
                    ,style={"color":"#546e7a","font-weight": "bold"})
                    # md=2,
                    ],),md=2
                ),
                dbc.Col(
                    html.Div([
                        html.H6("XYZ-Data"),
                        dcc.Dropdown(
                            id="xyz-code",
                            options=xyz_options,
                            value=xyz_options[0]
                            ,style={"color":"#546e7a","font-weight": "bold"}
                            
                        )
                    ]),md=2
                ),

            ]
        ),


        
        ],
   
)

#################################################################################################################





#Average_selling_price.py
# layout1 = html.Div([
#     dcc.Graph(id="graph6")

# ])
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
        html.Div(id="pivot_table")
    ]
)


app.layout = main_page_var
@app.callback(
    Output("graph6", "figure"), 
    Output("text", "children"), 
    Output("pivot_table", "children"), 
    Input("sku", "value"),
    Input("location","value"),
    Input('abc-code', 'value'),
    Input('xyz-code', 'value')
    )
def new_customers(sku,location,abc_code,xyz_code):
    df_copy=df.copy()
   
    df_copy=df_copy[(df_copy["SKU"]==sku)&\
                (df_copy["Location"]==location)&\
                  (df_copy["ABC Code"]==abc_code)&\
                  (df_copy["XYZ Code"]==xyz_code)]
    
    
     
    # res=pd.pivot_table(df,index=["SKU","Location","ABC Code","XYZ Code"],columns="Week",\
    #                     values=["Actuals QTY"]).reset_index()
    # df_copy=df_copy[(df_copy["SKU"]==sku)]
    cols=df.columns.tolist()
    new_df=pd.DataFrame([cols],columns=cols)
    data=pd.concat([new_df,df]).reset_index(drop=True)
    data=data.values.tolist()
    pivot_table=dash_pivottable.PivotTable(
        data=data
        ,
        cols=["Week"],
        rows=['SKU',  'Location','ABC Code','XYZ Code'],
        vals=['Actuals QTY']
          )
       
    
    df_copy=df_copy.groupby(["Week"])['Actuals QTY ADJ'].sum().reset_index()
    df_copy.to_csv(r"result.csv",index=False)
    try:
        fig = px.bar(df_copy, y='Actuals QTY ADJ', x="Week",title='new_customers')
    except:
        fig = px.bar(df_copy, y='Actuals QTY ADJ', x="Week",title='new_customers')
    fig=fig.update_layout(template=selected_chart_template)
    fig.update_traces(marker_color=ai_green)
    output="SKU : {}---location:{}---abc-code:{}---xyz-code:{}".format(sku,location,abc_code,xyz_code)
    return fig,output,pivot_table





server = app.server
if __name__ == '__main__':
    app.run_server(debug=True,port=3100)