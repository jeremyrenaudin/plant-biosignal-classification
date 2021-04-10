import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import os
from dash.dependencies import Output, Input

root_data = "D:/"
plant_ids = []

for file in os.listdir(root_data):
    if (file.endswith(".parquet")) and (file not in plant_ids):
        file = file.replace(".parquet", "")
        plant_ids.append(file)

anonym_plant = [f"Plant {i}" for i in range(1, len(plant_ids) + 1)]
excel_label = pd.read_excel("D:/signal_labelling/signal_labelling.xlsx")
excel_label["anonym_name"] = ""

root = "C:/Users/Lenovo/Documents/Vivent/vivent_project/dataset_vivent/"

for plant_id, anonym_name in zip(plant_ids, anonym_plant):
    for i, value in enumerate(excel_label["plant_id"].values):
        if value == plant_id:
            excel_label.loc[i, "anonym_name"] = anonym_name

print(excel_label.head())

data = pd.DataFrame()
for i, plant_id in enumerate(plant_ids[:2]):
    df = pd.read_parquet(root, filters=[("plant_id","==",plant_id)])
    df["anonym_plant"] = anonym_plant[i]
    data = data.append(df)

data.sort_values(by=["plant_id", "timestamp"], inplace=True, ignore_index=True)
data["mV"].fillna(0, inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "LabelApp: Let's classify your signal!"

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🌿", className="header-emoji"),
                html.H1(
                    children="Signal classify'app", className="header-title"
                ),
                html.P(
                    children="Master your signal labelling !",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Plant", className="menu-title"),
                        dcc.Dropdown(
                            id="plant-filter",
                            options=[
                                {"label": plant_name, "value": plant_name}
                                for plant_name in data.anonym_plant.unique()
                            ],
                            value="Plant 1",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.timestamp.min().date(),
                            max_date_allowed=data.timestamp.max().date(),
                            start_date=data.timestamp.min().date(),
                            end_date=data.timestamp.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="signal-chart", config={"displayModeBar": True},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dash_table.DataTable(
                        id='label-table',
                        columns=[
                            {'id': col, 'name': col} for col in excel_label.columns[:2]
                            ],
                        # data=excel_label.to_dict("records"),
                        editable=True
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [
        Output("date-range", "start_date"),
        Output("date-range", "end_date")
    ],
    [
        Input("plant-filter", "value"),
    ],
)
def update_datepicker(plant):
    mask = (data.anonym_plant == plant)
    filtered_data = data.loc[mask, :]
    min_date_signal = filtered_data.timestamp.min().date()
    max_date_signal = filtered_data.timestamp.max().date()

    return min_date_signal, max_date_signal

@app.callback(
    Output("signal-chart", "figure"),
    [
        Input("plant-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(plant, start_date, end_date):
    mask = (
        (data.anonym_plant == plant)
        & (data.timestamp.dt.normalize() >= start_date)
        & (data.timestamp.dt.normalize() <= end_date)
    )
    filtered_data = data.loc[mask, :]
    signal_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["mV"],
                "type": "lines",
                "hovertemplate": "%{y:.2f} mV<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Biosignal (in millivolt)",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": False},
            "yaxis": {"ticksuffix": "mV", "range": [-100, 100]},
            "colorway": ["#17B897"],
        },
    }
    return signal_chart_figure

@app.callback(
    Output("label-table", "data"),
    [
        Input("plant-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def filter_table(plant, start_date, end_date):
    mask = (
        (excel_label.anonym_name == plant)
        & (excel_label.date >= start_date)
        & (excel_label.date <= end_date)
    )
    filtered_data = excel_label.loc[mask, ["date", "signal_quality"]]
    return filtered_data.to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)