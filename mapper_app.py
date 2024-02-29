import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

def find_shapefile(shapefiles_dir):
    """
    Finds and returns the path to the .shp file within the specified directory.
    Returns None if no .shp file is found.
    """
    for file in os.listdir(shapefiles_dir):
        if file.endswith(".shp"):
            return os.path.join(shapefiles_dir, file)
    return None

def load_and_display_shapefile(shapefile_path):
    """
    Loads a shapefile from a given path, displays the head of the GeoDataFrame, 
    and plots it using Folium if it contains data.
    """
    gdf = gpd.read_file(shapefile_path)
    if not gdf.empty:
        # Display the head of the GeoDataFrame
        st.write("Preview of the shapefile data:")
        gdf['geometry'] = gdf['geometry'].astype(str)
        st.dataframe(gdf.head())
        return 
    else:
        return None

def display_map(data, lat_col, lon_col, detail_col):
    """
    Display a map with Folium based on the specified latitude and longitude columns, 
    including popups based on a detail column.
    """
    m = folium.Map(location=[data[lat_col].mean(), data[lon_col].mean()], zoom_start=5)
    for _, row in data.iterrows():
        folium.Marker(
            location=[row[lat_col], row[lon_col]],
            popup=str(row[detail_col]),
        ).add_to(m)
    st_data = st_folium(m, width=725)
    return st_data

def main():
    st.title("Maapu")
    
    uploaded_file = st.file_uploader("Upload a CSV file for mapping", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(data.head())
        
        # Column selection
        lat_col = st.selectbox("Select Latitude Column", data.columns)
        lon_col = st.selectbox("Select Longitude Column", data.columns)
        detail_col = st.selectbox("Select Detail Column for Popup", data.columns, index=0)
        
        if st.button("Display Map"):
            display_map(data, lat_col, lon_col, detail_col)
    
    # Shapefile Section
    shapefiles_dir = 'shapefiles'  # Path to the directory containing shapefiles
    shapefile_path = find_shapefile(shapefiles_dir)
    
    if shapefile_path:
        st.success("Shapefile found and loaded!")
        load_and_display_shapefile(shapefile_path)
    else:
        st.error("No shapefile found in the 'shapefiles' directory.")

if __name__ == "__main__":
    main()
