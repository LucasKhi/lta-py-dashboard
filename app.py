import json
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Carregando os dados
with open('data/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Processando os dados para criar DataFrames
def process_data(data):
    all_players = []
    team_averages = []
    
    for team in data['teams']:
        team_name = team['name']
        for week in team['weeks']:
            week_num = week['week']
            for player in week['players']:
                player_data = {
                    'team': team_name,
                    'week': week_num,
                    'name': player['name'],
                    'lane': player['lane'],
                    'country': player['country'],
                    'score': player['score'],
                    'tier': player['tier']
                }
                all_players.append(player_data)
            
            team_averages.append({
                'team': team_name,
                'week': week_num,
                'average_score': week['average_score']
            })
    
    return pd.DataFrame(all_players), pd.DataFrame(team_averages)

df_players, df_teams = process_data(data)

# Configurações de tema para os gráficos
GRAPH_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#ffffff'},
    'xaxis': {'gridcolor': '#333333', 'zerolinecolor': '#333333'},
    'yaxis': {'gridcolor': '#333333', 'zerolinecolor': '#333333'}
}

# Cores personalizadas para os times
TEAM_COLORS = {
    'paiN Gaming': '#000000',
    'LOUD': '#13FF00',
    'RED Canids': '#9E1A27',
    'Leviatan': '#6AABDC',
    'Isurus Estral': '#FA4726',
    'FURIA': '#817D4D',
    'Fluxo W7M': '#ED0446',
    'VKS': '#5C2A82',
}

# Para times com duas cores, você pode usar gradientes
def create_gradient_colors():
    return {
        'paiN Gaming': ['#000000', '#FFFFFF'],
        'FURIA': ['#000000', '#817D4D'],
        'Fluxo W7M': ['#3A3436', '#ED0446'],
        'Isurus Estral': ['#FA4726', '#0054DC']
    }

GRADIENT_COLORS = create_gradient_colors()

# Iniciando o app Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap'
    ]
)

# Layout do dashboard
app.layout = dbc.Container([
    # Cabeçalho com logo
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    src="https://elasticbeanstalk-us-east-1-909474674380.s3.us-east-1.amazonaws.com/lta_sul_logo_certo_f5613bf154.png",
                    className="img-fluid",
                    style={'maxHeight': '80px'}
                ),
                html.H1("LTA sul Dashboard", className="ms-3 mb-0")
            ], className="logo-container")
        ], className="dashboard-header")
    ]),
    
    # Filtros globais
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filtros", className="card-title"),
                    dcc.Dropdown(
                        id='lane-selector',
                        options=[{'label': lane, 'value': lane} for lane in df_players['lane'].unique()],
                        value='Top',
                        clearable=False,
                        className="mb-3"
                    )
                ])
            ], className="dashboard-card")
        ])
    ], className="mb-4"),
    
    # Primeira linha de gráficos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Evolução do Desempenho das Equipes"),
                dbc.CardBody([
                    dcc.Graph(id='team-evolution')
                ])
            ], className="dashboard-card")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Comparação de Jogadores por Lane"),
                dbc.CardBody([
                    dcc.Graph(id='player-comparison')
                ])
            ], className="dashboard-card")
        ], width=6)
    ], className="mb-4"),
    
    # Segunda linha de gráficos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Comparação entre Lanes"),
                dbc.CardBody([
                    dcc.Graph(id='lane-radar')
                ])
            ], className="dashboard-card")
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Queda de Desempenho"),
                dbc.CardBody([
                    dcc.Graph(id='performance-drop')
                ])
            ], className="dashboard-card")
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Nacionalidade dos Jogadores"),
                dbc.CardBody([
                    dcc.Graph(id='nationality-pie')
                ])
            ], className="dashboard-card")
        ], width=4)
    ])
    
], fluid=True, className="p-4")

# Callbacks atualizados com novo tema
@app.callback(
    Output('team-evolution', 'figure'),
    Input('lane-selector', 'value')
)
def update_team_evolution(dummy):
    fig = go.Figure()
    
    for team in df_teams['team'].unique():
        fig.add_trace(go.Scatter(
            x=df_teams[df_teams['team'] == team]['week'],
            y=df_teams[df_teams['team'] == team]['average_score'],
            name=team,
            mode='lines+markers',
            line={'color': TEAM_COLORS[team]},
            marker={'size': 10}
        ))
    
    fig.update_layout(
        **GRAPH_THEME,
        title='Evolução do Desempenho das Equipes',
        xaxis_title='Semana',
        yaxis_title='Pontuação Média',
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output('player-comparison', 'figure'),
    Input('lane-selector', 'value')
)
def update_player_comparison(lane):
    lane_data = df_players[df_players['lane'] == lane]
    
    fig = px.bar(
        lane_data,
        x='name',
        y='score',
        color='team',
        barmode='group',
        facet_col='week',
        color_discrete_map=TEAM_COLORS,
        title=f'Comparação de Jogadores - {lane}'
    )
    
    fig.update_layout(**GRAPH_THEME)
    
    return fig

@app.callback(
    Output('lane-radar', 'figure'),
    Input('lane-selector', 'value')
)
def update_lane_radar(dummy):
    lane_avg = df_players.groupby(['team', 'lane'])['score'].mean().reset_index()
    
    fig = go.Figure()
    
    for team in lane_avg['team'].unique():
        team_data = lane_avg[lane_avg['team'] == team]
        fig.add_trace(go.Scatterpolar(
            r=team_data['score'],
            theta=team_data['lane'],
            name=team,
            fill='toself',
            line={'color': TEAM_COLORS[team]}
        ))
    
    fig.update_layout(
        **GRAPH_THEME,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#333333'
            )
        )
    )
    
    return fig

@app.callback(
    Output('performance-drop', 'figure'),
    Input('lane-selector', 'value')
)
def update_performance_drop(dummy):
    week1 = df_players[df_players['week'] == 1].set_index(['name', 'team'])['score']
    week2 = df_players[df_players['week'] == 2].set_index(['name', 'team'])['score']
    variation = (week2 - week1).reset_index()
    variation.columns = ['name', 'team', 'variation']
    
    drops = variation[variation['variation'] < 0].sort_values('variation')
    
    fig = px.bar(
        drops,
        y='name',
        x='variation',
        color='team',
        orientation='h',
        color_discrete_map=TEAM_COLORS
    )
    
    fig.update_layout(
        **GRAPH_THEME,
        title='Queda de Desempenho entre Semanas',
        xaxis_title='Variação na Pontuação',
        yaxis_title='Jogador'
    )
    
    return fig

@app.callback(
    Output('nationality-pie', 'figure'),
    Input('lane-selector', 'value')
)
def update_nationality_pie(dummy):
    nationality_counts = df_players[df_players['week'] == 1]['country'].value_counts()
    
    fig = px.pie(
        values=nationality_counts.values,
        names=nationality_counts.index,
        title='Nacionalidade dos Jogadores',
        hole=0.3,
        color_discrete_sequence=['#FF4B4B', '#4B9EFF']
    )
    
    fig.update_layout(**GRAPH_THEME)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)