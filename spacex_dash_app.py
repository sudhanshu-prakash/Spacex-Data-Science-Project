# Import required libraries
from unicodedata import name
from click import launch
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import warnings
from dash import no_update
from jupyter_dash import JupyterDash



# Create a dash application
app = JupyterDash(__name__)
JupyterDash.infer_jupyter_proxy_config()

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True


warnings.filterwarnings("ignore")
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={
                'textAlign': 'center', 
                'color': '#503D36',
                'font-size': 40
            }
        ),

        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id='site-dropdown', 
            options=[
                {'label': 'All Sites', 'value': 'all'},
                {'label': 'CCAFS LC-40', 'value': 'ccafs_lc_40'},
                {'label': 'VAFB SLC-4E', 'value': 'vafb_slc_4e'},
                {'label': 'KSC LC-39A', 'value': 'ksc_lc_39a'},
                {'label': 'CCAFS SLC-40', 'value': 'ccafs_slc_40'}
            ],
            placeholder='Select a Launch Site here',
            style={ 'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'},
            searchable= True
        ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site

        
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        #dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(
            id='payload-slider',
            min=0, max=10000, step=1000,
            marks={0: '0', 100: '100'},
            value=[min_payload, max_payload]
        ),


        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph( id='success-payload-scatter-chart'))       
    ]
)




@app.callback(
        Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_input):
    filtered_df = spacex_df
    xfiltered_df = spacex_df
    if entered_input=='all':
        fig = px.pie(
            filtered_df, 
            values='class', 
            names='Launch Site', 
            title='Total Sucess launches By Site'
        )
    else:
        launch_site = ''
        if entered_input=='ccafs_lc_40':
            xfiltered_df = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
            launch_site = 'CCAFS LC-40'
        if entered_input=='vafb_slc_4e':
            xfiltered_df = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
            launch_site = 'VAFB SLC-4E'
        if entered_input=='ksc_lc_39a':
            xfiltered_df = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
            launch_site = 'CCAFS SLC-40'
        if entered_input=='ccafs_slc_40':
            xfiltered_df = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
            launch_site = 'CCAFS SLC-40'
        xfiltered_df['new']=xfiltered_df['class'].apply(lambda x: 'success' if x==1 else 'failed')
        fig = px.pie(
            xfiltered_df, 
            names='new',
            title='Total Sucess launches for Site ' + launch_site
        )
    return fig
 


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'), 
        Input(component_id="payload-slider", component_property="value")        
    ]
)
def get_input(entered_input, payload_slider_input):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)']>=payload_slider_input[0]]
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)']<=payload_slider_input[1]]
    if entered_input=='all':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        if entered_input=='ccafs_lc_40':
            filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        if entered_input=='vafb_slc_4e':
            filtered_df = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        if entered_input=='ksc_lc_39a':
            filtered_df = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        if entered_input=='ccafs_slc_40':
            filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server(mode="inline", host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False)
