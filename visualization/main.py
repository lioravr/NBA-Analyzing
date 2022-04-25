from fastapi import FastAPI
import requests
import pandas as pd
from pandas import merge
from copy import deepcopy
import plotly.express as px


app = FastAPI()
@app.get("/gen_scoring_efficiency_plot/select_year={selected_year}")
async def ttt(selected_year:int):
    x= gen_scoring_efficiency_plot(selected_year)
    return x.to_json()
def gen_scoring_efficiency_plot(season):
    """
    Generates points per 75 x TS% plot
    """

    per_100_standing = requests.get(f"http://backend:8000/get_player_data/season={season}&category=per_poss")
    per_100_standing=deepcopy(pd.read_json(per_100_standing.json()))

    
    advanced_standing = requests.get(f"http://backend:8000/get_player_data/season={season}&category=advanced")
    advanced_standing=pd.read_json(advanced_standing.json())
    
    # Calculating points per 75 
    per_100_standing['PTS'] = per_100_standing['PTS'].apply(lambda x: x*.75)
    per_75_standing = per_100_standing    
    avg_ts_percentage = round(advanced_standing['TS%'].mean(), 3)
    combined = merge(per_75_standing, advanced_standing, on='Player', suffixes=('', '_y'))
    
    # Plottings data
    fig = px.scatter(data_frame=combined, x='PTS', y='TS%',
                     hover_name='Player',
                     color='Pos',
                     range_x=[0, 40],
                     opacity=.65,
                     template="plotly_dark")

    
    fig.add_hline(y=avg_ts_percentage, 
                  line_width=2, 
                  line_dash="dash", 
                  line_color="gray",
                  opacity=.5,
                  annotation_text=f"League Avg.={avg_ts_percentage}",
                  annotation_position="bottom right")

    fig.update_xaxes(
        title_text = "Pts. per 75",
        title_font = {"size": 15},
        title_standoff = 20,
        showgrid = True,
        showline = True,
        showticklabels = True,
        zeroline = True
    )

    fig.update_yaxes(
        title_text = "TS%",
        title_font = {"size": 15},
        title_standoff = 20,
        showgrid = True,
        showline = True,
        showticklabels = True,
        zeroline = True
    )
    
    return fig