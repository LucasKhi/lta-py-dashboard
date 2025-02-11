from dash import html

def create_header():
    return html.Div([
        html.Img(
            src="https://elasticbeanstalk-us-east-1-909474674380.s3.us-east-1.amazonaws.com/lta_sul_logo_certo_f5613bf154.png",
            className="img-fluid",
            style={'maxHeight': '80px'}
        ),
        html.H1("LTA sul Dashboard", className="ms-3 mb-0")
    ], className="logo-container")