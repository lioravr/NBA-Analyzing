import requests
import streamlit as st
import os
from PIL import Image
import pandas as pd
script_directory = os.getcwd()
PROGRESS_BAR_CUSTOM_COLOR = '#f63366'

import plotly.io as pio
pio.renderers.default = "notebook"


def translate_standing_type(stat_type):
    if stat_type == 'per_game':
        return 'Per Game'
    elif stat_type == 'totals':
        return 'Total'
    elif stat_type == 'per_minute':
        return 'Per 36 Minutes'
    elif stat_type == 'advanced':
        return 'Advanced'    
    elif stat_type == 'per_poss':
        return 'Per 100 Possessions'    
    elif stat_type == 'play-by-play':
        return 'Play-by-Play'
    elif stat_type == 'advanced_box_score':
        return 'Advanced Box Score'
    return 'None'


def ordinal(n): return "%d%s" % (
    n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


STANDING_TYPES = ['per_game', 'totals', 'per_minute', 'advanced',
              'per_poss', 'play-by-play', 'advanced_box_score']

icon = Image.open(os.path.join(script_directory, 'favicon.ico'))
st.set_page_config('NBA Standing Web', icon)

st.markdown('<img src=\"https://cdn.nba.com/logos/nba/nba-logoman-75-word_white.svg\" alt=\"NBA logo\" style=\"width:150px\"> ',
            unsafe_allow_html=True)
st.title('NBA Standing Web')

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox(
    'Year', list(reversed(range(1977, 2023))))
selected_standing = st.sidebar.selectbox(
    'Player Stats', STANDING_TYPES, format_func=translate_standing_type)
playerstanding = requests.get(f"http://backend:8000/load_data/selectyear={selected_year}selectstat={selected_standing}")

playerstanding=pd.read_json(playerstanding.json())
# Sidebar - Team selection
sorted_unique_team = sorted(playerstanding.Tm.unique())
selected_team = st.sidebar.multiselect(
    'Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_position = ['C', 'PF', 'SF', 'PG', 'SG']
selected_position = st.sidebar.multiselect('Position', unique_position, unique_position)

# Filtering data
df_selected_team = playerstanding[(playerstanding.Tm.isin(
    selected_team)) & (playerstanding.Pos.isin(selected_position))]


st.header('Displaying Players\' ' + translate_standing_type(selected_standing) +
          ' Stats of Selected Team(s)')
st.write('The result of your search given ' + str(df_selected_team.shape[0]) + ' players')
st.dataframe(df_selected_team)


with st.spinner('Loading season Scoring summary...'):
    st.header(f'{selected_year} Season Scoring Summary')
    st.write(f"""
            The {selected_year} season was the {ordinal(selected_year - 1946)} of the [National Basketball Association](https://en.wikipedia.org/wiki/National_Basketball_Association). 
        """)
    gen_scoring_efficiency_plot = requests.get(
            f"http://visualization:7000/gen_scoring_efficiency_plot/select_year={selected_year}")
    st.plotly_chart(pio.from_json(gen_scoring_efficiency_plot.json()))
