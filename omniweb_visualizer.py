# omniweb_visualizer.py

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go


def read_data(lst_file):
    """
    Read and process data from the LST file.

    :param lst_file: Path to the LST file.
    :return: DataFrame containing the storm data.
    """
    column_names = [
        'Year', 'Day', 'Hour', 'Minute',
        'Field_Magnitude_Avg', 'BX', 'BY', 'BZ',
        'Speed', 'Proton_Density', 'Proton_Temperature',
        'Electric_Field', 'Plasma_Beta', 'Alfven_Mach_Number',
        'AE_Index', 'AL_Index', 'AU_Index',
        'SYM_D', 'SYM_H'
    ]

    try:
        data = pd.read_fwf(lst_file, names=column_names)  # Adjust if needed
        print("Data read successfully. First few rows:")
        print(data.head())  # Print the first few rows for debugging

        # Create DateTime for plotting
        data['DateTime'] = pd.to_datetime(
            data[['Year', 'Day', 'Hour', 'Minute']].astype(str).agg('-'.join, axis=1),
            format='%Y-%j-%H-%M',
            errors='coerce'
        )

        # Print the number of records
        print(f"Number of records: {len(data)}")

        return data
    except Exception as e:
        print(f"Error reading the LST file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


# File paths for your LST file
lst_file_path = 'omni_web_data1.lst'  # Adjust this path

# Load the data
storm_data = read_data(lst_file_path)

# Check if the DataFrame is empty
if storm_data.empty:
    print("The DataFrame is empty. Please check the LST file format.")
else:
    # Initialize Dash app
    app = dash.Dash(__name__)

    # Dash layout
    app.layout = html.Div([
        html.H1("3D Geomagnetic Storm Data for May 2024"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in storm_data['Year'].unique()],
            value=storm_data['Year'].min(),  # Default to the minimum year
            clearable=False
        ),
        dcc.Slider(
            id='magnitude-slider',
            min=storm_data['Field_Magnitude_Avg'].min(),
            max=storm_data['Field_Magnitude_Avg'].max(),
            value=storm_data['Field_Magnitude_Avg'].mean(),
            marks={i: str(round(i, 2)) for i in
                   range(int(storm_data['Field_Magnitude_Avg'].min()), int(storm_data['Field_Magnitude_Avg'].max()) + 1,
                         5)},
            step=0.1,
        ),
        dcc.Graph(id='storm-3d-plot'),
        html.Div(id='click-data')  # Div to display click data
    ])


    @app.callback(
        Output('storm-3d-plot', 'figure'),
        Input('year-dropdown', 'value'),
        Input('magnitude-slider', 'value')
    )
    def update_graph(selected_year, selected_magnitude):
        # Filter the DataFrame based on the selected year and magnitude
        filtered_data = storm_data[(storm_data['Year'] == selected_year) &
                                   (storm_data['Field_Magnitude_Avg'] <= selected_magnitude)]

        return {
            'data': [
                go.Scatter3d(
                    x=filtered_data['BX'],  # Magnetic field X component
                    y=filtered_data['BY'],  # Magnetic field Y component
                    z=filtered_data['BZ'],  # Magnetic field Z component
                    mode='markers',
                    marker=dict(
                        size=5,
                        color=filtered_data['Field_Magnitude_Avg'],  # Color by field magnitude average
                        colorscale='Viridis',  # Color scale
                        showscale=True,
                    ),
                    text=filtered_data['DateTime'].dt.strftime('%Y-%m-%d %H:%M'),  # Annotations
                    hoverinfo='text'  # Show DateTime on hover
                )
            ],
            'layout': go.Layout(
                title='3D Geomagnetic Storm Data',
                scene=dict(
                    xaxis_title='BX (nT)',
                    yaxis_title='BY (nT)',
                    zaxis_title='BZ (nT)',
                ),
                margin=dict(l=0, r=0, b=0, t=40)
            )
        }


    @app.callback(
        Output('click-data', 'children'),
        Input('storm-3d-plot', 'clickData')
    )
    def display_click_data(clickdata):
        if clickdata:
            point = clickdata['points'][0]
            return f'Clicked Point: DateTime: {point["text"]}, BX: {point["x"]}, BY: {point["y"]}, BZ: {point["z"]}'
        return "Click on a point to see details."


    if __name__ == "__main__":
        app.run_server(debug=True)
