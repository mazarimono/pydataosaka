import dash  
import dash_core_components as dcc 
import dash_html_components as html  
import dash_table 
import dash_cytoscape as cyto  
import plotly.graph_objs as go 
import pandas as pd  
import numpy as np 
from datetime import datetime   
from datetime import timedelta
import os   
import json 

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

# Color
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# GET DATA 
df = pd.read_csv('./data/longform2.csv', index_col = 0)
dflong = df.iloc[:15, :]

dfhokkaido = df[df['area']=='北海道']
dfpergdp = df[df.item=='pergdp']

dftable = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
dfcons = pd.read_csv('./data/jp_consumer2014.csv', index_col=0)
dfcons = dfcons.iloc[:10, :20]

dfkyoto = pd.read_csv('./data/kyoto_hotel_comp1.csv', index_col=0)
mapbox_access_token = "pk.eyJ1IjoibWF6YXJpbW9ubyIsImEiOiJjanA5Y3IxaWsxeGtmM3dweDh5bjgydGFxIn0.3vrfsqZ_kGPGhi4_npruGg"

dfjpy = pd.read_csv('https://raw.githubusercontent.com/plotly/dash-web-trader/master/pairs/USDJPY.csv', index_col=1, parse_dates=['Date'])
dffjpy = dfjpy['2016/1/5']
dffjpy = dffjpy.resample('1S').last().bfill()

# cytoscape用データ   
nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20*lat, 'y': -20*long}
    }
    for short, label, long, lat in (
        ('la', 'Los Angeles', 34.03, -118.25),
        ('nyc', 'New York', 40.71, -74),
        ('to', 'Toronto', 43.65, -79.38),
        ('mtl', 'Montreal', 45.50, -73.57),
        ('van', 'Vancouver', 49.28, -123.12),
        ('chi', 'Chicago', 41.88, -87.63),
        ('bos', 'Boston', 42.36, -71.06),
        ('hou', 'Houston', 29.76, -95.37)
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

elements = nodes + edges

dfmany = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

available_indicators = dfmany['Indicator Name'].unique()

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
                    html.H1('20190405 大阪Pythonの会', style= {'marginRight': '2%',}),
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
                html.H3('データって何？', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Div([
                html.Img(src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190315/20190315175525.png",style={'width': '25%', 'margin': '0 5% 0', 'display': 'inline'}),
                html.Div([
                html.H3('最近話題のこの本'),
                html.H3('事実に基づき世界を見る！'),
                html.H3('データを基に世界を正しく見る'),
                html.H3('データ == 事実')
                ], style={'display': 'inline-block', 'fontSize': '3rem', 'color': 'limegreen'}),
                ], style={'background': '#EEFFDD'}),
            ]),
    #PAGE5
        dcc.Tab(label="DATA5", value="DATA5", style=tab_style, selected_style=tab_selected_style,         children=[
                html.H3('データを見る?', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Div([
                        dash_table.DataTable(
                            id = 'table1',
                            columns = [{"name": i, "id": i} for i in df.columns],
                            data = df[:500].to_dict("rows"),
                            sorting = True,

                        )
                ], style={'marginLeft':"15%", 'marginRight': '15%'})
            ]),
    #PAGE6
        dcc.Tab(label="DATA6", value="DATA6", style=tab_style, selected_style=tab_selected_style,         children=[
                html.Div([
                    html.H3('都道府県別一人当たりGDP')
                ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD'}),
                html.Div([
                dcc.Graph(
                    id='pergdpGraph',
                    figure={
                    'data': [
                        go.Scatter(
                            x = dfpergdp[dfpergdp['area'] == i]['year'],
                            y = dfpergdp[dfpergdp['area'] == i]['value'],
                            name = i,
                            mode = 'lines'
                        ) for i in dfpergdp.area.unique()
                    ],
                    'layout':go.Layout(
                        xaxis= {'title': '年度'},
                        yaxis= {'title': '一人当たりGDP'},
                        height = 700,
                    )
                }
                )
                ], style ={'height': '80%', 'background': '#EEFFDD'}), 
            ]),
    #PAGE7
        dcc.Tab(label="DATA7", value="DATA7", style=tab_style, selected_style=tab_selected_style,         children=[
                html.Div([
                    html.H3('データを情報化するときの問題点', style={'textAlign': 'center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                    html.Div([
                        html.H4('大量にデータがあっても見せれない(特にプレゼン)'),
                        html.H4('多くの意見を反映しにくい'),
                        html.H4('凄い発見も当たり前かのように見えてしまう'),

                    ], style = {'textAlign': 'Center', 'fontSize': '3rem', 'background': '#EEFFDD',
                    'color': 'limegreen', 'padding': '1%'})
                ])
            ]),
    #PAGE8
        dcc.Tab(label="DATA8", value="DATA8", style=tab_style, selected_style=tab_selected_style,         children=[
                    html.H1('出来るよ！Dashなら！！', style={'textAlign': 'Center', 'fontSize': '3rem','marginTop': '15%', 'padding': '5%','background': '#EEFFDD', 'color': 'limegreen'})
            ]),
    #PAGE9
        dcc.Tab(label="DATA9", value="DATA9", style=tab_style, selected_style=tab_selected_style,         children=[
                    html.Div([
                        html.H3('都道府県別人口とGDP,一人当たりGDP', style={
                        'textAlign': 'center', 'fontSize':'2.5rem', 'background': '#EEFFDD'
                        }),
                    html.Div([
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
                    ], style={'background': '#EEFFDD', 'padding':'1%'}),
                    ])
                ]),
    #PAGE10
        dcc.Tab(label="DATA10", value="DATA10", style=tab_style, selected_style=tab_selected_style,         children=[
                html.Div([
                    html.Div([

                    html.H3('Dashの使い方(1)', style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                    ]),
                    html.Div([
                        html.H3('DashはFlask, React, Plotlyで作られたフレームワーク'),
                        html.H3('Pythonで使える。グラフ部分はPlotly。'),
                        html.H3('グラフ部分がインタラクティブに作れる'),
                        html.H3('ドキュメント　https://dash.plot.ly/')
                    ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 10, 'color': 'limegreen', 'marginTop': '5%'}),
                #グラフ１
                    html.Div([
                        html.H3('Dashグラフ基本形', style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                    ]),
                    html.Div([
                        html.H1(children='Hello Dash'),

                        html.Div(children='''
                                    Dash: A web application framework for Python.
                                '''),

                        dcc.Graph(
                            id='example-graph',
                            figure={
                            'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                            ],
                            'layout': {
                            'title': 'Dash Data Visualization'
                            }
                            }
                            )
                    ], style={'padding': '2%', 'width': '50%', 'margin': '0 auto 0'}),

                    html.Div([
                        dcc.Markdown('''
                        
                        下のようなコードで簡単にグラフを作ることができます。
                        マウスホバーで何を出すかを指定しなくても、legendを出せとも
                        書かなくても表示してくれています。
                        

                        import dash
                        import dash_core_components as dcc
                        import dash_html_components as html

                        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

                        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

                        app.layout = html.Div(children=[
                            html.H1(children='Hello Dash'),

                        html.Div([
                        html.P('Dash: A web application framework for Python.')
                        ]),

                        dcc.Graph(
                        id='example-graph',
                        figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                            ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                            }})
                        ])

                        if __name__ == '__main__':
                            app.run_server(debug=True)
                             
                             
                        また、html要素にスタイルを適用することにより、文字色、表示位置を変える
                        なんてことも簡単にできます。

                        ''')
                    ], style = {'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 10,}
                    ),
                #グラフ2
                    html.Div([
                        html.H3('グラフにスタイルを加える', style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                    ]),
                    html.Div([
                        html.Div(children=[
                    html.H1(
                        children='Hello Dash',
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                            }
                        ),

                    html.Div(children='Dash: A web application framework for Python.', style={
                        'textAlign': 'center',
                        'color': colors['text']
                        }),

                    dcc.Graph(
                        id='example-graph-2',
                        figure={
                            'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                            ],
                            'layout': {
                                'plot_bgcolor': colors['background'],
                                'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                                }
                            }
                        }
                    )
                        ], style = {'backgroundColor': colors['background'], 'padding': 10, 'width': '50%', 'margin': '0 auto 0', })
                        ], style={'padding': 10}),
                # 解説
                    html.Div([
                        dcc.Markdown('''
                        またもコード

                        import dash
                        import dash_core_components as dcc
                        import dash_html_components as html

                        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

                        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
                        
                        # 追加
                        colors = {
                            'background': '#111111',
                            'text': '#7FDBFF'
                            }

                        app.layout = html.Div(style={'backgroundColor': colors['background'] # 追加}, children=[
                            html.H1(
                                children='Hello Dash',
                                style={
                                    'textAlign': 'center',
                                    'color': colors['text'] # 追加
                                    }
                                ),

                        html.Div(children='Dash: A web application framework for Python.', style={
                            'textAlign': 'center',
                            'color': colors['text']
                                }), # 追加

                        dcc.Graph(
                            id='example-graph-2',
                            figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                            # 追加
                            'layout': {
                                'plot_bgcolor': colors['background'],
                                'paper_bgcolor': colors['background'],
                                'font': {
                                    'color': colors['text']
                                        }
                                    }
                                }
                            )
                        ])

                        if __name__ == '__main__':
                            app.run_server(debug=True)
                        ''')
                    ], style = {'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 20, 'marginTop': '5%'}),
                # show table
                    html.Div([
                        html.H3('テーブルデータも簡単に見せられる！', style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                    ]),
                    html.Div([
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in dftable.columns],
                            data=dftable.to_dict("rows"),
                            sorting= True,
                            )
                        ], style={'padding': '5%', 'width': '50%', 'margin': '0 auto 0'}),
                # comment table
                    html.Div([
                        dcc.Markdown('''
                            テーブルデータのソートも簡単につけられる。
                            
                            import dash
                            import dash_table
                            import pandas as pd

                            df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

                            app = dash.Dash(__name__)

                            app.layout = dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict("rows"),
                                sorting= True,
                                )

                            if __name__ == '__main__':
                                app.run_server(debug=True)

                        ''')
                    ], style = {'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 20,}),
                #まとめ１
                    html.Div([
                        html.Div([
                            html.H3('使い方　ちょっとまとめ')
                        ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '10%'}),
                        html.Div([
                        html.H3('app = Dash(__name__) で入れ物作り！'),
                        html.H3('app.layout = html.Div()で中身を詰める！'),
                        html.H3('dash_html_componentsでhtml要素を触る！'),
                        html.H3('dash_core_componentsでグラフとかツールを触る！'),
                        html.H3('dash_tableでデータをテーブルでみられる！'),
                        html.H3('何故かdccだがmarkdownが使える！'),
                    ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 50, 'color': 'limegreen', 'marginTop': '10%'})
                    ])
                ])           
            ]),
    #PAGE11
        dcc.Tab(label="DATA11", value="DATA11", style=tab_style, selected_style=tab_selected_style,         children=[
                html.Div([
                    html.Div([
                        html.H3('Dashの使い方（２）')
                    ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                #データの形のお話
                    html.Div([
                        html.Div([
                            html.H3('その前に、ちょっとデータの形の話')
                        ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%', 'color': 'skyblue'}),
                        html.Div([
                            html.H3('よく見るデータの形 Wide Form Data', style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%', 'color': 'limegreen'}),
                            html.Div([
                            dash_table.DataTable(
                                id='wide-form-table',
                                columns = [{'name': i, 'id': i} for i in dfcons.columns],
                                data = dfcons.to_dict("rows"),
                                sorting = True,
                            )
                            ], style = {'width': '80%', 'margin': '0 auto 0'}),
                        html.Div([
                            html.H3('可視化に使うデータの形 Long Form Data', style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'marginTop': '5%', 'color': 'limegreen'}),
                            html.Div([
                                dash_table.DataTable(
                                    id = 'long-form-table',
                                    columns = [{'name': i, 'id': i} for i in dflong.columns],
                                    data = dflong.to_dict('rows'),
                                    sorting = True
                                )
                            ], style = {'width': '30%', 'margin': '0 auto 0'})
                        ]),
                        ])
                    ]),
                # コールバックの話
                    html.Div([
                        html.Div([
                            html.H3('Dashで最も重要なCallbackのお話')
                        ], style = {'textAlign': 'Center', 'fontSize': '4rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                        html.Div([
                            dcc.Markdown('''
                                Dashをインタラクティブにするのに
                                超重要なのがCallback！！！
                                逆にこれを使わないと、普通のライブラリ
                                を使っているのと同じといって、
                                も良いと思える！！！

                                ので、フォントサイズをここまでで
                                一番大きくしました！
                            ''')
                        ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
                # first callback
                        html.Div([
                            html.Div(
                                html.H1('北海道のGDP、人口、一人あたりGDPの推移',
                                    style = {'textAlign': 'center'})
                                        ),
                            dcc.Dropdown(
                                id = 'dropdown-for-hokkaido',
                                options = [{'label': i, 'value': i} for i in dfhokkaido.item.unique()],
                                value = 'GDP'
                                , style={'width': '40%', 'margin': '0 auto 0'}),
                            dcc.Graph(
                                id="hokkaidoGraph",
                                style = {'width': '70%', 'margin': '0 auto 0'}
                                )
                                ]),
                # comment to callback
                        html.Div([
                            dcc.Markdown('''
                                このグラフのコードは以下のような感じになっています。

                                import dash  
                                import dash_core_components as dcc   
                                import dash_html_components as html
                                import plotly.graph_objs as go  
                                import pandas as pd 

                                # ①データ読み込み
                                df = pd.read_csv('./data/longform.csv', index_col=0)
                                dfhokkaido = df[df['area']=='北海道']

                                app = dash.Dash(__name__)

                                # ②表示作成
                                app.layout = html.Div(children=[
                                    html.Div(
                                        html.H1('北海道のGDP、人口、一人あたりGDPの推移',
                                        style = {'textAlign': 'center'})
                                        ),
                                    dcc.Dropdown(
                                        id = 'dropdown-for-hokkaido',
                                        options = [{'label': i, 'value': i} for i in dfhokkaido.item.unique()],
                                        value = 'GDP',
                                        style={'width': '40%', 'margin': '0 auto 0'}
                                        ),
                                    dcc.Graph(
                                        id="hokkaidoGraph",
                                        style = {'width': '70%', 'margin': '0 auto 0'}
                                            )
                                        ])

                                    # ③コールバック作成
                                    @app.callback(
                                        dash.dependencies.Output('hokkaidoGraph', 'figure'),
                                        [dash.dependencies.Input('dropdown-for-hokkaido', 'value')]
                                        )
                                    def update_graph(factor):
                                        dff = dfhokkaido[dfhokkaido['item'] == factor]

                                        return {
                                            'data': [go.Scatter(
                                                x = dff['year'],
                                                y = dff['value']
                                                )]
                                            }

                                    if __name__ == '__main__':
                                        app.run_server(debug=True)

                                    
                                    30行ほどでこんなに複雑な処理ができてしまいます！！
                                    他だったら、グラフ処理でこれくらい必要かと。

                                    ドロップダウンなど要素選択のツールはたくさんあります。
                                    https://dash.plot.ly/dash-core-components
                            ''')
                        ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
                    #マウスアクション活用
                        html.Div([
                            html.Div([
                                html.H3('マウスアクションを活用する')
                            ], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                            html.Div([
                                html.Div(
                                    html.H1('北海道のGDP、人口、一人あたりGDPの推移',
                                    style = {'textAlign': 'center'})
                                        ),
                            # 付け足し①
                            html.Div(
                                html.H1(id='add-hover-data')
                                    ),
                            dcc.RadioItems(
                                id = 'dropdown-for-hokkaido1',
                                options = [{'label': i, 'value': i} for i in dfhokkaido.item.unique()],
                                value = 'GDP'
                                ),
                            dcc.Graph(
                                id="hokkaidoGraph1",
                                )
                                ], style={'width': '75%', 'margin': '0 auto 0', 'padding': '3%'})
                                ]),
                            html.Div([
                                dcc.Markdown('''
                                    コードを見てみましょう

                                    import dash  
                                    import dash_core_components as dcc   
                                    import dash_html_components as html
                                    import plotly.graph_objs as go  
                                    import pandas as pd 
                                    import json 

                                    df = pd.read_csv('./data/longform.csv', index_col=0)
                                    dfhokkaido = df[df['area']=='北海道']

                                    app = dash.Dash(__name__)

                                    app.layout = html.Div(children=[
                                        html.Div(
                                            html.H1('北海道のGDP、人口、一人あたりGDPの推移',
                                            style = {'textAlign': 'center'})
                                                ),
                                    # 付け足し①
                                    html.Div(
                                        html.H1(id='add-hover-data')
                                        ),
                                        dcc.RadioItems(
                                            id = 'dropdown-for-hokkaido',
                                            options = [{'label': i, 'value': i} for i in dfhokkaido.item.unique()],
                                            value = 'GDP'
                                            ),
                                        dcc.Graph(
                                            id="hokkaidoGraph",
                                            )
                                        ])

                                    @app.callback(
                                        dash.dependencies.Output('hokkaidoGraph', 'figure'),
                                        [dash.dependencies.Input('dropdown-for-hokkaido', 'value')]
                                        )
                                    def update_graph(factor):
                                        dff = dfhokkaido[dfhokkaido['item'] == factor]

                                        return {
                                            'data': [go.Scatter(
                                                x = dff['year'],
                                                y = dff['value']
                                                )]
                                            }

                                    # 付けたし②
                                    @app.callback(
                                        dash.dependencies.Output('add-hover-data', 'children'),
                                        [dash.dependencies.Input('hokkaidoGraph', 'hoverData')]
                                        )
                                    def return_hoverdata(hoverData):
                                        return json.dumps(hoverData)


                                    if __name__ == '__main__':
                                        app.run_server(debug=True)
                                    
                                    先ほどのグラフをちょっと変更して、
                                    マウスホバーで得られるデータを表示するようにしました。

                                    付け足し1でh1要素を追加して、ここに
                                    マウスホバーの情報を返すようになっています。

                                    付け足し２でグラフ上で得られたデータを返す
                                    処理を行っています。といっても、
                                    json.dumps()で取得データを返すだけです。


                                ''')
                                ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
                            # バブルグラフ
                            html.Div([
                                html.Div([
                    html.Div([
                        dcc.Graph(id = 'scatter-chart1',
                        hoverData = {'points': [{'customdata': '大阪府'}]},
                        ),
                    dcc.Slider(
                        id = 'slider-one1',
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
                        dcc.Graph(id='chart-one1'),
                        dcc.Graph(id='chart-two1'),
                        dcc.Graph(id='chart-three1'),
                    ],style={
                        'display': 'inline-block',
                        'width': '39%'
                        })
                    ], style={'padding':'1%'}),
                            ]),
                html.Div([
                    dcc.Markdown('''
                        ツールとマウスホバーを使った合わせ技で
                        上のようなものができます。

                        グラフの下にあるスライダーで
                        表示する年度を変更しながら、
                        グラフ上の都道府県をホバーすると、
                        ホバーした都道府県のヒストリカルなデータが
                        みられます！
                        
                        import pandas as pd 
                        import numpy as np   
                        import dash  
                        import dash_core_components as dcc 
                        import dash_html_components as html  
                        import plotly.graph_objs as go 
                        import json 

                        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

                        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

                        df = pd.read_csv('./data/longform.csv', index_col = 0)

                        app.layout = html.Div([
                            html.Div([
                                html.H3('都道府県別人口とGDP,一人当たりGDP', style={
                                        'textAlign': 'center'
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
                                ])

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
                            dff　= df[df['area']==areaName]
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

                        if __name__=="__main__":
                            app.run_server(debug=True)

                    ''')
                ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
            html.Div([
                html.Div([
                    html.H3(['マップもいける！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                ]),
                dcc.Graph(
                    id = 'kyoto-hotels',
                    figure = {
                        'data':[
                        go.Scattermapbox(
                        lat = dfkyoto[dfkyoto['age']== i]['ido'],
                        lon = dfkyoto[dfkyoto['age']== i]['keido'],
                        mode = 'markers',
                        marker = dict(
                        size=9
                        ),
                        text = dfkyoto[dfkyoto['age']== i]['hotel_name'],
                        name = str(i),
                        ) for i in dfkyoto['age'].unique()
                        ],
                        'layout':
                        go.Layout(
                            autosize=True,
                            hovermode='closest',
                            mapbox = dict(
                            accesstoken=mapbox_access_token,
                            bearing = 0,
                            center = dict(
                            lat=np.mean(dfkyoto['ido']),
                            lon=np.mean(dfkyoto['keido'])
                        ),
                        pitch = 90,
                        zoom=10,
                    ),
                    height=600
                        )
                    }
                    )
                    ]),
                    html.Div([
                        dcc.Markdown('''
                        今回の利用例の場合、経度緯度のデータが
                        あれば簡単にできる！

                        df = pd.read_csv('mapdadta.csv', index_col=0)
                        app = dash.Dash(__name__)
                        app.layout = html.Div([dcc.Graph(
                        id = 'kyoto-hotels',
                        figure = {
                            'data':[
                                go.Scattermapbox(
                                lat = df[df['age']== i]['ido'],
                                lon = df[df['age']== i]['keido'],
                                mode = 'markers',
                                marker = dict(
                                    size=9
                                ),
                                text = df[df['age']== i]['hotel_name'],
                                name = str(i),
                                ) for i in df['age'].unique()
                                ],
                            'layout':
                                go.Layout(
                                    autosize=True,
                                    hovermode='closest',
                                    mapbox = dict(
                                        accesstoken=mapbox_access_token,
                                        bearing = 0,
                                        center = dict(
                                            lat=np.mean(df['ido']),
                                            lon=np.mean(df['keido'])
                                            ),
                                        pitch = 90,
                                        zoom=10,
                                        ),
                                    height=600
                                        )
                                            }
                                        )])])
                                
                        '''
                        )
                    ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
                    html.Div([
                        html.Div([
                        html.H3(['Webにあげるのも簡単！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                        ]),
                        html.Div([
                            dcc.Markdown([
                                '''
                                VPSにあげる方法とかはちょっとわからないが、
                                herokuにあげるの簡単！

                                app.pyファイルにコードを
                                import os

                                server = app.server

                                ファイルを付け加える
                                Procfile
                                web: gunicorn app:server
                                
                                requirements.txt

                                $ heroku create osaka　# ヘロクのアドレスを取る　https://osaka.herokuapp.com
                                $ git add .
                                $ git commit -u 'hogehoge'　
                                $ git push heroku master    # ヘロクにプッシュ
                                $ heroku ps: scale web:1  # 無料のヘロクで動かす 

                                '''
                            ]),
                        ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
                    ]),
                                ])
                                ])
                            ]),
    #PAGE12
        dcc.Tab(label="DATA12", value="DATA12", style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                        html.H3('Dash使い方（３）')
                    ], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
            html.Div([
                html.Div([
                    html.H3(['ライブアップデートもいける！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                ]),
                html.Div([
                    dcc.Graph(id="usdjpy"),
                    dcc.Interval(
                        id = 'interval_components',
                        interval = 1000,
                        )
                ], style={'height': '30%', 'width': '80%', 'margin': '0 auto 0', 'textAlign': 'center'}),
                ]),
            html.Div([
                html.Div([
                            dcc.Markdown([
                                '''
                                リアルタイムで更新する際には
                                dash_core_componentsのIntervalを使う。

                                Interbalではid, iterval(更新時間　ミリ秒)を設定し、
                                コールバックでその設定時間ごとにグラフを返すようにしている。

                                ここでは一日分のドル円の価格データを取り、それを
                                リアルタイムの時間に合わせて動かしている。
                                

                                [Intervalのgithub](https://github.com/plotly/dash-core-components/blob/master/dash_core_components/Interval.py)
                            
                                import dash  
                                import dash_core_components as dcc  
                                import dash_html_components as html 
                                from datetime import datetime   
                                from datetime import timedelta
                                import pandas as pd  
                                import plotly.graph_objs as go 

                                df = pd.read_csv('https://raw.githubusercontent.com/plotly/dash-web-trader/master/pairs/USDJPY.csv', 
                                index_col=1, parse_dates=['Date'])
                                dff = df['2016/1/5']
                                dff = dff.resample('1S').last().bfill()

                                app = dash.Dash(__name__)

                                app.layout = html.Div([
                                html.Div([
                                    dcc.Graph(id="usdjpy"),
                                    dcc.Interval(
                                        id = 'interval_components',
                                        interval = 1000,

                                        )
                                    ], style={'height': '30%', 'width': '80%', 'margin': '0 auto 0', 'textAlign': 'center'})
                                    ])


                                @app.callback(
                                    dash.dependencies.Output('usdjpy', 'figure'),
                                    [dash.dependencies.Input('interval_components', 'n_intervals')]
                                    )
                                def update_graph(n):
                                    t = datetime.now()
                                    nowHour = t.hour
                                    nowMinute = t.minute 
                                    nowSecond = t.second 

                                    d = datetime(2016, 1, 5, nowHour+9, nowMinute, nowSecond)
                                    period = timedelta(seconds = 120)
                                    d1 = d - period 
                                    dff1 = dff.loc['{}'.format(d1): '{}'.format(d), :]

                                    return {
                                        'data': [go.Scatter(
                                                x = dff1.index,
                                                y = dff1['Bid']
                                            )],
                                        'layout':{
                                            'height': 600,
                                            'title': 'USD-JPY 1Second Charts'
                                        }
                                    }

                                if __name__=='__main__':
                                    app.run_server(debug=True)

                                '''
                            ]),
                        ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
            ]),
            html.Div([
                html.Div([
                    html.H3(['グラフもいける！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                ]),
                html.Div([
                        dcc.Dropdown(
                            id='dropdown-update-layout',
                            value='grid',
                            clearable=False,
                            options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                            ], style={'width': '30%', 'margin':'0 auto 0'}
                        ),
                        cyto.Cytoscape(
                            id='cytoscape-update-layout',
                            layout={'name': 'grid'},
                            style={'width': '80%', 'height': '700px', 'margin': '0 auto 0', 'padding': '5%'},
                            elements=elements
                            )
                        ]),
                    ]),
                html.Div([
                    dcc.Markdown([
                        '''
                        グラフカッコ良いですね。
                        どういうのに使うか模索中ですけど。
                        現時点では有向には出来ない模様です。

                        Dash Cytoscape解説ページ
                        https://dash.plot.ly/cytoscape
                        
                        import dash
                        import dash_cytoscape as cyto
                        import dash_html_components as html
                        import dash_core_components as dcc
                        from dash.dependencies import Input, Output

                        app = dash.Dash(__name__)


                        nodes = [
                            {
                            'data': {'id': short, 'label': label},
                            'position': {'x': 20*lat, 'y': -20*long}
                                    }
                        for short, label, long, lat in (
                                ('la', 'Los Angeles', 34.03, -118.25),
                                ('nyc', 'New York', 40.71, -74),
                                ('to', 'Toronto', 43.65, -79.38),
                                ('mtl', 'Montreal', 45.50, -73.57),
                                ('van', 'Vancouver', 49.28, -123.12),
                                ('chi', 'Chicago', 41.88, -87.63),
                                ('bos', 'Boston', 42.36, -71.06),
                                ('hou', 'Houston', 29.76, -95.37)
                                )
                                ]

                        edges = [
                            {'data': {'source': source, 'target': target}}
                            for source, target in (
                                ('van', 'la'),
                                ('la', 'chi'),
                                ('hou', 'chi'),
                                ('to', 'mtl'),
                                ('mtl', 'bos'),
                                ('nyc', 'bos'),
                                ('to', 'hou'),
                                ('to', 'nyc'),
                                ('la', 'nyc'),
                                ('nyc', 'bos')
                                )
                            ]

                        elements = nodes + edges


                        app.layout = html.Div([
                            dcc.Dropdown(
                                id='dropdown-update-layout',
                                value='grid',
                                clearable=False,
                                options=[
                                {'label': name.capitalize(), 'value': name}
                                for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                                    ]   
                                ),
                        cyto.Cytoscape(
                            id='cytoscape-update-layout',
                            layout={'name': 'grid'},
                            style={'width': '100%', 'height': '450px'},
                            elements=elements
                                    )
                            ])


                        @app.callback(Output('cytoscape-update-layout', 'layout'),
                            [Input('dropdown-update-layout', 'value')])
                        def update_layout(layout):
                            return {
                                'name': layout,
                                'animate': True
                                }


                        if __name__ == '__main__':
                            app.run_server(debug=True)      

                        '''
                    ]),
                ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),

                html.Div([
                html.Div([
                    html.H3(['大量のデータを見ることも出来る！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                ]),
                html.Div([
                        html.Div([

                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Fertility rate, total (births per woman)'
                        ),
                    dcc.RadioItems(
                        id='crossfilter-xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                        )
                    ],
                    style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Life expectancy at birth, total (years)'
                        ),
                    dcc.RadioItems(
                        id='crossfilter-yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                        )
                        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
                        ], style={
                            'borderBottom': 'thin lightgrey solid',
                            'backgroundColor': 'rgb(250, 250, 250)',
                            'padding': '10px 5px'
                        }),
                html.Div([
                html.Div([
                    dcc.Graph(
                        id='crossfilter-indicator-scatter',
                        hoverData={'points': [{'customdata': 'Japan'}]}
                        )
                        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
                    html.Div([
                        dcc.Graph(id='x-time-series'),
                        dcc.Graph(id='y-time-series'),
                        ], style={'display': 'inline-block', 'width': '49%'}),

                html.Div(dcc.Slider(
                    id='crossfilter-year--slider',
                    min=dfmany['Year'].min(),
                    max=dfmany['Year'].max(),
                    value=dfmany['Year'].max(),
                    marks={str(year): str(year) for year in dfmany['Year'].unique()}
                    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
                    ], style={'padding': '2%'}),
                    ])
                    ]),
                html.Div([
                    dcc.Markdown([
                        '''
                            こんな感じでアイデアがまとまっていない
                            データを大量に比較してみることもできます。

                            import dash
                            import dash_core_components as dcc
                            import dash_html_components as html
                            import pandas as pd
                            import plotly.graph_objs as go

                            external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

                            app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

                            df = pd.read_csv(
                            'https://gist.githubusercontent.com/chriddyp/'
                            'cb5392c35661370d95f300086accea51/raw/'
                            '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
                            'indicators.csv')

                            available_indicators = df['Indicator Name'].unique()

                            app.layout = html.Div([
                                html.Div([

                                html.Div([
                                    dcc.Dropdown(
                                        id='crossfilter-xaxis-column',
                                        options=[{'label': i, 'value': i} for i in available_indicators],
                                        value='Fertility rate, total (births per woman)'
                                        ),
                                    dcc.RadioItems(
                                        id='crossfilter-xaxis-type',
                                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                        value='Linear',
                                        labelStyle={'display': 'inline-block'}
                                        )
                                        ],
                                        style={'width': '49%', 'display': 'inline-block'}),

                                html.Div([
                                    dcc.Dropdown(
                                        id='crossfilter-yaxis-column',
                                        options=[{'label': i, 'value': i} for i in available_indicators],
                                        value='Life expectancy at birth, total (years)'
                                        ),
                                    dcc.RadioItems(
                                        id='crossfilter-yaxis-type',
                                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                        value='Linear',
                                        labelStyle={'display': 'inline-block'}
                                        )
                                        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
                                        ], style={
                                        'borderBottom': 'thin lightgrey solid',
                                        'backgroundColor': 'rgb(250, 250, 250)',
                                        'padding': '10px 5px'
                                        }),

                                html.Div([
                                    dcc.Graph(
                                        id='crossfilter-indicator-scatter',
                                        hoverData={'points': [{'customdata': 'Japan'}]}
                                            )
                                        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
                                html.Div([
                                    dcc.Graph(id='x-time-series'),
                                    dcc.Graph(id='y-time-series'),
                                    ], style={'display': 'inline-block', 'width': '49%'}),

                                html.Div(dcc.Slider(
                                    id='crossfilter-year--slider',
                                    min=df['Year'].min(),
                                    max=df['Year'].max(),
                                    value=df['Year'].max(),
                                    marks={str(year): str(year) for year in df['Year'].unique()}
                                    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
                                    ])


                            @app.callback(
                            dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
                            [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
                            dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
                            dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
                             dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
                            dash.dependencies.Input('crossfilter-year--slider', 'value')])
                            def update_graph(xaxis_column_name, yaxis_column_name,
                                xaxis_type, yaxis_type,
                                year_value):
                            dff = df[df['Year'] == year_value]

                            return {
                                'data': [go.Scatter(
                                x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                                y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                                text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                                customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                                mode='markers',
                                marker={
                                'size': 15,
                                'opacity': 0.5,
                                'line': {'width': 0.5, 'color': 'white'}
                                }
                                )],
                                'layout': go.Layout(
                                    xaxis={
                                    'title': xaxis_column_name,
                                    'type': 'linear' if xaxis_type == 'Linear' else 'log'
                                    },
                                    yaxis={
                                        'title': yaxis_column_name,
                                        'type': 'linear' if yaxis_type == 'Linear' else 'log'
                                        },
                                    margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                                    height=450,
                                    hovermode='closest'
                                        )
                                    }


                                def create_time_series(dff, axis_type, title):
                                    return {
                                        'data': [go.Scatter(
                                        x=dff['Year'],
                                        y=dff['Value'],
                                        mode='lines+markers'
                                        )],
                                        'layout': {
                                        'height': 225,
                                        'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
                                        'annotations': [{
                                        'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                                        'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                                        'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                                        'text': title
                                        }],
                                        'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
                                        'xaxis': {'showgrid': False}
                                        }
                                    }


                                @app.callback(
                                dash.dependencies.Output('x-time-series', 'figure'),
                                [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
                                 dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
                                dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
                                def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
                                    country_name = hoverData['points'][0]['customdata']
                                    dff = df[df['Country Name'] == country_name]
                                    dff = dff[dff['Indicator Name'] == xaxis_column_name]
                                    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
                                    return create_time_series(dff, axis_type, title)


                                @app.callback(
                                dash.dependencies.Output('y-time-series', 'figure'),
                                [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
                                dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
                                dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
                                def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
                                    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
                                    dff = dff[dff['Indicator Name'] == yaxis_column_name]
                                    return create_time_series(dff, axis_type, yaxis_column_name)


                                if __name__ == '__main__':
                                    app.run_server(debug=True)

                        '''
                    ])
                ], style={'padding': 30, 'fontSize': '2rem', 'background': '#EEFFDD'}),
                ]),
    #PAGE13
        dcc.Tab(label="DATA13", value="DATA13", style=tab_style, selected_style=tab_selected_style,         children=[
                    html.Div([
                        html.H3('今日のまとめ')
                    ], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                    html.Div([
                        html.H3('このようにDashを使えば、かなりの量のデータを使った可視化が簡単にできる！'),
                        html.H3('これを使えば、これまで以上にデータから情報を得ることが可能になる！'),
                        html.H3('プレゼンテーションでも使えるのではないか？'),
                        html.H3('もしそのような使い方ができるのであれば、多くの意見が得られるようになり、これまでにないデータの活用ができる！'),
                        html.H3('Dashの難点・・カッコが多い！！！！'),
                        html.H3('まぁCSSの使い方なんかを覚えられるのは良い')
                    ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 50, 'color': 'limegreen', 'marginTop': '5%'})
            ]),
    ], style=tabs_styles)
])

# Back To DATA9
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
                'color': dffpop[dffpop['area']==i]['color'],
            }, 
            name=i,
        )for i in dff.area.unique()],
        'layout': {
            'height': 800,
            'title': '{}年の都道府県GDP、一人当たりGDP、人口（円の大きさ）'.format(selected_year),
            'paper_bgcolor': '#EEFFDD',
            'fontSize': "2rem",
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
            'title': '{}の{}データ'.format(area, name),
            'paper_bgcolor': '#EEFFDD',
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

# first callback
@app.callback(
    dash.dependencies.Output('hokkaidoGraph', 'figure'),
    [dash.dependencies.Input('dropdown-for-hokkaido', 'value')]
)
def update_graph(factor):
    dff = dfhokkaido[dfhokkaido['item'] == factor]

    return {
        'data': [go.Scatter(
            x = dff['year'],
            y = dff['value']
        )]
    }

@app.callback(
    dash.dependencies.Output('hokkaidoGraph1', 'figure'),
    [dash.dependencies.Input('dropdown-for-hokkaido1', 'value')]
)
def update_graph(factor):
    dff = dfhokkaido[dfhokkaido['item'] == factor]

    return {
        'data': [go.Scatter(
            x = dff['year'],
            y = dff['value']
        )]
    }

# 付けたし②
@app.callback(
    dash.dependencies.Output('add-hover-data', 'children'),
    [dash.dependencies.Input('hokkaidoGraph1', 'hoverData')]
)
def return_hoverdata(hoverData):
    return json.dumps(hoverData)



# DATA11 CallBack
@app.callback(
    dash.dependencies.Output('scatter-chart1', 'figure'),
    [dash.dependencies.Input('slider-one1', 'value')]
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
                'color': dffpop[dffpop['area']==i]['color'],
            }, 
            name=i,
        )for i in dff.area.unique()],
        'layout': {
            'height': 800,
            'title': '{}年の都道府県GDP、一人当たりGDP、人口（円の大きさ）'.format(selected_year),
            'fontSize': "2rem",
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
            'title': '{}の{}データ'.format(area, name),
        }
    }



@app.callback(
    dash.dependencies.Output('chart-one1', 'figure'),
    [(dash.dependencies.Input('scatter-chart1', 'hoverData'))]
)
def createGDP(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'GDP']
    return create_smallChart(dff, areaName, 'GDP')

@app.callback(
    dash.dependencies.Output('chart-two1', 'figure'),
    [(dash.dependencies.Input('scatter-chart1', 'hoverData'))]
)
def createPerGDP(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'pergdp']
    return create_smallChart(dff, areaName, 'pergdp')

@app.callback(
    dash.dependencies.Output('chart-three1', 'figure'),
    [(dash.dependencies.Input('scatter-chart1', 'hoverData'))]
)
def createPopu(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'popu']
    return create_smallChart(dff, areaName, 'popu')

# DATA12
# RealTime Graph usd-jpy
@app.callback(
    dash.dependencies.Output('usdjpy', 'figure'),
    [dash.dependencies.Input('interval_components', 'n_intervals')]
)
def update_graph(n):
    t = datetime.now()
    nowHour = t.hour
    nowMinute = t.minute 
    nowSecond = t.second 

    d = datetime(2016, 1, 5, nowHour+9, nowMinute, nowSecond)
    period = timedelta(seconds = 120)
    d1 = d - period 
    dffjpy1 = dffjpy.loc['{}'.format(d1): '{}'.format(d), :]

    return {
        'data': [go.Scatter(
            x = dffjpy1.index,
            y = dffjpy1['Bid']
        )],
        'layout':{
            'height': 600,
            'title': 'USD-JPY 1Second Charts'
        }
    }

# CytoScape callback
@app.callback(dash.dependencies.Output('cytoscape-update-layout', 'layout'),
              [dash.dependencies.Input('dropdown-update-layout', 'value')])
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }

# many data callback
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dffmany = dfmany[dfmany['Year'] == year_value]

    return {
        'data': [go.Scatter(
            x=dffmany[dffmany['Indicator Name'] == xaxis_column_name]['Value'],
            y=dffmany[dffmany['Indicator Name'] == yaxis_column_name]['Value'],
            text=dffmany[dffmany['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dffmany[dffmany['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dffmany, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dffmany['Year'],
            y=dffmany['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dffmany = dfmany[dfmany['Country Name'] == country_name]
    dffmany = dffmany[dffmany['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dffmany, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dffmany = dfmany[dfmany['Country Name'] == hoverData['points'][0]['customdata']]
    dffmany = dffmany[dffmany['Indicator Name'] == yaxis_column_name]
    return create_time_series(dffmany, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)