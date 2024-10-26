import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
import streamlit as st


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
dict_colour.update({'All': '#808080'})
# Create a dictionary mapping pitch types to their colors
dict_pitch = dict(zip(pitch_colours.keys(), [pitch_colours[key]['name'] for key in pitch_colours]))

# Create a dictionary mapping pitch types to their colors
dict_pitch_desc_type = dict(zip([pitch_colours[key]['name'] for key in pitch_colours],pitch_colours.keys()))


# Create a dictionary mapping pitch types to their colors
dict_pitch_name = dict(zip([pitch_colours[key]['name'] for key in pitch_colours], 
                           [pitch_colours[key]['colour'] for key in pitch_colours]))



required_pitch_types = ['All', 'FF', 'SI', 'FC', 'CH', 'FS','FO','SC','SL', 
                        'ST','SV' ,'CU', 'KC','KN']
# Create a mapping dictionary from the list
custom_order_dict = {pitch: index for index, pitch in enumerate(required_pitch_types)}

def tjstuff_plot(df:pl.DataFrame, 
                 pitcher_id:int,
                 position:str,
                 pitcher_name:str):

    # Create the figure and GridSpec layout
    fig = plt.figure(figsize=(10, 8), dpi=300)
    gs = GridSpec(5, 3, height_ratios=[0.1, 10, 10, 2, 0.1], width_ratios=[1, 100, 1])
    gs.update(hspace=0.4, wspace=0.1)

    # Add subplots to the grid
    ax0 = fig.add_subplot(gs[1, 1]) 
    ax1 = fig.add_subplot(gs[2, 1])
    ax1_left = fig.add_subplot(gs[:, 0]) 
    ax1_right = fig.add_subplot(gs[:, 2]) 
    ax1_top = fig.add_subplot(gs[0, :])
    ax1_bot = fig.add_subplot(gs[4, 1])
    ax2 = fig.add_subplot(gs[3, 1])

    # Update color dictionary
    

 
    df = df.to_pandas()
    # Filter data for the specific pitcher
    pitcher_df = df[(df['pitcher_id'] == pitcher_id) &
                                    (df['pitches'] >= 10)]
    

    
    # Add a new column for the custom order
    pitcher_df['order'] = pitcher_df['pitch_type'].map(custom_order_dict)
    pitcher_df = pitcher_df.sort_values('order')
                         
    # Get unique pitch types for the pitcher
    pitcher_pitches = pitcher_df['pitch_type'].unique()
    pitcher_pitches = [x for x in required_pitch_types if x in pitcher_pitches]


                     
    # Plot tjStuff+ with swarmplot for all players in the same position
    sns.swarmplot(data=df[(df['pitches'] >= 10) &
                                            (df['position'] == position)].dropna(subset=['pitch_type']),
                x='pitch_type',
                y='tj_stuff_plus',
                palette=dict_colour,
                alpha=0.3,
                size=3,
                ax=ax0,
                order=pitcher_pitches)

    # Overlay swarmplot for the specific pitcher
    sns.swarmplot(data=df[(df['pitcher_id'] == pitcher_id) &
                                            (df['pitches'] >= 10)],
                x='pitch_type',
                y='tj_stuff_plus',
                palette=dict_colour,
                alpha=1,
                size=14,
                ax=ax0,
                order=pitcher_pitches,
                edgecolor='black',
                linewidth=1)

    # Annotate the median values on the plot
    for index, row in pitcher_df.reset_index(drop=True).iterrows():
        ax0.text(index, 
                row['tj_stuff_plus'], 
                f'{row["tj_stuff_plus"]:.0f}', 
                color='white', 
                ha="center", 
                va="center",
                fontsize=7,
                weight='bold',
                clip_on=False)

    # Customize ax0
    ax0.set_xlabel('')
    ax0.set_ylabel('tjStuff+')
    ax0.grid(False)
    ax0.set_ylim(70, 130)
    ax0.axhline(y=100, color='black', linestyle='--', alpha=0.2, zorder=0)

    # Plot pitch grade with swarmplot for all players in the same position
    sns.swarmplot(data=df[(df['pitches'] >= 10) &
                                            (df['position'] == position)].dropna(subset=['pitch_type']),
                x='pitch_type',
                y='pitch_grade',
                palette=dict_colour,
                alpha=0.3,
                size=3,
                ax=ax1,
                clip_on=False,
                order=pitcher_pitches)

    # Overlay swarmplot for the specific pitcher
    sns.swarmplot(data=df[(df['pitcher_id'] == pitcher_id) &
                                            (df['pitches'] >= 10)],
                x='pitch_type',
                y='pitch_grade',
                palette=dict_colour,
                alpha=1,
                size=16,
                ax=ax1,
                order=pitcher_pitches,
                edgecolor='black',
                clip_on=False,
                linewidth=1)

    # Annotate the median values on the plot
    for index, row in pitcher_df.reset_index(drop=True).iterrows():
        ax1.text(index, 
                row['pitch_grade'], 
                f'{row["pitch_grade"]:.0f}', 
                color='white', 
                ha="center", 
                va="center",
                fontsize=8,
                weight='bold',
                clip_on=False,
                zorder=1000)
        
    # Customize ax1
    ax1.set_xlabel('Pitch Type')
    ax1.set_ylabel('Pitch Grade')
    ax1.grid(False)
    ax1.set_ylim(20, 80)
    ax1.axhline(y=50, color='black', linestyle='--', alpha=0.2, zorder=0)

    # Hide axes for additional subplots
    ax2.axis('off')
    ax1_left.axis('off')
    ax1_right.axis('off')
    ax1_top.axis('off')
    ax1_bot.axis('off')

    # Add text annotations
    ax1_bot.text(s='By: @TJStats', x=0, y=1, fontsize=12, ha='left')
    ax1_bot.text(s='Data: MLB', x=1, y=1, fontsize=12, ha='right')

    ax1_top.text(0.5, 0, f'{pitcher_name} tjStuff+ 2024 Season - {position}',
                fontsize=24, ha='center', va='top')

    ax2.text(x=0.5, y=0.6, s='tjStuff+ calculates the Expected Run Value (xRV) of a pitch regardless of type\n'
                            'tjStuff+ is normally distributed, where 100 is the mean and Standard Deviation is 10\n'
                            'Pitch Grade is based off tjStuff+ and scales the data to the traditional 20-80 Scouting Scale for a given pitch type',
                            
            ha='center', va='top', fontname='Calibri', fontsize=10)

    # Adjust subplot layout
    fig.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.03)
    st.pyplot(fig)
