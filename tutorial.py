import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

# Constants section
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


# Funcion para cargar datos
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def plain_data(data):
    # Toggle para activar y desactivar cosas
    if st.checkbox('Show raw data'):
        # Datos planes
        st.subheader('Raw data')
        st.write(data)

def draw_histogram(data):
    st.subheader('Number of pickups by hour')

    #Use NumPy to generate a histogram that breaks down pickup times binned by hour:
    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

    # Draw bar chart
    st.bar_chart(hist_values)


def plot_map(data):
    """
    Using a histogram with Uber's dataset helped us determine what the busiest times are for pickups,
    but what if we wanted to figure out where pickups were concentrated throughout the city.
    While you could use a bar chart to show this data, it wouldn't be easy to interpret unless you were intimately
    familiar with latitudinal and longitudinal coordinates in the city. To show pickup concentration,
    let's use Streamlit st.map() function to overlay the data on a map of New York City
    :param data:
    :return:
    """
    st.subheader('Map of all pickups')
    st.map(data)

def plot_map_by_time(data):
    hour_to_filter = 17
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    st.map(filtered_data)
    # Visualizacion mas completa de mapo
    #st.pydeck_chart

def plot_map_by_time_slider(data):
    hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'FILTERED: Map of all pickups at {hour_to_filter}:00')
    st.map(filtered_data)

def plot_line_chart(data):
     chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
     st.line_chart(chart_data)

# Main function
def main():
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data(1000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!')

    # Plain data
    plain_data(data)
    draw_histogram(data)
    plot_map(data)

    # Map con filtro de fechas
    #plot_map_by_time(data)
         
    # Map con sliders
    #plot_map_by_time_slider(data)
         
    plot_line_chart(data)

# LLamado al main
main()
