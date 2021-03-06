# dash-plotly-geoapps
Repo compilatorio del código fuente de aplicaciones geológicas interactivas creadas con [Dash](https://plotly.com/dash/). Entre las aplicaciones encontramos:

## Dashboards caudales y gráfico de barras de elementos mayores

https://user-images.githubusercontent.com/69276157/120119104-deded280-c163-11eb-94bf-bdbed477f172.mp4

Live link: https://mapa-em-caudales-vertientes.herokuapp.com/

Dashboard que muestra la ubicación de muestras hidrogeoquímicas y sus concentraciones de elementos mayores, además de los caudales medidos en un estudio hidrogeológico en la península de Tumbes. Para poder ver el mapa satelital necesitas tu propio [token de mapbox](https://docs.mapbox.com/api/accounts/tokens/) en la sección "set_mapbox_access_token" del código.

## Dashboard para análisis de correlación de elementos con un diagrama scatter

https://user-images.githubusercontent.com/69276157/120119230-89ef8c00-c164-11eb-9a21-8e3becb79e85.mp4

Live link: https://vertientes-scatter-reg.herokuapp.com/

Dashboard que permite ver un diagrama binario para analizar las relaciones entre elementos. Es posible filtrar muestras con un % de error en el balance iónico de un valor arbitrario, además de quitar muestras en específico.

## Dashboard terremotos

https://user-images.githubusercontent.com/69276157/120117950-e13e2e00-c15d-11eb-808c-2d716510d47e.mp4

Dashboard con ubicación y magnitud de los sismos más recientes. Realizado a partir de información obtenida desde la [API de la USGS](https://earthquake.usgs.gov/fdsnws/event/1/).
