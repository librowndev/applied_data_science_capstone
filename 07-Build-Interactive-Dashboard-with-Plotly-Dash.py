# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# get spacex data
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

launch_sites = spacex_df['Launch Site'].str.strip().unique()

dropdown_options = [{'label': 'All', 'value': 'All'}] + [{'label': category, 'value': category} for category in
                                                         launch_sites]

max_payload = spacex_df['Payload Mass (kg)'].max()


min_payload = spacex_df['Payload Mass (kg)'].min()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('SpaceX Launch App', style={'textAlign': 'center', 'color': 'black', 'fontSize': 24}),
    dcc.Dropdown(
        id='category-dropdown',
        options=dropdown_options,
        value='All',
        searchable=True,
        clearable=True,

    ),
    dcc.Graph(
        id='pie-chart'
    ),
    html.Br(),
    html.P('Payload Mass (kg):'),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: '{}'.format(i) for i in range(int(min_payload), int(max_payload) + 1000, 1000)},
        value=[min_payload, max_payload]
    ),
    dcc.Graph(id='scatter-plot'),
])


@app.callback(
    Output('pie-chart', 'figure'),
    Input('category-dropdown', 'value')

)
def pie_chart(selected_category):
    if selected_category == ('All' or 'ALL'):
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Success Rate by Launch Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_category]
        small_df = filtered_df['class'].value_counts().reset_index()
        fig = px.pie(small_df, values='count', names='class',
                     title=f'Success vs Failed Launches for {selected_category}')
        return fig


@app.callback(
    Output('scatter-plot', 'figure'),
    Input('category-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def scatter_plot(selected_category, payload_range):
    if selected_category == 'All':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_category) &
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                         title=f'Correlation between Payload and Success for {selected_category}')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
