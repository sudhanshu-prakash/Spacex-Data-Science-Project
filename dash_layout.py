# Import required libraries
from dash.html.Center import Center
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "NYC", "MTL", "NYC"]
})

fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')

app =dash.Dash()
app.layout = html.Div(
    children=[
        html.H1(
            children='Dashboard',
            style={
                'textAlign':'center'
            }
        ),
        dcc.Dropdown(options=[
            { 'label': 'New York City', 'value':'NYC'},
            { 'label': 'Montreal', 'value':'MTL'},
            { 'label': 'San Francisco', 'value':'SF'},
        ]),
        dcc.Graph(id='example-graph-2',figure=fig)
    ]
)


if __name__=='__main__':
    app.run_server()