import dash  
import dash_core_components as dcc 
import dash_html_components as html  
import dash_table 
import plotly.graph_objs as go 
import pandas as pd  
import numpy as np 
import os   

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

# GET DATA 
df = pd.read_csv('./data/longform.csv', index_col = 0)

app = dash.Dash(__name__)
server = app.server 

app.layout = html.Div(children=[
    dcc.Tabs(id="tabs-styled-with-inline", value='DATA1', 
    children=[
    # PAGE1
        dcc.Tab(label="DATA1", value='DATA1', style=tab_style, selected_style=tab_selected_style,
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
                ], style={'marginTop':'15%', 'textAlign': 'right', 
                })
            ]),
    #PAGE2
        dcc.Tab(label="DATA2", value='DATA2', style=tab_style, selected_style=tab_selected_style,
            children=[
                html.Div([
                    html.H3('自己紹介', style={'textAlign': 'Center', 'fontSize':'3rem','background': '#EEFFDD'}),
                    html.Div([
                    html.Img(src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190315/20190315143003.png" , style={'marginTop':'5%', 'marginLeft': '5%', 'display': 'inline-block', 'height': 500}),
                    html.Div([
                    html.H3('ひでやん'),
                    html.H3('@ogawahideyuki'),
                    html.H3('はんなりPythonの会、Crypto Kitchenのオーガナイザー'),
                    html.H3('合同会社 長目（ちょうもく）経営'),
                    html.H3('金融・データ・ブロックチェーンを扱う会社'),
                    html.H3('何事も全力でをモットーに')
                    ], style={'display': 'inline-block', 'fontSize': '2rem', 'marginLeft': '2%', 'color':'limegreen'})
                    ], style = {'background': '#EEFFDD'})
                ])
            ]),
    #PAGE3
        dcc.Tab(label="DATA3", value='DATA3', style=tab_style, selected_style=tab_selected_style,
            children=[
                html.H3('今日話すこと', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Div([
                    html.H3('１．データを見ることの重要性と問題点'),
                    html.H3('２．データをみんなで見るのにDash良いですよ'),
                    html.H3('３．じゃあそのDashってどうやって使うの？')
                ], style={'textAlign': 'Center', 'fontSize':'3rem', 'marginTop': '10%', 'background': '#EEFFDD', 'color':'limegreen'})
            ]),
    #PAGE4
        dcc.Tab(label="DATA4", value="DATA4", style=tab_style, selected_style=tab_selected_style,         children=[
                html.H3('データを見ることの重要性', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Img(src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190315/20190315175525.png",style={'width': '25%', 'margin': '0 5% 0'})
            ]),
    #PAGE5
        dcc.Tab(label="DATA5", value="DATA5", style=tab_style, selected_style=tab_selected_style,         children=[
                html.H3('データを見ることの重要性', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Div([
                        dash_table.DataTable(
                            id = 'table1',
                            columns = [{"name": i, "id": i} for i in df.columns],
                            data = df[:150].to_dict("rows")
                        )
                ], style={'marginLeft':"15%", 'marginRight': '15%'})
            ]),
    #PAGE6
        dcc.Tab(label="DATA6", value="DATA6", style=tab_style, selected_style=tab_selected_style,         children=[
                    html.Div([
                        html.H3('都道府県別人口とGDP,一人当たりGDP', style={
                        'textAlign': 'center', 'fontSize':'1.5rem', 'background': '#EEFFDD'
                        }),
                    html.Div([
                        dcc.Graph(id = 'scatter-chart',
                        hoverData = {'points': [{'customdata': '大阪府'}]},
                        ),
                    dcc.Slider(
                        id = 'slider-one',
                        min = df['year'].min(),
                        max = df['year'].max(),
                        marks = {i: '{}'.format(i) for i in range(int(df['year'].min()), int(df['year'].max())) if i % 2 == 1},
                        value = 1955,
                        )
                        ], style={
                            'display': 'inline-block',
                            'width': '60%',
                            }),
                    html.Div([
                        dcc.Graph(id='chart-one'),
                        dcc.Graph(id='chart-two'),
                        dcc.Graph(id='chart-three'),
                    ],style={
                        'display': 'inline-block',
                        'width': '39%'
                        })
                    ])
                ]),
    #PAGE7
        dcc.Tab(label="DATA7", value="DATA7", style=tab_style, selected_style=tab_selected_style,         children=[

            ]),
    #PAGE8
        dcc.Tab(label="DATA8", value="DATA8", style=tab_style, selected_style=tab_selected_style,         children=[

            ]),
    ], style=tabs_styles)
])

# Back To DATA4
@app.callback(
    dash.dependencies.Output('scatter-chart', 'figure'),
    [dash.dependencies.Input('slider-one', 'value')]
)
def update_graph(selected_year):
    dff = df[df['year'] == selected_year]
    dffper = dff[dff['item']=='pergdp']
    dffgdp = dff[dff['item']== 'GDP']
    dffpop = dff[dff['item']== 'popu']

    return {
        'data': [go.Scatter(
            x = dffper[dffper['area']==i]['value'],
            y = dffgdp[dffgdp['area']==i]['value'],
            mode = 'markers',
            customdata = [i],
            marker={
                'size' : dffpop[dffpop['area']==i]['value']/100,
                'color': dffpop[dffpop['area']==i]['value']/10000,
            }, 
            name=i,
        )for i in dff.area.unique()],
        'layout': {
            'height': 900,
            'xaxis': {
                'type': 'log',
                'title': '都道府県別一人当たりGDP(log scale)',
                'range':[np.log(80), np.log(1200)]
            },
            'yaxis': {
                'type':'log',
                'title': '都道府県別GDP(log scale)',
                'range':[np.log(80), np.log(8000)]
            },
            'hovermode': 'closest',
        }
    }

def create_smallChart(dff, area, name):
    return {
        'data':[go.Scatter(
            x = dff['year'],
            y = dff['value']
        )],
        'layout':{
            'height': 300,
            'title': '{}の{}データ'.format(area, name)
        }
    }



@app.callback(
    dash.dependencies.Output('chart-one', 'figure'),
    [(dash.dependencies.Input('scatter-chart', 'hoverData'))]
)
def createGDP(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'GDP']
    return create_smallChart(dff, areaName, 'GDP')

@app.callback(
    dash.dependencies.Output('chart-two', 'figure'),
    [(dash.dependencies.Input('scatter-chart', 'hoverData'))]
)
def createPerGDP(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'pergdp']
    return create_smallChart(dff, areaName, 'pergdp')

@app.callback(
    dash.dependencies.Output('chart-three', 'figure'),
    [(dash.dependencies.Input('scatter-chart', 'hoverData'))]
)
def createPopu(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'popu']
    return create_smallChart(dff, areaName, 'popu')


if __name__ == '__main__':
    app.run_server(debug=True)