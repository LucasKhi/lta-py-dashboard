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
                                {'name': 'Jogador com Maior Melhoria', 'id': 'Jogador com Maior Melhoria'},
                                {'name': 'Time que Mais Evoluiu', 'id': 'Time que Mais Evoluiu'}
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