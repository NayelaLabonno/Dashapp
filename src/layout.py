""" 
Defines app layout with two tabs, one for process overview,
another for instance details like kpis, stage-gate diagram etc. 
"""

import dash
from dash import dcc, html

def get_options(case_id_list):

    # returns a list of dictionary for case id selector dropdown
    case_id_options = []
    for i in case_id_list:
        case_id_options.append({'label': i, 'value': i})
    return case_id_options


def get_layout(app,new_dataframe):
    layout=html.Div(children=[
        html.Div(className='row',
                children=[
                    html.Div(className='two columns div-user-controls',
                            children=[
                                html.H1('BPM-I4.0', style={'color': '#000000'}),
                                html.H2('Übersicht über aktuelle Instanzen',
                                        style={'color': '#000000'}),
                                html.P(
                                    'Select a case id and switch tab to get instance overview', style={'color': '#000000'}),
                                html.Div(
                                    className='div-for-dropdown bg-blue',
                                    children=[
                                        dcc.Dropdown(id='caseselector', options=get_options(new_dataframe['Case ID'].unique()), value=[new_dataframe['Case ID'].sort_values()[0]],
                                                        style={
                                                            'backgroundColor': '#dde4eb'},
                                                        className='caseselector #dde4eb'
                                                    ),
                                    ],
                                    style={'color': 'dde4eb'}),
                            ]
                            ),
                    html.Div(className='ten columns div-for-charts bg-white',
                            children=[     
                                # Initializing the tabs with process overview tab as default tab
                                dcc.Tabs(id='process-tabs', value='tab-1', children=[
                                    dcc.Tab(id='tab1', value='tab-1', label='Processes', children=[
                                            html.Div(className='bg-white', children=[
                                                html.H3('Ongoing Processes', style={
                                                        'color': '#000000'}),
                                                dash.dash_table.DataTable(
                                                    id="table",
                                                    columns=[{"name": c, "id": c}
                                                            for c in new_dataframe.loc[new_dataframe['Case ID'] == 'EC00005299', ['Case ID', 'Name', 'Start Time', 'Total Leadtime']]],
                                                    data=new_dataframe.to_dict(
                                                        "records"),
                                                    style_header={
                                                        'backgroundColor': '#dde4eb',
                                                        'color': 'black'
                                                    },
                                                    style_data={
                                                        'backgroundColor': 'white',
                                                        'color': 'black',
                                                        'border': 'none'
                                                    },
                                                    page_size=15,
                                                    sort_action="native",
                                                )
                                            ])
                                            ]),
                                    dcc.Tab(id='tab2', value='tab-2', label='Instance Detail', children=[
                                        html.H1('Stage-Gate View',
                                                style={'color': '#000000'}),
                                        html.Div(className='twelve columns div-for-gate-view bg-blue',
                                                # Div for stage-gate view with empty children, children is a graph returned from callback function
                                                id='stage-gate-view',
                                                ),
                                        html.P(
                                            'Select four KPI types from the list below', style={'color': '#000000'}),
                                        dcc.Dropdown(
                                            id='kpiselector', multi=True),
                                        html.H3(
                                            'Instance Specific KPIs', style={'color': '#000000'}),
                                        html.Div([
                                            html.Div(className='div-for-kpi bg-blue', children=[html.Div(id='kpi1')]),
                                            html.Div(className='div-for-kpi bg-blue', children=[html.Div(id='kpi2')])]),
                                        html.Div([
                                            html.Div(className='div-for-kpi bg-blue', children=[html.Div(id='kpi3')]),
                                            html.Div(className='div-for-kpi bg-blue', children=[html.Div(id='kpi4')])])

                                    ])
                                ]
                                )])
                ])])
    return layout