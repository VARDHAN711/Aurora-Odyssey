import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os
from astropy.io import fits
import plotly.graph_objs as go
import numpy as np
import dash_bootstrap_components as dbc

# Initialize the Dash app
# app = dash.Dash(__name__, external_stylesheets=['/assets/styles.css', dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=['/assets/styles.css', dbc.themes.BOOTSTRAP])

# Define the directory where your FITS files are stored
fits_dir = 'fits files'  # Adjust this path
# Specify the relevant FITS files for AIA synoptic maps
fits_files = [
    "AIAsynoptic0094.fits",
    "AIAsynoptic0131.fits",
    "AIAsynoptic0171.fits",
    "AIAsynoptic0193.fits",
    "AIAsynoptic0211.fits",
    "AIAsynoptic0304.fits",
    "AIAsynoptic0335.fits",
    "AIAsynoptic1600.fits",
    "AIAsynoptic1700.fits",
    "AIAsynoptic4500.fits"
]

# Create the image slider (carousel)
carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": '/assets/Aurora_austral.jpg'},
        {"key": "2", "src": '/assets/Aurora_Australis_From_Melbourne.jpg'},
        {"key": "3", "src": '/assets/Aurora_Borealis_(May_10_2024_solar_storms)_as_seen_from_Kraków.jpg'},
        {"key": "4", "src": '/assets/Aurora_Borealis_from_Cwmbran,_Wales.png'},
        {"key": "5", "src": '/assets/Aurora_over_Northern_Ireland.jpg'},
        {"key": "6", "src": '/assets/Auroral_Corona_Onawa_IA.jpg'},
        {"key": "7", "src": '/assets/Magenta_G5_aurora_over_Tuntorp,_Lysekil_Municipality_12.jpg'},
        {"key": "8", "src": '/assets/May_2024_aurora_in_Perth_Australia.jpg'},
        {"key": "9", "src": '/assets/May_2024_aurora_over_Xinjiang.jpg'},
        {"key": "10", "src": '/assets/May_2024_Aurora_SC.jpg'},
        {"key": "11", "src": '/assets/Palm_Trees_and_Auroras_In_Mazatlan.jpg'},
        {"key": "12", "src": '/assets/Solar_Storm_of_May_10,_2024_over_Viola,_Arkansas.jpg'}
    ],
    controls=True,
    indicators=True,
    interval=2000,
    ride="carousel",
    style={'width': '60%','height':'auto', 'margin': 'auto','object-fit':'contain'},  # Center and control size of the carousel
)


# Layout of the Dash app
app.layout = html.Div([
    html.Header(html.H1("AURORA ODYSSEY",id="aurora-odyssey")),

    html.Video(controls=True, loop=True, src='/assets/INTRO_VIDEO_FINAL_reduced.mp4',  style={'width': '100%', 'height': 'auto','border-radius':'5px', 'margin-bottom':'25px','padding':'20px'}),
   
    html.H1("Solar Storms of May 2024:",style={'color':'white','padding':'20px'}),
    html.Div([
        html.P(
            "The solar storms of May 2024 were a series of powerful solar storms "
            "that occurred during solar cycle 25. This app visualizes the solar flares "
            "and geomagnetic storms that occurred from May 10-13, 2024."
        ),
        html.H2("What Happened?"),
        html.P(
            "During this period, the Sun produced extreme solar flares and coronal mass ejections (CMEs) "
            "that reached Earth, causing one of the most powerful geomagnetic storms in decades."
        ),
        
        html.H2("What Are FITS Files?"),
        html.P("FITS (Flexible Image Transport System) is a standard file format used primarily in astronomy. It was designed to store, transmit, and manipulate scientific images, data tables, and even multi-dimensional data. FITS files are used by astronomers and researchers to store large amounts of observational data from telescopes, space observatories, and other instruments."),
        html.Br(),
        
        html.H2("Why FITS Files?"),
        html.P("FITS files are widely used because they are versatile and allow scientists to store not just images but also metadata (information about the image, such as the instrument used, observation time, etc.). This makes them perfect for scientific purposes where both data and context are crucial."),
        html.Br(),

        html.H2("Common Use Cases: FITS files are used to store:"),
        html.P("Images captured by space observatories like NASA's Solar Dynamics Observatory (SDO).Data from astronomical observations, such as solar flares, distant galaxies, and even black holes.Other scientific data in tabular or multi-dimensional form.Brief Explanation of 2D and 3D Plots in the AppTo help users visualize the data stored in the FITS files, we create two types of plots: 2D Heatmaps and 3D Surface Plots. Here's how they work:"),
        html.Br(),
        
        html.H2("2D Heatmaps (Flat View of Solar Data):"),
        html.P(" A 2D heatmap is a visual representation of data where colors represent the intensity or value of the data at each point. In our case, the heatmap shows how bright different parts of the solar image are, based on the data in the FITS file."),
        html.Br(),

        html.H2("How to Understand a 2D Heatmap?"),
        html.P("Think of it as a “top-down view” of the Sun. Each pixel (dot) on the map represents a point on the Sun's surface, and the color represents the intensity of the radiation at that point."),
        html.P("Bright colors (usually yellow or white) represent areas of high intensity, such as solar flares or active regions on the Sun."),
        html.P("Darker colors (like blue or black) represent areas with less intensity, such as quieter regions on the Sun."),
        html.Br(),

        html.P("Why It's Useful:"),
        html.P(" A 2D heatmap provides a simple, easy-to-understand way to see which parts of the Sun were more active during the May 2024 solar storms."),
        html.Br(),

        html.H2("3D Surface Plots (Depth View of Solar Data):"),
        html.P('A 3D surface plot takes the same data used in the 2D heatmap but adds another dimension: depth. Instead of just using colors to show intensity, we also use height (z-axis) to represent intensity, so brighter areas are shown as taller "peaks."'),
        html.Br(),

        html.H2("How to Understand a 3D Surface Plot?"),
        html.P("Imagine the Sun as a landscape with hills and valleys:"),
        html.P("High peaks represent regions of intense solar activity (high radiation levels).Low valleys represent calmer areas of the Sun with less activity."),
        html.P("By rotating the 3D plot, you can explore the surface of the Sun from different angles, gaining a better understanding of the data."),
        html.Br(),

        html.P("Why It's Useful:"),
        html.P("The 3D view allows you to better grasp the variation in intensity across the Sun's surface during the solar storm. You can visualize not only where the activity is happening but also how intense it is relative to other parts.")
        
    ], style={'margin-bottom': '20px','color':'white','padding':'20px'}), #white,#00FF7F,#FF00FF

    # Dropdown to select FITS file
    dcc.Dropdown(
        id='fits-dropdown',
        options=[{'label': f, 'value': f} for f in fits_files],
        value=fits_files[0],  # Default to the first FITS file
        clearable=False,
        style={'margin-bottom': '20px','margin-left': '10px','width':'500px','height':'40px'}
    ),

    # Div to hold both graphs side by side
    html.Div([
        dcc.Graph(id='fits-heatmap', style={'flex': 1}),
        dcc.Graph(id='fits-3d-plot', style={'flex': 1})
    ], style={'display': 'flex','color':'#00FF7F','padding':'20px'}),  # Use flexbox for side-by-side layout

    # Information about auroras
    html.Div([
        html.H2("Auroras Across the Globe"),
        html.P(
            "The geomagnetic storm caused beautiful auroras to be visible in locations far from the poles, "
            "including parts of the United States, Europe, and Australia. "
            "This is a rare event and showcases the power of solar activity."
        ),
        html.H2("Gallery of Aurora Sightings:"),
        html.Br(),
        
        # Image slider (carousel) with fixed height
        html.Div(
            [carousel], style={ 'height': '600px','width':'100%','overflow': 'hidden'})  # Set fixed height for the carousel

    ], style={'margin-top': '20px','color':'white','padding':'20px'}),

    # Footer information
    html.Footer([
        html.P("Data Source: NASA, NOAA"),
        html.P("Developed with Dash by Astro Archers Team."),
    ], style={'text-align': 'center', 'margin-top': '20px','color':'#00FF7F'}),
])


# Callback to update the heatmap and 3D plot when a FITS file is selected
@app.callback(
    [Output('fits-heatmap', 'figure'),
     Output('fits-3d-plot', 'figure')],
    [Input('fits-dropdown', 'value')]
)
def update_graph(selected_fits_file):
    # Load the selected FITS file
    fits_file_path = os.path.join(fits_dir, selected_fits_file)

    try:
        with fits.open(fits_file_path) as hdul:
            # Check all HDUs for image data
            image_data = None
            for hdu in hdul:
                if hdu.data is not None:  # Look for data
                    image_data = hdu.data
                    print(f"Loaded data from HDU {hdul.index(hdu)}")  # Log which HDU is used
                    break  # Exit loop after finding the first valid data

            # Check if image data is valid
            if image_data is None or image_data.size == 0:
                raise ValueError("No image data found.")

            # Normalize the image data for better visualization
            image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))

            # Create a heatmap to visualize the FITS data
            heatmap_fig = go.Figure(go.Heatmap(z=image_data, colorscale='Cividis'))

            # Update the layout for the heatmap
            heatmap_fig.update_layout(
                title=f'Solar Data from {selected_fits_file} (2D Heatmap)',
                xaxis_title='X Pixel',
                yaxis_title='Y Pixel',
                width=700,
                height=800,
                xaxis=dict(showgrid=False),  # Optionally hide grid lines
                yaxis=dict(showgrid=False),
                coloraxis_colorbar=dict(title='Intensity', thickness=15, titlefont=dict(size=16),tickfont=dict(size=14))
            )

            # Create a 3D plot of the FITS data
            x = np.arange(image_data.shape[1])
            y = np.arange(image_data.shape[0])
            x, y = np.meshgrid(x, y)

            z = image_data  # Z data is the image data

            # Create the 3D surface plot
            surface_fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Viridis')])

            # Update the layout for the 3D plot
            surface_fig.update_layout(
                title=f'Solar Data from {selected_fits_file} (3D Surface Plot)',
                scene=dict(
                    xaxis_title='X Pixel',
                    yaxis_title='Y Pixel',
                    zaxis_title='Intensity',
                    camera_eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                width=700,
                height=800
            )

            return heatmap_fig, surface_fig

    except Exception as e:
        print(f"Error loading FITS file: {e}")
        return go.Figure(), go.Figure()  # Return empty figures on error


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
