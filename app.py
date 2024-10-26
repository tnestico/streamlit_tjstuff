import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    'pitch_type': ['Fastball', 'Curveball', 'Slider', 'Changeup', 'Fastball', 'Slider'],
    'speed': [95, 78, 85, 82, 97, 88],
    'spin_rate': [2200, 2500, 2300, 2100, 2250, 2350]
}
df = pd.DataFrame(data)

# Initialize session state for selected pitch types
if 'selected_pitch_types' not in st.session_state:
    st.session_state.selected_pitch_types = []

# Multiselect widget for pitch types
pitch_types = df['pitch_type'].unique()
selected_pitch_types = st.multiselect('Select pitch types', pitch_types, default=st.session_state.selected_pitch_types)

# Update session state
st.session_state.selected_pitch_types = selected_pitch_types

# Filter DataFrame based on selected pitch types
if selected_pitch_types:
    filtered_df = df[df['pitch_type'].isin(selected_pitch_types)]
else:
    filtered_df = df

# Render the filtered DataFrame
st.dataframe(filtered_df)
