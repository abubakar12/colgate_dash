from dash import Dash, dcc, html, Input, Output, callback
from pages import page1, page2


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page2'),
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    
    if pathname == '/page1':
        print("SSS")
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=False)