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
from dash.dependencies import State

import dash_auth
import secrets_users
import styles


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Authentification
auth = dash_auth.BasicAuth(
    app,
    secrets_users.VALID_USERNAME_PASSWORD_PAIRS
)

# styles = {
# 	'H1': {'textAlign':'center', 'color':'grey'},
# 	'text': {'textAlign':'center', 'color':'grey', 'fontSize':20}
# }

np.random.seed(50)
df = pd.DataFrame({
	'x_rand': np.random.randint(1,61,60),
	'y_rand': np.random.randint(1,61,60)
})

df_iris = px.data.iris()


app.layout = html.Div([
	html.H1(
		children='Iris Dashboard!!!',
		style=styles.H1
	),
	html.Div(
		children='This is a dashboard about the classical Iris datasetDash',
		style=styles.text
	),
	html.Br(),
	# link: https://www.youtube.com/watch?v=1nEL0S8i2Wk
	dbc.Row([
		dbc.Col([
			html.H1(
				children='Controls for the plots',
				style=styles.H1
			),
			html.Label(
				children='Please choose Iris species:',
				style=styles.text
			),
			html.Br(), # Add a break
			dcc.Dropdown(
				id='iris_species_dropdown',
				options = df_iris['species'].unique(),
				value = 'setosa', # Choose default pre-selected value
				multi = True, # Enable multi-choice option
				# disabled = True, # Makes this dropdown unavailable. Can be useful in conditions
				placeholder = "Select a city from the list ..."
			),
		]),
		dbc.Col([
			html.H1(
				children='Relationship of sepal length and width',
				style=styles.H1
			),
			dcc.Graph(
				id = 'iris_scatterplot'
			),
		])
	]),
	html.Br(),
	html.H1(
		children='Sepal Characteristics',
		style=styles.H1
	),
	html.Br(),
	dbc.Row([
		dbc.Col([
			html.H2(
				children='Distribution of sepal length by species',
				style=styles.H2
			),
			dcc.Graph(id = 'iris_barplot_sepalLength')
		]),
		dbc.Col([
			html.H2(
				children='Distribution of sepal width by species',
				style=styles.H2
			),
			dcc.Graph(id = 'iris_barplot_sepalWidth')
		])
	]),
	html.Br(),
	# html.Div(
	# 	children='Below you can see the dataset used for Iris:',
	# 	style = H1_style
	# ),
	# # dcc.Graph(id = 'iris_barplot_sepalLength'),
	# dash_table.DataTable(df_iris.to_dict('records'), [{"name": i, "id": i} for i in df_iris.columns])
])

@app.callback(
	Output("iris_scatterplot", "figure"), 
	Input('iris_species_dropdown', 'value')
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

@app.callback(
	Output('iris_barplot_sepalLength', 'figure'),
	Input('iris_species_dropdown', 'value')
)
def figure1(input):
	if type(input) == str:
		input = [input]
	df_iris_slice = df_iris[df_iris['species'].isin(input)]
	fig = px.histogram(
		df_iris_slice, x='sepal_length', color='species', nbins=40
	)
	fig.update_layout(barmode='overlay')
	fig.update_traces(opacity=0.75)
	fig.layout.title = "title1"
	fig.layout.paper_bgcolor = '#f2f2f2'
	fig.layout.plot_bgcolor = '#e1e1e1'
	return fig

@app.callback(
	Output('iris_barplot_sepalWidth', 'figure'),
	Input('iris_species_dropdown', 'value')
)
def figure1(input):
	if type(input) == str:
		input = [input]
	df_iris_slice = df_iris[df_iris['species'].isin(input)]
	fig = px.histogram(
		df_iris_slice, x='sepal_width', color='species', nbins=40
	)
	fig.update_layout(barmode='overlay')
	fig.update_traces(opacity=0.75)
	fig.layout.title = "title1"
	fig.layout.paper_bgcolor = '#f2f2f2'
	fig.layout.plot_bgcolor = '#e1e1e1'
	return fig



if __name__ == '__main__':
	app.run_server(
		debug=True, # To automatically reload your changes in the online dashboard
	)