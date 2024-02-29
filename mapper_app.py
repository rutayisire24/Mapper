import streamlit as st
import streamlit_folium as st_folium
import folium
import pandas as pd
import geopandas as gpd

def upload_csv_data():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(uploaded_file)

        # Iterate through each column in the DataFrame
        for column in data.columns:
            # Check if the column is of object type (string)
            if data[column].dtype == 'object':
                # Convert the column to lowercase and strip whitespace
                data[column] = data[column].str.lower().str.strip()

        st.success("CSV data loaded successfully!")

        return data
    else:
        st.info("Please upload a CSV file to proceed.")
        return pd.DataFrame() # Return empty DataFrame as a placeholder

def load_geojson_data():
    try:
        geojson_path = 'Geojson/District.geojson'
        gdf = gpd.read_file(geojson_path)
        st.success("GeoJSON data imported successfully!")
        return gdf
    except Exception as e:
        st.error(f"Failed to load GeoJSON data: {e}")
        return gpd.GeoDataFrame()  # Return empty GeoDataFrame as a placeholder

def process_data(data, gdf):
    gdf['name'] = gdf['name'].str.replace("District", "", regex=False).str.strip().str.lower()
    return data, gdf

def create_and_display_map(data, gdf, org_unit,data_col):

    bounds = gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=center, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=gdf,
        data=data,
        columns=[org_unit, data_col],
        key_on="feature.properties.name",
    ).add_to(m)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    st_folium.folium_static(m)
    return

# Main app logic
def main():
    st.title("Map")
    st.info("This tool eases drawing maps as standardized by the Division of Health Information - Ministry of Health")

    gdf = load_geojson_data()
    st.write('Please upload the Data file')
    data = upload_csv_data()
    
    if not data.empty and not gdf.empty:
        data, gdf = process_data(data, gdf)
        
        # Adding an empty option manually
        org_unit_options = [""] + list(data.columns)
        data_col_options = [""] + list(data.columns)
        
        org_unit = st.selectbox("Select Organizational Unit", options=org_unit_options)
        data_col = st.selectbox("Select Data Column", options=data_col_options)
        
        # Proceed only if selections are made
        if org_unit and data_col:
            # Check if the selected data column is numerical or integer
            if pd.api.types.is_numeric_dtype(data[data_col]):
                if st.button("Lets Map"):
                    create_and_display_map(data, gdf, org_unit, data_col)
            else:
                st.error("Error: Please choose the right column. The selected column is not of type numerical or integer.")

if __name__ == "__main__":
    main()
