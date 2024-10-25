import seaborn as sns
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import requests
import polars as pl
from datetime import date
import pandas as pd
import matplotlib

cmap_sum = matplotlib.colors.LinearSegmentedColormap.from_list("", ['#648FFF','#FFFFFF','#FFB000',])


# Load data
df = pl.read_csv("tjstuff_plus_pitch_data_2024.csv").fill_nan(None)
df = df.filter(df['pitches']>=10).drop_nulls(subset=['pitch_grade','tj_stuff_plus'])
df = df.sort(['pitcher_name','pitch_type'], descending=[False,False])

df = df.with_columns([
    pl.col('tj_stuff_plus').cast(pl.Int64).alias('tj_stuff_plus'),
    pl.col('pitches').cast(pl.Int64).alias('pitches'),
    pl.col('pitcher_id').cast(pl.Int64).alias('pitcher_id'),
    pl.col('pitch_grade').cast(pl.Int64).alias('pitch_grade')
])

column_config_dict = {
    'pitcher_id': 'Pitcher ID',
    'pitcher_name': 'Pitcher Name',
    'pitch_type': 'Pitch Type',
    'pitches': 'Pitches',
    'tj_stuff_plus': st.column_config.NumberColumn("tjStuff+", format="%.0f"),
    'pitch_grade': st.column_config.NumberColumn("Pitch Grade", format="%.0f")
}

styled_df = df[['pitcher_id', 'pitcher_name', 'pitch_type', 'pitches', 'tj_stuff_plus', 'pitch_grade']].to_pandas().style

styled_df = styled_df.background_gradient(subset=['tj_stuff_plus'], cmap=cmap_sum,vmin=85,vmax=115)
styled_df = styled_df.background_gradient(subset=['pitch_grade'], cmap=cmap_sum,vmin=20,vmax=80)


st.dataframe(styled_df,
                hide_index=True,
                column_config=column_config_dict,
                width=1500)
