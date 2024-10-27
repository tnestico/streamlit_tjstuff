# tjStuff+ App

## Overview

This Streamlit app tabulates and plots my pitching metric, tjStuff+, for all MLB players during the 2024 MLB Season.

About tjStuff+:

tjStuff+ calculates the Expected Run Value (xRV) of a pitch regardless of type
tjStuff+ is normally distributed, where 100 is the mean and Standard Deviation is 10
Pitch Grade is based off tjStuff+ and scales the data to the traditional 20-80 Scouting Scale for a given pitch type

## Features

- Generates and displays tjStuff+ plots and tables for all pitchers during the 2024 Season.

## Requirements

- Python 3.7+
- Streamlit
- Polars
- Seaborn
- Requests
- st_aggrid
- matplotlib

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the interface to input the required parameters:
    - Select the Pitch Type
    - Select the Pitcher

4. Click the "Generate Plot" button to generate and display the plot.

ed DataFrame is empty, the application prompts the user to select different parameters.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
