from dash.dependencies import Input, Output
import plotly.express as px
from utils.theme import GRAPH_THEME, TEAM_COLORS

def register_player_comparison_callback(app, df_players):
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

        fig.update_xaxes(title_text='Jogador')
        fig.update_yaxes(title_text='Pontuação')

        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("week=", "Semana ")))
        fig.update_layout(**GRAPH_THEME)
        return fig