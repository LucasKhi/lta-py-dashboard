from dash.dependencies import Input, Output
from utils.data_processing import calculate_metrics

def register_metrics_table_callback(app, df_players, df_teams):
    @app.callback(
        Output('metrics-table', 'data'),
        Input('lane-selector', 'value')
    )
    def update_metrics_table(dummy):
        metrics_df = calculate_metrics(df_players, df_teams)
        return metrics_df.to_dict('records')