import dash
from dash import html
import dash_bootstrap_components as dbc
from components.header import create_header
from components.filters import create_filters
from components.cards import create_cards
from callbacks.team_evolution import register_team_evolution_callback
from callbacks.player_comparison import register_player_comparison_callback
from callbacks.lane_radar import register_lane_radar_callback
from callbacks.performance_drop import register_performance_drop_callback
from callbacks.nationality_pie import register_nationality_pie_callback
from callbacks.metrics_table import register_metrics_table_callback

from utils.data_processing import load_and_process_data

df_players, df_teams = load_and_process_data()

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap'
    ]
)

app.layout = dbc.Container([
    create_header(),
    create_filters(df_players),
    *create_cards()
], fluid=True, className="p-4")

register_team_evolution_callback(app, df_teams)
register_player_comparison_callback(app, df_players)
register_lane_radar_callback(app, df_players)
register_performance_drop_callback(app, df_players)
register_nationality_pie_callback(app, df_players)
register_metrics_table_callback(app, df_players, df_teams)


if __name__ == '__main__':
    app.run_server(debug=True)