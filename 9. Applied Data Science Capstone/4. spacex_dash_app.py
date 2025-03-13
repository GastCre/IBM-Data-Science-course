# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

#Dropdown options
launch_sites=spacex_df['Launch Site'].value_counts().index
options=[{'label': 'All Sites', 'value': 'ALL'},{'label': launch_sites[0], 'value': launch_sites[0]},{'label': launch_sites[1], 'value': launch_sites[1]},{'label': launch_sites[2], 'value': launch_sites[2]},{'label': launch_sites[3], 'value': launch_sites[3]}]

#Success rate
sr_df=spacex_df.groupby('Launch Site')['class'].mean()



# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=options,placeholder='Select Launch Site here',value='ALL',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'), Input(component_id='site-dropdown',component_property='value'))
#Pie chart
def get_pie_chart(options):
    if options == 'ALL':
        sr_df=spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig = px.pie(sr_df,values='class',names='Launch Site',title='Total success launches by site')
        return fig
    else:
        filtered_df = spacex_df[['Launch Site','class']].value_counts().reset_index()
        filtered_df['class']=filtered_df['class'].map({0:'Failure',1:'Success'})
        fig = px.pie(filtered_df[filtered_df['Launch Site']==options],values='count', names='class',title='Success rate',color='class', color_discrete_map={'Failure': 'red', 'Success': 'green'})
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'), [Input(component_id='payload-slider',component_property='value'),Input(component_id='site-dropdown',component_property='value')])
def get_scatter(value,options):
    if options == 'ALL':
        fig = px.scatter(spacex_df,x='Payload Mass (kg)',y='class',title='Outcome vs payload mass by booster version',color="Booster Version Category",range_x=value)
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==options]
        fig = px.scatter(filtered_df,x='Payload Mass (kg)',y='class',title='Outcome vs payload mass by booster version',color="Booster Version Category",range_x=value)
        return fig
        # return the outcomes piechart for a selected site


# Run the app
if __name__ == '__main__':
    app.run_server()
