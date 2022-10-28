""" 
Initialize dash app, sets layout and 
assigns callbacks to the app 
"""

import pandas as pd 
from dash import Dash
from settings import kpi_columns
from layout import get_layout
from callbacks import get_callbacks


dataframe = pd.read_csv("~/projects/process-assistent/data/WDM_final.csv")      # Loads dataframe
relevant_columns = ["cdb_ec_id", "case:concept:name", "case:start_timestamp", "case:total_leadtime", "case:start_division", "case:throughput_time"]
case_id = 'cdb_ec_id'
new_dataframe = dataframe.groupby(by=case_id)[relevant_columns].agg(pd.Series.mode).reset_index(drop=True)
new_dataframe.rename(columns=kpi_columns, inplace=True)     # renames relevant columns for better user view 

app = Dash(__name__)
app.layout=get_layout(app,new_dataframe)
get_callbacks(app,dataframe,case_id,new_dataframe)

if __name__ == '__main__':
    app.run_server()
