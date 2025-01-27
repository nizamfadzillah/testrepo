# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get the max and min payload for the range slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Get the unique launch sites
launch_sites = spacex_df['Launch Site'].unique()
launch_site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in
                                                                  launch_sites]

# Create the app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Task 1: Launch Site Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=launch_site_options,
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),

    # Task 2: Success Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    # Task 3: Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0,  # Minimum value is 0 Kg
                    max=10000,  # Maximum value is 10000 Kg
                    step=1000,  # Step size is 1000 Kg
                    marks={0: '0',
                           1000: '1000',
                           2000: '2000',
                           3000: '3000',
                           4000: '4000',
                           5000: '5000',
                           6000: '6000',
                           7000: '7000',
                           8000: '8000',
                           9000: '9000',
                           10000: '10000'},  # Label marks for different payloads
                    value=[min_payload, max_payload]),  # Default value range from min_payload to max_payload

    # Task 4: Success-Payload Scatter Chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])


# Task 2: Add a callback function to render the success-pie-chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # Filter the dataframe based on the selected site
    if entered_site == 'ALL':
        # If 'ALL' is selected, show the total success count for all sites
        fig = px.pie(spacex_df, names='class',
                     title='Total Launch Success (All Sites)',
                     labels={'class': 'Launch Success'},
                     hole=0.3)  # Add a hole for a donut-style chart
    else:
        # If a specific site is selected, filter data for the chosen site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Group by 'class' and count the number of occurrences for each success/failure
        site_success_counts = filtered_df.groupby('class').size().reset_index(name='count')

        # Create a pie chart with success (class=1) and failure (class=0) counts
        fig = px.pie(site_success_counts,
                     values='count',
                     names=site_success_counts['class'].map({0: 'Failed', 1: 'Success'}),
                     title=f'Launch Success for {entered_site}')

    return fig


# Task 4: Add a callback function for success-payload-scatter-chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, payload_range):
    # Filter data based on selected payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]

    if entered_site != 'ALL':
        # If a specific site is selected, filter further by the launch site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    # Create a scatter plot to show the correlation between payload and launch success
    fig = px.scatter(filtered_df,
                     x='Payload Mass (kg)',
                     y='class',
                     color='Booster Version Category',  # Color points based on the booster version
                     title='Launch Success vs Payload Mass',
                     labels={'class': 'Launch Success (0=Failure, 1=Success)',
                             'Payload Mass (kg)': 'Payload Mass (kg)'},
                     category_orders={'class': [0, 1]})

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
'''
Which site has the largest successful launches?
CCAFS SLC-40

Which site has the highest launch success rate?


Which payload range(s) has the highest launch success rate?
Which payload range(s) has the lowest launch success rate?
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?
'''