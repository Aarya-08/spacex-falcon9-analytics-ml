import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={'textAlign': 'center'}
    ),

    # Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),

    dcc.Graph(id='success-pie-chart'),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={i: str(i) for i in range(0, 10001, 2500)}
    ),

    dcc.Graph(id='success-payload-scatter-chart')
])

# ---------------- PIE CHART CALLBACK ----------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):
    if site == 'ALL':
        success_df = spacex_df[spacex_df['class'] == 1] \
                        .groupby('Launch Site') \
                        .size() \
                        .reset_index(name='Success Count')

        fig = px.pie(
            success_df,
            values='Success Count',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(
            site_df,
            names='class',
            title=f'Success vs Failure for {site}'
        )
        return fig

# ---------------- SCATTER PLOT CALLBACK ----------------
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(site, payload_range):
    low, high = payload_range

    df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if site != 'ALL':
        df = df[df['Launch Site'] == site]

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs Launch Outcome'
    )
    return fig
if __name__ == '__main__':
    app.run()
