from dash import dcc

def create_filters(df_players):
    return dcc.Dropdown(
        id='lane-selector',
        options=[{'label': lane, 'value': lane} for lane in df_players['lane'].unique()],
        value='Top',
        clearable=False,
        className="mb-3"
    )