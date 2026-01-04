import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min and max payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center'}
    ),

    # Dropdownpython3.11 spacex-dash-app.py

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    # Pie chart
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    # Payload slider
    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload],
        marks={i: str(i) for i in range(0, 10001, 2500)}
    ),

    # Scatter chart
    dcc.Graph(id='success-payload-scatter-chart')

])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):

    if site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='Class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig

    filtered_df = spacex_df[spacex_df['Launch Site'] == site]

    fig = px.pie(
        filtered_df,
        names='Class',
        title=f'Success vs Failure for {site}'
    )
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter_plot(site, payload_range):

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
        y='Class',
        color='Booster Version Category',
        title='Payload vs Launch Outcome'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
