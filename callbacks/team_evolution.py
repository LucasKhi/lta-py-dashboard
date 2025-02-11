from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utils.theme import GRAPH_THEME, TEAM_COLORS

def register_team_evolution_callback(app, df_teams):
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