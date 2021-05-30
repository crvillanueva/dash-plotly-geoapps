import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Carga datos
df_elementos = pd.read_csv(r"data/meq_cerror.csv")
df_elementos = df_elementos.drop('Unnamed: 0', axis=1)

# Figura inicial
fig = px.scatter(df_elementos, x="Cl", y="Na",
                 hover_name='codigo',
                 trendline='ols',
                 title='Gráfico de correlación bivariada',
                 trendline_color_override='#ff8080'
                 )
fig.update_xaxes(title={'font':{'size':22}})
fig.update_yaxes(title={'font':{'size':22}})
fig.update_layout(title={'x': 0.5})


"""################################################# App ############################################################"""

app = dash.Dash(__name__)
server = app.server

"""################################################# Layout #########################################################"""

app.layout = html.Div(

    [html.Div([
        # Dropdown de columnas
        html.Div(
            [
                html.H3('Eje X'),
                dcc.Dropdown(id='x_col',
                             options=[{'label': value, 'value': value} for value in df_elementos.columns],
                             value='Cl'),
                dcc.RadioItems(id='x_modo',
                               options=[{'label': 'Linear', 'value': "Linear"}, {'label': 'Log', 'value': "Log"}],
                               value="Linear", style={'textAlign': 'center'})
            ], style={'width':'48%'}
        ),
        html.Div(
            [
                html.H3('Eje Y'),
                dcc.Dropdown(id='y_col',
                             options=[{'label': value, 'value': value} for value in df_elementos.columns],
                             value='Na'),
                dcc.RadioItems(id='y_modo',
                               options=[{'label': 'Linear', 'value': "Linear"}, {'label': 'Log', 'value': "Log"}],
                               value="Linear", style={'textAlign': 'center'})
            ], style={'width':'48%'}
                )

                ], style={'display': 'flex', 'justifyContent': 'center', 'textAlign': 'center', 'height': '20vh'}
                ),

    html.Div([
        # Grafico scatter
        html.Div([
            dcc.Graph(id='scatter-reg',
                      figure=fig,
                      children=[],
                      style={'height': '100%'}
                      ),
                ], style={'width': '80%', 'height': '100%'}),

        # Opciones: Input, regresion y dropdown muestras
        html.Div([
            html.H4('Eliminar muestra con un error (%) mayor a: '),
            dcc.Input(id='input-error',
                      type='number',
                      value=30),
            html.Div(
                [html.H4('Línea de regresion (R2)'),
                 dcc.RadioItems(id='check-regresion',
                                options=[{'label': 'Si', 'value': 'Activado'},
                                         {'label': 'No', 'value': 'No activada'}],
                                value='Activado')
                 ]
                    ),
            html.Hr(style={'size': '0.2px', 'color': 'grey'}),
            html.H4('Muestras activas'),
            dcc.Dropdown(id='muestras_activas',
                         options=[{'label': muestra, 'value': muestra} for muestra in df_elementos['codigo'].unique()],
                         value=df_elementos['codigo'].unique(),
                         multi=True)
                ], style={'width': '20%'})
            ], style={'display': 'flex', 'height': '80vh', 'width': '100%', 'alignItems': 'center'})

    ], style={'fontFamily': 'Lucida Sans'})

"""############################################### Callbacks ########################################################"""

@app.callback(
    [Output('muestras_activas', 'options'),
    Output('muestras_activas', 'value')],
    [Input('input-error', 'value')])
def filtrar_df(error):
    if error is None:
        dash.exceptions.PreventUpdate
    else:
        dfferror = df_elementos.copy()
        filtro = dfferror.err < error
        dfferror = dfferror.loc[filtro]
        opciones = [{'label': value, 'value': value} for value in dfferror['codigo'].unique()], dfferror['codigo'].unique()


        return opciones


@app.callback(
    Output('scatter-reg', 'figure'),
    [Input('x_col', 'value'),
     Input('y_col', 'value'),
     Input('x_modo', 'value'),
     Input('y_modo', 'value'),
     Input('check-regresion', 'value'),
     Input('muestras_activas', 'value')])
def actualizar_grafico(columna_x, columna_y, x_axis_mode, y_axis_mode, checklist_regresion, muestra_activa):
    df_filtrado = df_elementos.copy()
    df_filtrado = df_filtrado.set_index('codigo')
    df_filtrado = df_filtrado.loc[muestra_activa]

    scatter = px.scatter(df_filtrado, x=columna_x, y=columna_y,
                         hover_name=df_filtrado.index,
                         hover_data={'err': True},
                         trendline='ols' if checklist_regresion == 'Activado' else None,
                         title='Gráfico de correlación bivariada',
                         trendline_color_override='#ff8080',
                         )

    scatter.update_layout(title_x=0.5)

    # Set tipo de 
    scatter.update_xaxes(title={'text': (columna_x + ' (meq/L)'), 'font':{'size':20}}, type='linear' if x_axis_mode == 'Linear' else 'log')
    scatter.update_yaxes(title={'text': (columna_y + ' (meq/L)'), 'font': {'size': 20}}, type='linear' if y_axis_mode == 'Linear' else 'log')

    # Cambiando estilo de marcadores y linea de regresión
    scatter.update_traces(marker_line_width=1, marker_size=10, selector=dict(type="scatter", mode="markers"))
    scatter.update_traces(line=dict(dash="dot", width=2), selector=dict(type="scatter", mode="lines"))


    return scatter


if __name__ == '__main__':
    app.run_server(debug=False)