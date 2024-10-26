import seaborn as sns
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import requests
import polars as pl
from datetime import date
import pandas as pd
import matplotlib


# For help with plotting the pitch data, we will use the following dictionary to map pitch types to their corresponding colours
### PITCH COLOURS ###
pitch_colours = {
    ## Fastballs ##
    'FF': {'colour': '#FF007D', 'name': '4-Seam Fastball'},
    'FA': {'colour': '#FF007D', 'name': 'Fastball'},
    'SI': {'colour': '#98165D', 'name': 'Sinker'},
    'FC': {'colour': '#BE5FA0', 'name': 'Cutter'},

    ## Offspeed ##
    'CH': {'colour': '#F79E70', 'name': 'Changeup'},
    'FS': {'colour': '#FE6100', 'name': 'Splitter'},
    'SC': {'colour': '#F08223', 'name': 'Screwball'},
    'FO': {'colour': '#FFB000', 'name': 'Forkball'},

    ## Sliders ##
    'SL': {'colour': '#67E18D', 'name': 'Slider'},
    'ST': {'colour': '#1BB999', 'name': 'Sweeper'},
    'SV': {'colour': '#376748', 'name': 'Slurve'},

    ## Curveballs ##
    'KC': {'colour': '#311D8B', 'name': 'Knuckle Curve'},
    'CU': {'colour': '#3025CE', 'name': 'Curveball'},
    'CS': {'colour': '#274BFC', 'name': 'Slow Curve'},
    'EP': {'colour': '#648FFF', 'name': 'Eephus'},

    ## Others ##
    'KN': {'colour': '#867A08', 'name': 'Knuckleball'},
    'PO': {'colour': '#472C30', 'name': 'Pitch Out'},
    'UN': {'colour': '#9C8975', 'name': 'Unknown'},
}

# Create a dictionary mapping pitch types to their colors
dict_colour = dict(zip(pitch_colours.keys(), [pitch_colours[key]['colour'] for key in pitch_colours]))

# Create a dictionary mapping pitch types to their colors
dict_pitch = dict(zip(pitch_colours.keys(), [pitch_colours[key]['name'] for key in pitch_colours]))

# Create a dictionary mapping pitch types to their colors
dict_pitch_desc_type = dict(zip([pitch_colours[key]['name'] for key in pitch_colours],pitch_colours.keys()))


# Create a dictionary mapping pitch types to their colors
dict_pitch_name = dict(zip([pitch_colours[key]['name'] for key in pitch_colours], 
                           [pitch_colours[key]['colour'] for key in pitch_colours]))

# Define a custom colormap for styling
cmap_sum = matplotlib.colors.LinearSegmentedColormap.from_list("", ['#648FFF','#FFFFFF','#FFB000',])

# Load data from CSV file and preprocess it
df = pl.read_csv("tjstuff_plus_pitch_data_2024.csv").fill_nan(None)
df_plot = df.clone()
df = df.filter(df['pitches']>=10).drop_nulls(subset=['pitch_grade','tj_stuff_plus'])
df = df.sort(['pitcher_name','pitch_type'], descending=[False,False])

# Cast columns to appropriate data types
df = df.with_columns([
    pl.col('tj_stuff_plus').cast(pl.Int64).alias('tj_stuff_plus'),
    pl.col('pitches').cast(pl.Int64).alias('pitches'),
    pl.col('pitcher_id').cast(pl.Int64).alias('pitcher_id'),
    pl.col('pitch_grade').cast(pl.Int64).alias('pitch_grade')
])

# Define column configuration for Streamlit
column_config_dict = {
    'pitcher_id': 'Pitcher ID',
    'pitcher_name': 'Pitcher Name',
    'pitch_type': 'Pitch Type',
    'pitches': 'Pitches',
    'tj_stuff_plus': st.column_config.NumberColumn("tjStuff+", format="%.0f"),
    'pitch_grade': st.column_config.NumberColumn("Pitch Grade", format="%.0f")
}


# Get unique pitch types for selection
unique_pitch_types = ['']+sorted(df['pitch_type'].unique().to_list())
unique_pitch_types = [dict_pitch[x] if x in dict_pitch else x for x in unique_pitch_types]

# Create a multiselect widget for pitch types
selected_pitch_types = st.selectbox('Select Pitch Types', unique_pitch_types)

# Filter the DataFrame based on selected pitch types
if selected_pitch_types == 'All':
    df = df.filter(pl.col('pitch_type')=='All').sort('tj_stuff_plus', descending=True)

elif selected_pitch_types != '':
    df = df.filter(pl.col('pitch_type')==dict_pitch_desc_type[selected_pitch_types]).sort('tj_stuff_plus', descending=True)

# Convert Polars DataFrame to Pandas DataFrame and apply styling
styled_df = df[['pitcher_id', 'pitcher_name', 'pitch_type', 'pitches', 'tj_stuff_plus', 'pitch_grade']].to_pandas().style

# Apply background gradient styling to specific columns
styled_df = styled_df.background_gradient(subset=['tj_stuff_plus'], cmap=cmap_sum,vmin=80,vmax=120)
styled_df = styled_df.background_gradient(subset=['pitch_grade'], cmap=cmap_sum,vmin=20,vmax=80)

# Display the styled DataFrame in Streamlit
st.dataframe(styled_df,
                hide_index=True,
                column_config=column_config_dict,
                width=1500)


pitcher_id_name = dict(zip(df_plot['pitcher_id'],df_plot['pitcher_name']))
pitcher_id_name_id = dict(zip(df_plot['pitcher_id'],df_plot['pitcher_name']+ ' - '+df_plot['pitcher_id']))
pitcher_name_id_id = dict(zip(df_plot['pitcher_id'],df_plot['pitcher_name']+ ' - '+df_plot['pitcher_id']))
pitcher_id_position = dict(zip(df_plot['pitcher_id'],df_plot.drop_nulls(subset=['position'])['position']))


# Create a multiselect widget for pitch types
pitcher_id = st.selectbox('Select Pitcher', [pitcher_name_id_id[x] for x in pitcher_name_id_id])

# Define pitcher ID and position
position = pitcher_id_position[pitcher_id]
pitcher_name = pitcher_name_id_id[pitcher_id]

import tjstuff_plot

tjstuff_plot.tjstuff_plot(df_plot, pitcher_id, position, pitcher_name)
