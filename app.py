import dash  
import dash_core_components as dcc 
import dash_html_components as html  
import plotly.graph_objs as go 
import pandas as pd  

# Tab CSS
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dcc.Tabs(id="tabs-styled-with-inline", value='tab1', 
    children=[
        dcc.Tab(label="tab1", value='tab1', style=tab_style, selected_style=tab_selected_style,
            children=[
                html.Div([
                html.H1('The Power Of Data Visualization', 
                style={'marginTop': '10%',  'fontFamily': 'Arial Bold', 'textAlign': 'Center', 'fontSize': '4rem','color': 'limegreen'}),
                html.H1('With Dash!', style={'textAlign':'Center', 'fontFamily': 'Arial Bold', 'textAlign': 'Center', 'fontSize': '4rem','color': 'limegreen'})
                ],style = {'background': '#EEFFDD'}
                ),
                html.Div([
                    html.H1('20190324 可視化特集会', style= {'marginRight': '2%',}),
                    html.H1('合同会社 長目　CEO  小川　英幸', style={'marginRight': '2%', })
                ], style={'marginTop':'15%', 'textAlign': 'right', 'color': 'green'})
            ]),
        dcc.Tab(label="tab2", value='tab2', style=tab_style, selected_style=tab_selected_style,
            children=[

            ]),
        dcc.Tab(label="tab3", value='tab3', style=tab_style, selected_style=tab_selected_style,
            children=[

            ]),
    ], style=tabs_styles)
])

if __name__ == '__main__':
    app.run_server(debug=True)