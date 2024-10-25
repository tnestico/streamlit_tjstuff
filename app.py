import seaborn as sns
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import requests
import polars as pl
from datetime import date

# Load data
df = pl.read_csv("tjstuff_plus_pitch_data_2024.csv")


df['tj_stuff_plus'] = df['tj_stuff_plus'].cast(pl.Int64)
df['pitches'] = df['pitches'].cast(pl.Int64)
df['pitcher_id'] = df['pitcher_id'].cast(pl.Int64)
df['pitch_grade'] = df['pitch_grade'].cast(pl.Int64)


column_config_dict = {
    'pitcher_id': 'Pitcher ID',
    'pitcher_name': 'Pitcher Name',
    'pitch_type': 'Pitch Type',
    'pitches': 'Pitches',
    'tj_stuff_plus': 'tjStuff+',
    'pitch_grade': 'Grade'
}




st.dataframe(df[['pitcher_id', 'pitcher_name', 'pitch_type', 'pitches', 'tj_stuff_plus', 'pitch_grade']],
                hide_index=True,
                column_config=column_config_dict,
                width=1500)
