# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import warnings

# Read the airline data into pandas dataframe

warnings.filterwarnings("ignore")
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
                               
app.layout = html.Div( 
    children = [
        html.H1( 
            'Airline Performance Dashboard', 
            style = { 
                'textAlign': 'center', 'color': '#503D36', 'font-size': 40
            }
        ),
        html.Div( 
            [
                "Input Year: ", 
                dcc.Input( 
                    id='input-year', 
                    value='2010', 
                    type='number',
                    style = {'height':'50px', 'font-size': 35} 
                )
            ], 
            style={'font-size': 40}
        ),
        html.Br(),
        html.Br(),
        html.Div(dcc.Graph(id='line-plot')),
    ]
)

# add callback decorator
@app.callback( Output(component_id='line-plot', component_property='figure'),
               Input(component_id='input-year', component_property='value'))

# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select 2019 data
    
    # Group the data by Month and compute average over arrival delay time.
    #line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()


    fig = go.Figure(data=go.Scatter(x=spacex_df['Launch Site'], y=spacex_df['Payload Mass (kg)'] ))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Launch Site', yaxis_title='Payload Mass (kg)')
    
    print(fig)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()