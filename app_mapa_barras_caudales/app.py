import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json


# Datos
df = pd.read_csv(r"data/geoquimica_limpio_index.csv")
df['tamaño'] = 50

lista_csv = [
    'data/data_baroa.csv', 
    'data/data_chilco.csv',
    'data/data_cipres.csv', 
    'data/data_cornou.csv',
    'data/data_tumbes.csv', 
    'data/data_vpinoh.csv',
    'data/data_vsur.csv'
]

nombres_caudales = [
    'Baroa Bajo',
    'El Chilco',
    'Los Cipreses',
    'Cerro Cornou',
    'San Juan Tumbes',
    'Pino Huacho',
    'Estrella Azul'
]

dfs = [pd.read_csv(nombre) for nombre in lista_csv]
dict_dfs = {nombre_hover: df for nombre_hover, df in zip(nombres_caudales, dfs)}


# Templates para gráfico
lista_templates = ['plotly', 'simple_white', 'plotly_dark', 'ggplot2']
lista_basemaps = ['open-street-map', 'satellite', 'carto-darkmatter']

"""############################################# Figuras preliminares ###############################################"""

# Figura mapa
latmax, latmin, lonmax, lonmin = df.N.max(), df.N.min(), df.E.max(), df.E.min()  # Limites mapa
latavg, lonavg = (latmax + latmin) / 2, (lonmax + lonmin) / 2  # Centro mapa

px.set_mapbox_access_token(open(".mapbox_token").read())

# Mapa Geoquimica
fig_mapa = px.scatter_mapbox(df, lat="N", lon="E",
                             size='tamaño',
                             size_max=7,
                             hover_name="nombre",
                             hover_data={'nombre': False, 'tamaño':False},
                             custom_data=["codigo"],
                             labels={'N': 'Lat', 'E': 'Lon'},
                             center={'lat': latavg, 'lon': lonavg},
                             mapbox_style='open-street-map',
                             opacity=1,
                             zoom=11)
fig_mapa.update_layout(margin=dict(l=15, r=25, t=5, b=5))
fig_mapa.layout.update(showlegend=False)

# Mapa caudales
df_xy = pd.read_csv('data/lonlat_caudales.csv')
df_xy['tamaño'] = 50
fig_mapa_2 = px.scatter_mapbox(df_xy, lat='lat', lon='lon',
                               hover_name='Nombre',
                               hover_data={'Nombre': False},
                               size='tamaño',
                               size_max=7,
                               custom_data=[nombres_caudales],
                               labels={'lat': 'Lat', 'lot': 'Lon'},
                               center={'lat': latavg, 'lon': lonavg},
                               opacity=1,
                               zoom=11,
                               mapbox_style='open-street-map')
fig_mapa_2.update_traces(marker=dict(color='red'))
fig_mapa_2.update_layout(margin=dict(l=15, r=25, t=5, b=5))
fig_mapa_2.update_layout(showlegend=False)


"""################################################ Dash app ########################################################"""


# Dash app
app = dash.Dash(__name__)
server = app.server

"""################################################ Layout ########################################################"""

app.layout = html.Div([

    dcc.Tabs(id='tabs', children=[

        # Tab 1 (geoquimica)
        dcc.Tab(id='tab_geoquimica',
                label='Geoquímica',
                children=[
                    html.Div([
                        html.Div([

                            html.Div([dcc.RadioItems(id='radio-basemap',
                                                     options=[{'label': basemap, 'value': basemap} for basemap in
                                                              lista_basemaps],
                                                     value='open-street-map')
                                      ], style={'display': 'flex', 'justifyContent': 'center',
                                                'marginTop': '5', 'marginBottom': '5'}),

                            html.Div([dcc.Graph(id='mapa',
                                                figure=fig_mapa,
                                                hoverData={'points': [{'customdata': ['PT01']}]},
                                                style={'width': '100%', 'height': '100%'}
                                                )
                                      ], style={'width': '100%', 'height': '89%'}),

                                    ], style={'display': 'flex', 'flex-direction': 'column',
                                              'position': 'relative', 'height': '100vh',
                                              'width': '60%'}),

                        html.Div([dcc.Graph(id='barras',
                                            hoverData={'points': [{'customdata': ['Baroa Bajo']}]}),
                                  html.H3('Estilo de gráfico'),
                                  dcc.Dropdown(id='dropdown-estilos',
                                               options=[{'label': estilo, 'value': estilo} for estilo in
                                                        lista_templates],
                                               value='plotly')], style={'width': '40%'})

                                ], style={'display': 'flex', 'alignItems': 'center'})
                ]),

        # Tab 2 (caudales)
        dcc.Tab(id='tab_caudales',
                label='Caudales',
                children=[
                    html.Div([
            html.Div([

                html.Div([dcc.RadioItems(id='radio-basemap_2',
                                         options=[{'label': basemap, 'value': basemap} for basemap in lista_basemaps],
                                         value='open-street-map')
                          ], style={'display': 'flex', 'justifyContent': 'center',
                                                'marginTop': '5', 'marginBottom': '5'}),

                html.Div([dcc.Graph(id='mapa_2',
                                    figure=fig_mapa_2,
                                    hoverData={'points': [{'customdata': ['Baroa Bajo']}]},
                                    style={'width': '100%', 'height': '100%'}
                                    )
                          ], style={'width': '100%', 'height': '89%'}),


                        ], style={'display': 'flex', 'flex-direction': 'column',
                                  'position': 'relative', 'height': '100vh',
                                  'width': '60%'}),

            html.Div([dcc.Graph(id='lines-caudal',
                                hoverData={'points': [{'customdata': ['Baroa Bajo']}]}),
                      html.H3('Estilo de gráfico'),
                      dcc.Dropdown(id='dropdown-estilos_2',
                                   options=[{'label': estilo, 'value': estilo} for estilo in lista_templates],
                                   value='plotly')], style={'width': '40%'})

                            ], style={'display': 'flex', 'alignItems': 'center'})
                        ])
            ])

                    ], style={'margin': 0, 'fontFamily': 'Lucida Sans'})


"""############################################### Callbacks ########################################################"""


# Actualizar basemap en mapa
@app.callback([Output('mapa', 'figure'),
              Output('mapa_2', 'figure')],
              [Input('radio-basemap', 'value'),
               Input('radio-basemap_2', 'value')])
def update_basemap(basemap, basemap2):
    fig_mapa.update_layout(mapbox_style=basemap)
    fig_mapa_2.update_layout(mapbox_style=basemap2)

    return fig_mapa, fig_mapa_2


# Actualizar figura barras
@app.callback(Output('barras', 'figure'),
              [Input('mapa', 'hoverData'),
               Input('dropdown-estilos', 'value')])
def update_barras(hoverData, estilo):
    """Recargar gráfico de barra en base a atributo de hover"""
    cod_muestra = hoverData['points'][0]['customdata'][0]# Codigo de muestra en hover
    filt = df.codigo == cod_muestra
    df_x_muestra = df.loc[filt]
    lista_valores = pd.Series(df_x_muestra.iloc[0, 4:-1])

    fig_barras = px.bar(x=['Na', 'K', 'Ca', 'Mg', 'Cl', 'HCO3', 'SO4', 'CO3', 'SiO2'],
                        y=lista_valores,
                        hover_name=['Na', 'K', 'Ca', 'Mg', 'Cl', 'HCO3', 'SO4', 'CO3', 'SiO2'],
                        title=cod_muestra,
                        template=estilo)
    fig_barras.update_layout(xaxis_title="Elemento", yaxis_title="Concentración (mg/L)")
    fig_barras.update_layout(title_x=.5, title_font_size=20)

    return fig_barras


# Serie de tiempo de caudales
@app.callback(Output('lines-caudal', 'figure'),
              [Input('mapa_2', 'hoverData'),
               Input('dropdown-estilos_2', 'value')])
def update_caudales(hoverData, estilo):
    """Recargar gráfico de caudales en base a hover"""
    nombre = hoverData['points'][0]['customdata'][0] # Nombre de df en hover
    fig_caudales = px.line(dict_dfs[nombre],
                           x='Fecha',
                           y='C (L/min)',
                           title=nombre,
                           template=estilo)
    fig_caudales.update_traces(mode='lines+markers')
    fig_caudales.update_layout(title_x=.5, title_font_size=20)
    fig_caudales.update_xaxes(tickformat="%d/%m/%y")

    return fig_caudales


if __name__ == '__main__':
    app.run_server(debug=False)