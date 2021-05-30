from functools import partial

import pandas as pd

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

from utilities import get_earthquake_df, plot_map, plot_table

df = get_earthquake_df()[0]

fig = plot_map(df)

tabla = plot_table(df)


app = dash.Dash(__name__)

app.layout = html.Div(children=[
	html.Div([tabla], id='tabla', className='tabla-dash'),
	html.Button('>', id='hide-table', className='btn-hide'),
	html.Div([
		html.Div([
			html.Div([
				html.H3('Magnitud Máxima'),
			    dcc.Dropdown(
			        id='dropdown-mag',
			        options=[
			            {'label': '1.0', 'value': 1.0},
			            {'label': '2.5', 'value': 2.5},
			            {'label': '4.5', 'value': 4.5}
			        	],
			        value=4.5
		    		)
			    ], className='dropdown-item'),
			html.Div([
			    html.H3('Intervalo máximo'),
			    dcc.Dropdown(
			        id='dropdown-tiempo',
			        options=[
			            {'label': 'Hora', 'value': 'hour'},
			            {'label': 'Día', 'value': 'day'},
			            {'label': 'Semana', 'value': 'week'},
			            {'label': 'Mes', 'value': 'month'}
			        	],
			        value='day'
			    	)
			    ], className='dropdown-item')
			], className='div-dropdowns'),
		dcc.Graph(id='mapa', figure=fig, style={'margin': '0', 'height':'100%'})
	], className="div-contenido", id="div-contenido"),
], style={'height': '85vh', 'display': 'flex'})


@app.callback(
    [Output(component_id='mapa', component_property='figure'),
    Output(component_id='tabla', component_property='children')],
    [Input(component_id='dropdown-mag', component_property='value'),
    Input(component_id='dropdown-tiempo', component_property='value')]
)
def update_map_mag(mag, t):

	mag = float(mag)

	df = get_earthquake_df(magnitud=mag, intervalo=t)[0]

	fig = plot_map(df)
	tabla = plot_table(df)

	return fig, tabla

@app.callback(
    [Output(component_id='tabla', component_property='style'),
    Output(component_id='div-contenido', component_property='style')],
    [Input(component_id='hide-table', component_property='n_clicks')]
)
def hide_table(n_clicks):
	if n_clicks:
		if n_clicks%2 == 0:
			return {"width": "15rem"}, {'width': 'calc(100vw - 15rem - 35px)'}
		else:
			return {"width": "0"}, {"width": "100vw"}

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True)