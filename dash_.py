# Importing the libraries needed.
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Creating our Dash web app.
app = dash.Dash(external_stylesheets=[
                dbc.themes.CYBORG], title='Life Expectancy x GDP')

# Loading the dataset to be used.
df = pd.read_csv(
    "https://raw.githubusercontent.com/ThuwarakeshM/geting-started-with-plottly-dash/main/life_expectancy.csv")

# Creating the dashboard's main chart.
fig = px.scatter(
    df,
    x="GDP",
    y="Life expectancy",
    size="Population",
    color="continent",
    hover_name="Country",
    log_x=True,
    size_max=60

)
# Defining the web page structure.
app.layout = html.Div([
    html.H1('Life Expectancy x GDP (2000-2015)',
            style={'font-size': '30px', 'text-align': 'center', 'margin-top': '15px'}),
    # The 'children' attribute allows you to insert other elements into an HTML or dcc features.
    # We are going to create a row with a column for each of the dashboard's Dropdowns.

    dbc.Row([
        dbc.Col([
            html.Div([
                # A Dropdown enabing the filtering of the data accordingly to the countries' development status.
                html.Label('Select the Country Status Desired'),
                dcc.Dropdown(
                    id='status-Dropdown',
                    options=[
                        {'label': s, 'value': s} for s in df.Status.unique()
                    ])  # ,

            ]),
        ]),
        dbc.Col([
            html.Div([
                # Another Dropdown filtering out the countries which its average schooling years surpasses the one established
                # by the user.
                html.Label('Select the Maximum Schooling Years'),
                dcc.Dropdown(id='schooling-Dropdown',
                             options=[
                                 {'label': y, 'value': y} for y in range(
                                     int(df.Schooling.min()),
                                     int(df.Schooling.max() + 1)
                                 )
                             ])
            ]),

        ])

    ]),
    # The place where the chart will be displayed.
    html.Div(
        dcc.Graph(id="life-exp-vs-gdp", figure=fig),
        className='chart'),

    # Finally, we are going to add a slider so one can visualize the data from every single year explored in the dataset.
    html.Div(
        dcc.Slider(min=df.Year.min(),
                   max=df.Year.max(),
                   step=1,
                   value=df.Year.min(),
                   marks={year: str(year) for year in range(
                       df.Year.min(), df.Year.max() + 1)},
                   id='year-slider')  # ,
    )

])

# Interactivity section.
# Setting the intereactivity functionality considering the values from the Dropdowns and the slider.


@app.callback(
    Output('life-exp-vs-gdp', 'figure'),
    Input('status-Dropdown', 'value'),
    Input('schooling-Dropdown', 'value'),
    Input('year-slider', 'value'))
def update_chart(country_status, schooling, selected_year):
    filtered_dataset = df[df.Year == selected_year]
    if schooling:
        filtered_dataset = filtered_dataset[filtered_dataset['Schooling'] <= schooling]
    if country_status:
        filtered_dataset = filtered_dataset[filtered_dataset['Status']
                                            == country_status]
    fig = px.scatter(
        filtered_dataset,
        x="GDP",
        y="Life expectancy",
        size="Population",
        color="continent",
        hover_name="Country",
        log_x=True,
        size_max=60  # ,
    )
    # Use this method in order to modify aesthetics features of your chart.
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='#7FDBFF',
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
