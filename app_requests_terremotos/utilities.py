import requests
import pandas as pd
import plotly.express as px
import dash_table

def get_earthquake_df(magnitud=4.5, intervalo='day'):
    """
    magnitud: int 
        Choice between 1, 2.5 or 4.5, that represents the minimun value
        to filter the earthquakes. Defaults to events greater that 4.5.
    intervalo: str
        Choice between "hour", "day", "week" and "month" that defines 
        the max time interval for the events. Defaults to last day.

    Returns
    -------
    Python dictionary    
    """
    
    # request the API with the given parameters
    request = requests.get(f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{magnitud}_{intervalo}.geojson")
    
    # convert response to a dictionary
    request_dict = request.json()

    df = pd.json_normalize(data=request_dict, record_path='features', errors='ignore')
    df.columns = df.columns.str.replace('properties.', '', regex=False)
    df.columns = df.columns.str.replace('geometry.', '', regex=False)

    df = df[['mag', 'place', 'time', 'tz', 'type', 'title', 'coordinates']] # Filtrando columnas relevantes
    df['time'] = pd.to_datetime(df['time'], unit='ms', origin='unix') # Unix time to datetime Series

    # unpacking the geometry in coordinates
    df_geometry = df['coordinates'].apply(pd.Series) # unpack coordinates
    df_geometry = df_geometry.rename(columns={0: 'lon', 1: 'lat', 2: 'depth'}) # rename columns

    # df.head()
    df = df.join(df_geometry)
    df.head()
    
    return df, magnitud, intervalo

def plot_map(df):
    fig = px.scatter_mapbox(df, lat='lat', lon='lon', 
                            size='mag',
                            size_max=15,
                            color='mag',
                            color_continuous_scale='viridis_r',
                            hover_data={'mag': True, 'time': True},
                            hover_name='title',
                            mapbox_style='carto-positron',
                            opacity=0.65,
                            zoom=0)
    fig.update_layout(
        title={
            'x': 0.5
        },
        font={
            'size': 16
        },
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
            )
        )

    fig.update_coloraxes(
    colorbar={
        'x': 1,
        'y': .5,
        'bgcolor': 'rgba(255, 255, 255, 1)'
            }
        )
    
    return fig

def plot_table(df):
    df = df[['place', 'mag']]

    df = df.sort_values(by='mag', ascending=False)

    return dash_table.DataTable(
        id='dash-table',
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_table={ 'maxHeight': '95vh','overflowX':'auto', 'overflowY': 'auto'},
        filter_action="native",
        page_action="native",
        page_current=0,
        page_size=15,
        style_cell={
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_data={                
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    )