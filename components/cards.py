from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def create_cards():
    return [
        # Primeira linha de gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Evolução do Desempenho das Equipes"),
                    dbc.CardBody([dcc.Graph(id='team-evolution')])
                ], className="dashboard-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Comparação de Jogadores por Lane"),
                    dbc.CardBody([dcc.Graph(id='player-comparison')])
                ], className="dashboard-card")
            ], width=6)
        ], className="mb-4"),

        # Segunda linha de gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Comparação entre Lanes"),
                    dbc.CardBody([dcc.Graph(id='lane-radar')])
                ], className="dashboard-card")
            ], width=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Queda de Desempenho"),
                    dbc.CardBody([dcc.Graph(id='performance-drop')])
                ], className="dashboard-card")
            ], width=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Nacionalidade dos Jogadores"),
                    dbc.CardBody([dcc.Graph(id='nationality-pie')])
                ], className="dashboard-card")
            ], width=4)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Métricas por Semana"),
                    dbc.CardBody([
                    dash_table.DataTable(
                        id='metrics-table',
                        columns=[
                            {'name': 'Semana', 'id': 'Semana'},
                            {'name': 'Melhor Time', 'id': 'Melhor Time'},
                            {'name': 'Pior Time', 'id': 'Pior Time'},
                            {'name': 'Jogador com Maior Melhoria', 'id': 'Jogador com Maior Melhoria'},
                            {'name': 'Jogador com Pior Desempenho', 'id': 'Jogador com Pior Desempenho'},
                            {'name': 'Time que Mais Evoluiu', 'id': 'Time que Mais Evoluiu'},
                            {'name': 'Time com Maior Queda', 'id': 'Time com Maior Queda'},
                            {'name': 'Jogador Mais Consistente', 'id': 'Jogador Mais Consistente'},
                            {'name': 'Time Mais Consistente', 'id': 'Time Mais Consistente'},
                            {'name': 'Maior Queda de Desempenho', 'id': 'Maior Queda de Desempenho'},
                            {'name': 'Melhores Jogadores por Lane', 'id': 'Melhores Jogadores por Lane'},
                            {'name': 'Melhor Jogador Geral', 'id': 'Melhor Jogador Geral'},
                            {'name': 'Time com Melhor Rendimento por Nacionalidade', 'id': 'Time com Melhor Rendimento por Nacionalidade'},
                            {'name': 'Evolução de Tiers', 'id': 'Evolução de Tiers'}
                        ],
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '10px'
                        },
                        style_header={
                            'backgroundColor': '#333333',
                            'color': '#ffffff',
                            'fontWeight': 'bold'
                        },
                        style_data={
                            'backgroundColor': '#1e1e1e',
                            'color': '#ffffff'
                        }
                    )
                    ])
                ], className="dashboard-card")
            ])
        ])
    ]