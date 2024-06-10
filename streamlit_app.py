import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Function to load data
def load_data(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        # Create a sample dataframe if no file exists
        sample_data = {
            'data1.csv': {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35], 'Job': ['Engineer', 'Doctor', 'Artist']},
            'data2.csv': {'Name': ['David', 'Eva', 'Frank'], 'Age': [28, 34, 29], 'Job': ['Writer', 'Chef', 'Banker']},
            'data3.csv': {'Name': ['George', 'Hannah', 'Ian'], 'Age': [42, 38, 31], 'Job1': ['Teacher', 'Designer', 'Developer']}
        }
        return pd.DataFrame(sample_data.get(file_name, {}))

# Function to save data
def save_data(df, file_name):
    try:
        df.to_csv(file_name, index=False)
    except Exception as e:
        st.sidebar.error(f"Failed to save data: {e}")

# Initialize session state
if 'current_df' not in st.session_state:
    st.session_state.current_df = 'data1.csv'
if 'df_history' not in st.session_state:
    st.session_state.df_history = []

# Load the selected dataframe
df = load_data(st.session_state.current_df)

# Title of the dashboard
st.title('Editable Dataframe Dashboard')

# Dropdown to select the dataframe
df_choice = st.sidebar.selectbox("Select DataFrame:", ['extracted_data.csv', 'data2.csv', 'data3.csv'])
if df_choice != st.session_state.current_df:
    st.session_state.current_df = df_choice
    df = load_data(st.session_state.current_df)
    st.rerun()

# Display the dataframe with specified width and height

# Function to handle changes in the dataframe
def handle_df_change():
    st.session_state.df_history.append(df.copy())

# Display the dataframe with specified width and height and handle changes
st.write("Here is the dataframe:")
df = st.data_editor(df, num_rows="dynamic", on_change=handle_df_change)


# Button to save changes
if st.sidebar.button('Save Changes'):
    # st.session_state.df_history.append(df.copy())
    save_data(df, st.session_state.current_df)
    st.sidebar.success("Data saved successfully!")
    st.rerun()

# Button to undo changes
if st.sidebar.button('Undo'):
    if st.session_state.df_history:
        df = st.session_state.df_history.pop()
        save_data(df, st.session_state.current_df)
        st.rerun()
    else:
        st.sidebar.error("No more changes to undo!")

# Excel file upload and data manipulation
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=['xlsx'])
if uploaded_file is not None:
    excel_data = pd.read_excel(uploaded_file)
    st.write("Excel Data Loaded Successfully!")
    st.write("Excel Data:")
    st.dataframe(excel_data)

# Function to create and return a Folium map
def create_map(location=[45.5236, -122.6750], zoom_start=13, geojson_path=None):
    m = folium.Map(location=location, zoom_start=zoom_start)
    if geojson_path and os.path.exists(geojson_path):
        with open(geojson_path, 'r') as file:
            geojson_data = file.read()
        folium.GeoJson(geojson_data, name='geojson').add_to(m)
    return m

# Display the map in Streamlit
st.header("Map View")
map_data = create_map()
st_folium(map_data, width=1400, height=600)
