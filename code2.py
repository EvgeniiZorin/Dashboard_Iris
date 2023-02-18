import datetime
import numpy as np
import pandas as pd

import plotly.graph_objs as go
import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {'text': 'red'}
np.random.seed(50)
df = pd.DataFrame({
	'x_rand': np.random.randint(1,61,60),
	'y_rand': np.random.randint(1,61,60)
})

df_iris = px.data.iris()


app.layout = html.Div([
	html.H1(
		children='Iris Dashboard!!!',
		style = {
			'textAlign': 'center',
			'color': 'grey'
		}
	),
	html.Div(
		children='This is a dashboard about the classical Iris datasetDash',
		style = {
			'textAlign': 'center',
			'color': 'grey'
		}
	),
	html.Br(),
	# link: https://www.youtube.com/watch?v=1nEL0S8i2Wk
	dbc.Row([
		dbc.Col([
			html.H1('Dropdown for Iris dataset:'),
			html.Label('Choose an Iris species:'),
			html.Br(), # Add a break
			dcc.Dropdown(
				id='iris_scatterplot_dropdown',
				options = df_iris['species'].unique(),
				value = 'setosa', # Choose default pre-selected value
				multi = True, # Enable multi-choice option
				# disabled = True, # Makes this dropdown unavailable. Can be useful in conditions
				placeholder = "Select a city from the list ..."
			),
		]),
		dbc.Col([
			dcc.Graph(
				id = 'iris_scatterplot'
			),
		])
	]),
	html.Br(),
	html.Div(
		children='Below you can see the dataset used for Iris:',
		style = {
			'textAlign': 'center',
			'color': 'grey'
		}
	),
	html.Br(),
	dash_table.DataTable(df_iris.to_dict('records'), [{"name": i, "id": i} for i in df_iris.columns])
])

@app.callback(Output("iris_scatterplot", "figure"), Input('iris_scatterplot_dropdown', 'value')
)
def sync_input(iris_scatterplot_selection):
	print(iris_scatterplot_selection)
	if type(iris_scatterplot_selection) == str:
		iris_scatterplot_selection = [iris_scatterplot_selection]
	# df_iris_slice = df_iris[df_iris['species'] == iris_scatterplot_selection]
	df_iris_slice = df_iris[df_iris['species'].isin(iris_scatterplot_selection)]
	fig = px.scatter(
		df_iris_slice, x=f'sepal_width', y='sepal_length',
		color='species'
	)
	fig.layout.paper_bgcolor = '#f2f2f2'
	fig.layout.plot_bgcolor = '#e1e1e1'
	fig.layout.title = 'Iris plot by species'
	return fig

if __name__ == '__main__':
	app.run_server(
		debug=True, # To automatically reload your changes in the online dashboard
	)