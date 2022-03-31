import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import json

df = pd.read_csv("an_municipios.csv",
                 dtype={"Município": str})
df.drop(columns=['Unnamed: 0', "Unnamed: 0.1", "Unnamed: 0.2"], inplace=True)

df.columns = ["Escala", "Referêcia", "codibge", "Anomalia", "Município", "SIGLA", "AREA", "Nome", "Porcentagem"]
geojson = json.load(open("geojson_municipios.geojson"))
coluna = {
    "Nome": False, "Município": True, "Anomalia": False, "Porcentagem": True
}

# In[ ]:


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Anomalias", className="display-4"),
        html.Hr(),
        html.P(
            "Valores de anomalia de chuva no Paraná", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Munucipíos", href="/", active="exact"),
                dbc.NavLink("Bacias", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

dropdown1 = html.Div([

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "Janeiro 2022", "value": "jan./2022"},
                     {"label": "Fevereiro 2022", "value": "fev./2022"},
                     {"label": "Março 2022", "value": "mar./2022"}],
                 multi=False,
                 value="jan./2022",
                 style={'width': "40%", 'margin-left': 150, },

                 )])

dropdown2 = html.Div([

    dcc.Dropdown(id="Escala",
                 options=[
                     {"label": "Mensal", "value": "Mensal"},
                     {"label": "Trimestral", "value": "Trimestral"},
                     {"label": "Semestral", "value": "Semestral"}],
                 multi=False,
                 value="Mensal",
                 style={'width': "40%", 'margin-left': 150, },

                 )])

explicando = html.Div(id="text", children="texto")

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),

    sidebar,
    html.H1("Dados por Municipios", style={'text-align': 'center'}),
    dropdown1,
    dropdown2,
    explicando,
    content,
    html.Br(),
])


@app.callback(
    [Output("page-content", "children"), ],
    [Input("url", "pathname"),
     Input(component_id='slct_year', component_property='value'),
     Input(component_id='Escala', component_property='value')]

)
def render_page_content(pathname, slct_year, Escala):
    if pathname == "/":
        dff = df.copy()
        dff = dff[dff["Referêcia"] == slct_year]
        dff = dff[dff["Escala"] == Escala]
        figure = px.choropleth_mapbox(dff, geojson=geojson, color="Anomalia",
                                      locations="Nome", featureidkey="properties.Município",
                                      center={"lat": -24.8, "lon": -51},
                                      color_continuous_scale=px.colors.diverging.BrBG,
                                      color_continuous_midpoint=0,
                                      hover_data=coluna,
                                      opacity=0.8,
                                      mapbox_style="carto-positron", zoom=5.8)
        figure.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10})
        return [dcc.Graph(id='my_bee_map', figure=figure)]

#
if __name__=='__main__':
    app.run_server(debug=False, port=3000)
