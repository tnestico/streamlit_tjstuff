import seaborn as sns
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import requests
import polars as pl
from datetime import date
import pandas as pd
import matplotlib

# Define a custom colormap for styling
cmap_sum = matplotlib.colors.LinearSegmentedColormap.from_list("", ['#648FFF','#FFFFFF','#FFB000',])

# Load data from CSV file and preprocess it
df = pl.read_csv("tjstuff_plus_pitch_data_2024.csv").fill_nan(None)
df = df.filter(df['pitches']>=10).drop_nulls(subset=['pitch_grade','tj_stuff_plus'])
df = df.sort(['pitcher_name','pitch_type'], descending=[False,False])

# Cast columns to appropriate data types
df = df.with_columns([
    pl.col('tj_stuff_plus').cast(pl.Int64).alias('tj_stuff_plus'),
    pl.col('pitches').cast(pl.Int64).alias('pitches'),
    pl.col('pitcher_id').cast(pl.Int64).alias('pitcher_id'),
    pl.col('pitch_grade').cast(pl.Int64).alias('pitch_grade')
])


# Drop rows with NaN values and sort the DataFrame
df = df.drop_nulls(subset=['pitch_grade', 'tj_stuff_plus'])
df = df.sort(['pitcher_name', 'pitch_type'], descending=[False, False])

# Define column configuration
column_config_dict = {
    'pitcher_id': 'Pitcher ID',
    'pitcher_name': 'Pitcher Name',
    'pitch_type': 'Pitch Type',
    'pitches': 'Pitches',
    'tj_stuff_plus': st.column_config.NumberColumn("tjStuff+", format="%.0f"),
    'pitch_grade': st.column_config.NumberColumn("Pitch Grade", format="%.0f")
}

# Get unique pitch types for multiselection
unique_pitch_types = df['pitch_type'].unique().to_list()




selected_pitch_types = st.multiselect('Select Pitch Types', unique_pitch_types)

# Create a multiselect widget for pitch types
if 'selected_pitch_types' not in st.session_state:
    st.session_state.selected_pitch_types = unique_pitch_types

# Filter the DataFrame based on selected pitch types
if selected_pitch_types:
    df = df.filter(pl.col('pitch_type').is_in(selected_pitch_types))
    #st.session_state.selected_pitch_types = selected_pitch_types

# Convert Polars DataFrame to Pandas DataFrame and apply styling
styled_df = df[['pitcher_id', 'pitcher_name', 'pitch_type', 'pitches', 'tj_stuff_plus', 'pitch_grade']].to_pandas().style

# Apply background gradient styling to specific columns
styled_df = styled_df.background_gradient(subset=['tj_stuff_plus'], cmap='viridis', vmin=80, vmax=120)
styled_df = styled_df.background_gradient(subset=['pitch_grade'], cmap='viridis', vmin=20, vmax=80)

# Display the styled DataFrame in Streamlit
st.dataframe(styled_df, hide_index=True, column_config=column_config_dict, width=1500)
