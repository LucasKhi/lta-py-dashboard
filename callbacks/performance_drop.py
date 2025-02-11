from dash.dependencies import Input, Output
import plotly.express as px
from utils.theme import GRAPH_THEME, TEAM_COLORS

def register_performance_drop_callback(app, df_players):
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