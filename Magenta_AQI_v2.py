# ----  importo librerie per i grafici ----
import pandas
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import date as dt
from datetime import date as dt, timedelta
import dash_daq as daq

# ------- questi servono per il google sheet -----
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# ------- collego il google sheet ---------
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Casa Magenta_Outdoor").sheet1  # Casa Magenta_soggiorno  #Casa Magenta_Outdoor #casa codini_esterno


sheet2 = client.open("Casa Magenta_soggiorno").sheet1


sheet3 = client.open(" Casa Magenta_cameretta").sheet1


sheet4 = client.open("casa codini_esterno").sheet1


sheet5 = client.open("Botte_Malvaglio_outdoor").sheet1


# ------------------ dash

app = Dash()

app.layout = html.Div(children=[
    html.H1(children='Magenta AQI',
            style={
                'textAlign': 'center',
                # 'color': colors['text']
            }
            ),

    html.Div(children='''
        Casa Andrea & Anita

        ''',
             style={
                 'textAlign': 'center'
                 # 'color': colors['text']
             }
             ),

    html.Div(children='''
        Sensore Balcone Sud/Ovest

        ''',
             style={
                 'textAlign': 'left'
                 # 'color': colors['text']
             }
             ),
    # -------------- DCC GRAPH METTO TUTTI I GRAPH-----------------------------
    dcc.Graph(
        id='graph',
    ),
    dcc.Graph(
       id='graph1',
    ),
    dcc.Graph(
        id='graph2',
    ),
    dcc.Graph(
        id='graph3',
    ),
    dcc.Graph(
        id='graph4',
    ),
    dcc.Graph(
        id='graph5',
    ),
    dcc.Graph(
        id='graph6',
    ),
    dcc.Graph(
        id='graph7',
    ),
# ----------  DCC INTERVAL --------- questo fa l'update della pagina

    dcc.Interval(
        id='interval-component',
        interval=1 * 1200000,  # in milliseconds
        n_intervals=0
    ),
])

# ------ range degli assi ----------------------------------------------


# ---- CALL BACK ----------------
@app.callback(
    Output(component_id='graph', component_property='figure'),
    Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='graph3', component_property='figure'),
    Output(component_id='graph4', component_property='figure'),
    Output(component_id='graph5', component_property='figure'),
    Output(component_id='graph6', component_property='figure'),
    Output(component_id='graph7', component_property='figure'),
    [Input(component_id='interval-component', component_property='n_intervals')]
)

# --- CALL BACK FUNCTION --------------------

def refresh_page(n):
    data = sheet.get_all_records()

    sg = sheet2.get_all_records()

    sc = sheet3.get_all_records()

    cc = sheet4.get_all_records()

    bb = sheet5.get_all_records()

    # ---------------- definisco il data frame con panda -----------
    df = pd.DataFrame(data)
    dfg = pd.DataFrame(sg)
    dfc = pd.DataFrame(sc)
    dfcc = pd.DataFrame(cc)
    dfbb = pd.DataFrame(bb)

    # -----  balcone

    PM10balcone = df['PM10 [µg/m³]'].iat[-1]
    PM25balcone = df['PM25 [µg/m³]'].iat[-1]
    TEMPbalcone = df['T [°C]'].iat[-1]

    # ----------- soggiorno

    PM10soggiorno = dfg['PM10 [µg/m³]'].iat[-1]
    PM25soggiorno = dfg['PM25 [µg/m³]'].iat[-1]
    TEMPsoggiorno = dfg['T [°C]'].iat[-1]
    CO2soggiorno = dfg['Co2 [ppm]'].iat[-1]

    # ---- cameretta

    PM10cameretta = dfc['PM10 [µg/m³]'].iat[-1]
    PM25cameretta = dfc['PM25 [µg/m³]'].iat[-1]
    TEMPcameretta = dfc['T [°C]'].iat[-1]
    CO2cameretta = dfc['Co2 [ppm]'].iat[-1]

    # ---- botte
    TEMPBOTTE = dfbb['tbotteout'].iat[-1]

    # ----- print delle variabili ---
    pprint(PM10balcone)
    pprint(PM25balcone)
    pprint(TEMPbalcone)
    pprint(PM10soggiorno)
    pprint(PM25soggiorno)
    pprint(TEMPsoggiorno)
    pprint(CO2soggiorno)
    pprint(PM10cameretta)
    pprint(PM25cameretta)
    pprint(TEMPcameretta)
    pprint(CO2cameretta)
    pprint(TEMPBOTTE)
    df.info()




    fig = go.Figure()
    # ------- indicator balcone --------------------------------------------------

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=TEMPbalcone,
        title={"text": "T [°C]"},
        domain={'y': [0, 0.10], 'x': [0.00, 0.25]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=PM10balcone,
        delta={"reference": 50, "valueformat": ".0f"},
        title={"text": "PM10 [µg/m³]"},
        domain={'y': [0, 0.10], 'x': [0.25, 0.30]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=PM25balcone,
        delta={"reference": 35, "valueformat": ".0f"},
        title={"text": "PM25 [µg/m³]"},
        domain={'y': [0, 0.10], 'x': [0.30, 0.55]})),

    # --- soggiorno -----------------------------------------------------

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=TEMPsoggiorno,
        title={"text": "T [°C]"},
        domain={'y': [0.30, 0.60], 'x': [0.00, 0.25]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=PM10soggiorno,
        delta={"reference": 50, "valueformat": ".0f"},
        title={"text": "PM10 [µg/m³]"},
        domain={'y': [0.30, 0.60], 'x': [0.25, 0.30]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=PM25soggiorno,
        delta={"reference": 35, "valueformat": ".0f"},
        title={"text": "PM25 [µg/m³]"},
        domain={'y': [0.30, 0.60], 'x': [0.30, 0.55]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=CO2soggiorno,
        title={"text": "PPM"},
        domain={'y': [0.30, 0.60], 'x': [0.55, 0.60]})),

    # ---- cameretta ----------------------------------------------------------

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=TEMPcameretta,
        title={"text": "T [°C]"},
        domain={'y': [0.75, 1], 'x': [0.00, 0.25]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=PM10cameretta,
        delta={"reference": 50, "valueformat": ".0f"},
        title={"text": "PM10 [µg/m³]"},
        domain={'y': [0.75, 1], 'x': [0.25, 0.30]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=PM25cameretta,
        delta={"reference": 35, "valueformat": ".0f"},
        title={"text": "PM25 [µg/m³]"},
        domain={'y': [0.75, 1], 'x': [0.30, 0.55]})),

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=CO2cameretta,
        title={"text": "PPM"},
        domain={'y': [0.75, 1], 'x': [0.55, 0.60]})),
    fig1 = px.line(df, x='Data', y=['PM10 [µg/m³]', 'PM25 [µg/m³]'],
                   color_discrete_sequence=px.colors.qualitative.Plotly,
                   title="Balcone Sud/Ovest")
    fig2 = px.line(dfg, x='quando', y=['PM10 [µg/m³]', 'PM25 [µg/m³]'], title="Soggiorno")
    fig3 = px.line(df, x='Data', y='T [°C]', title="Balcone Sud/Ovest")
    fig4 = px.line(dfg, x='quando', y='T [°C]', title="Soggiorno")
    fig5 = px.line(dfcc, x='quando', y=['PM10 [µg/m³]', 'PM2,5 [µg/m³]'], title="Malvaglio Outdoor")
    fig6 = px.line(dfbb, x='Data', y='tbotteout', title="Temperatura Casetta Botte")
    fig7 = px.line(dfcc, x='quando', y='T [°C]', title="Temperatura Malvaglio Esterna")
    # ------ range degli assi ----------------------------------------------

    fig1.update_yaxes(range=[0, 120], fixedrange=True)
    fig2.update_yaxes(range=[0, 60], fixedrange=True)
    fig5.update_yaxes(range=[0, 80], fixedrange=True)
    fig.update_layout(
        grid={'rows': 1, 'columns': 4, 'pattern': "independent"})
    fig.update_traces(title_font_size=18, number_font_size=30)  # dimensione font degli indicator

    return fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7




# ------ END CALL BACK -------


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

