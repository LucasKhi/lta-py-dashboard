from dash.dependencies import Input, Output
import plotly.express as px
from utils.theme import GRAPH_THEME

def register_nationality_pie_callback(app, df_players):
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