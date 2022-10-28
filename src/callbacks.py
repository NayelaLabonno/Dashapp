import pandas as pd
from dash.dependencies import Input, Output
from dash import html
import dash_cytoscape as cyto


def get_callbacks(app,dataframe,case_id,new_dataframe):

# Callback functions to return four KPIs to html divs
    @ app.callback(Output('kpi1', 'children'),
                [Input('kpiselector', 'value')])
    def update_kpis(selected_kpi_value):
        div = html.H3(selected_kpi_value[0], style={'color': '#000000'})
        return div


    @ app.callback(Output('kpi2', 'children'),
                [Input('kpiselector', 'value')])
    def update_kpis(selected_kpi_value):
        div = html.H3(selected_kpi_value[1], style={'color': '#000000'})
        return div


    @ app.callback(Output('kpi3', 'children'),
                [Input('kpiselector', 'value')])
    def update_kpis(selected_kpi_value):
        div = html.H3(selected_kpi_value[2], style={'color': '#000000'})
        return div


    @ app.callback(Output('kpi4', 'children'),
                [Input('kpiselector', 'value')])
    def update_kpis(selected_kpi_value):
        div = html.H3(selected_kpi_value[3], style={'color': '#000000'})
        return div


    """ 
    First output of the callback function returns the kpi dropdown options with label and values
    and the second output returns the four default kpi values
    """
    @ app.callback([Output('kpiselector', 'options'),
                Output('kpiselector', 'value')],
                [Input('caseselector', 'value')])
    def update_kpi_dropdown(selected_case_id):
        options_list = []
        value_list = []
        if case_id.startswith("case:"):
            relevant_columns = (
                [col for col in dataframe if col.startswith("case:")])
        else:
            relevant_columns = [case_id] + \
                ([col for col in dataframe if col.startswith("case:")])
        kpi_dataframe = dataframe.groupby(by=case_id)[relevant_columns].agg(
            pd.Series.mode).reset_index(drop=True)
        kpi_dataframe.rename(columns={'cdb_ec_id': 'Case ID', 'case:start_division': 'Start Division', 'case:total_leadtime': 'Total Leadtime',
                                    'case:throughput_time': 'Throughput Time', 'case:concept:name': 'Name', 'case:start_timestamp': 'Start Time'}, inplace=True)
        if len(selected_case_id) != 0:
            kpi_options = kpi_dataframe.loc[kpi_dataframe['Case ID'].unique(
            ) == selected_case_id]
            options_dict = kpi_options.to_dict('records')[0]
            for key in options_dict:
                options_list.append({'label': key, 'value': options_dict[key]})
            kpi_values = new_dataframe.loc[new_dataframe['Case ID'].unique(
            ) == selected_case_id]
            values_dict = kpi_values.to_dict('records')[0]
            for key in values_dict:
                value_list.append(values_dict[key])
        return options_list, value_list[:4]


    # Callback function that creates stage-gate view as a graph
    @ app.callback(Output('stage-gate-view', 'children'),
                [Input('caseselector', 'value')])
    def update_gate_view(selected_case_id):
        if selected_case_id != None:
            gate_column = "concept:name"
            gates_list = ['Review & Release Gate 6&7',
                        'Review & Release Gate 8',
                        'Review & Release Gate 9']
            process_instance = selected_case_id
            gate_dataframe = pd.DataFrame(gates_list, columns=["Source Gates"])
            
            gate_dataframe['Target Gates'] = gate_dataframe['Source Gates'].shift(
                -1)     # For the stage gate view graph, source and target nodes are defined                       
            gate_dataframe['Gate Label'] = gate_dataframe['Source Gates'].str[17:]  # Selects shorter gate names as node labels
            gate_dataframe["Completed"] = 0
            gate_dataframe["x_position"] = 0
            gate_dataframe["y_position"] = 0
            x = 10
            y = 10
            for idx, gate in enumerate(gate_dataframe["Source Gates"]):
                # For each given gate, check whether that gate is present in the event log for the given ECID
                # If the gate has accured in the event log, then the completed column is set to 1, otherwise 0
                if gate in dataframe[dataframe[case_id].apply(lambda x: x == process_instance)][gate_column].unique():
                    gate_dataframe.loc[idx, ("Completed")] = 1
                    # Defines the placement of the gate nodes with x and y coordinates value
                    gate_dataframe.loc[idx, ("x_position")] = x     
                    gate_dataframe.loc[idx, ("y_position")] = y
                x += 120
            nodes = [
                {
                    'data': {'id': id, 'label': label, 'done': completed},
                    'position': {'x': x, 'y': y},
                }
                for id, label, completed, x, y in gate_dataframe[['Source Gates', 'Gate Label', 'Completed', 'x_position', 'y_position']].apply(tuple, axis=1)]
            edges = [
                {'data': {'source': source, 'target': target}
                }
                for source, target in gate_dataframe[['Source Gates', 'Target Gates']].apply(tuple, axis=1)
            ]
            # change node complete status for stage gate view mockup
            # nodes[1]['data']['done'] = 0
            # nodes[2]['data']['done'] = 0
            graph = cyto.Cytoscape(
                id='cyto-gate-view',
                layout={'name': 'preset'},
                elements=nodes+edges[:-1],
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'content': 'data(label)'
                        }
                    },
                    {
                        # Nodes that are complete will have a darker shade
                        'selector': '[done!=0]',
                        'style': {
                            'background-color':  '#000000'
                        }
                    },
                    {
                        'selector': '.light-nodes',
                        'style': {
                            'background-color': 'rgb(228, 220, 220)'
                        }
                    }])
            return graph
