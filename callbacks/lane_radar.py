from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utils.theme import GRAPH_THEME, TEAM_COLORS

def register_lane_radar_callback(app, df_players):
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