import streamlit as st
import streamlit_folium as st_folium
import folium
import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt

def load_geojson_data(choice):
    """
    Load GeoJSON data based on user choice between districts and regions.
    """
    try:
        if choice == 'district':
            geojson_path = 'Geojson/District.geojson'
        elif choice == 'region':
            geojson_path = 'Geojson/Regions.geojson'
        elif choice == 'subcounty':
            geojson_path = 'Geojson/Subcounties.geojson'
        else:
            st.error("Invalid choice. Please select either 'region' or 'district'.")
            return gpd.GeoDataFrame()

        gdf = gpd.read_file(geojson_path)
        st.success("GeoJSON data loaded successfully!")        
        return gdf
    except Exception as e:
        st.error(f"Failed to load GeoJSON data: {e}")
        return gpd.GeoDataFrame()
    

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

def process_data(data, gdf):
    gdf['name'] = gdf['name'].str.replace("District", "", regex=False).str.strip().str.lower()
    return data, gdf

def create_and_display_map(data, gdf, org_unit,data_col, Palette):

    bounds = gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=center, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=gdf,
        data=data,
        columns=[org_unit, data_col],
        fill_color= Palette,
        fill_opacity=0.8,
        line_opacity=0.8,
        key_on="feature.properties.name",
    ).add_to(m)
    overlay = folium.Rectangle(
    bounds=[[-90, -180], [90, 180]], 
    fill=True,
    color='#000000',  # Black color
    fill_color='#000000',
    fill_opacity=0.2,  # Adjust opacity here (0 is fully transparent, 1 is fully opaque)
    )
    overlay.add_to(m)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

  # Save the map as an HTML file
    map_file_path = "map.html"
    m.save(map_file_path)
    
    # Display the map in the Streamlit app
    st_folium.folium_static(m)
    
    # Provide a download button for the map
    with open(map_file_path, "rb") as file:
        btn = st.download_button(
            label="Download Map",
            data=file,
            file_name="map.html",
            mime="text/html"
        )


# Main app logic
def main():
    st.title("Maapu")
    map_logo_path = 'logo.png'
    st.image(map_logo_path, width=100)

    with st.expander("See Details"):
        st.write("This tool eases drawing maps as standardized by the Division of Health Information - Ministry of Health")

    geojson_choice = st.radio("Choose the GeoJSON data to use:", ('region', 'district', 'subcounty'))
    
    # Assuming load_geojson_data returns a GeoDataFrame or similar
    gdf = load_geojson_data(geojson_choice)
    
    district_list = [
'agago', 'amuru', 'gulu city', 'gulu', 'kitgum', 'lamwo', 'nwoya', 'omoro', 'pader',
'buhweju', 'bushenyi', 'ibanda', 'isingiro', 'kazo', 'kiruhura', 'mbarara city', 'mbarara',
'mitooma', 'ntungamo', 'rubirizi', 'rwampara', 'sheema', 'bududa', 'bukwo', 'bulambuli',
'kapchorwa', 'kween', 'manafwa', 'mbale city', 'mbale', 'namisindwa', 'sironko', 'budaka',
'busia', 'butaleja', 'butebo', 'kibuku', 'pallisa', 'tororo', 'buliisa', 'hoima city', 'hoima',
'kagadi', 'kakumiro', 'kibaale', 'kikuube', 'kiryandongo', 'masindi', 'bugiri', 'bugweri',
'buyende', 'iganga', 'jinja city', 'jinja', 'kaliro', 'kamuli', 'luuka', 'mayuge', 'namayingo',
'namutumba', 'kampala', 'abim', 'amudat', 'kaabong', 'karenga', 'kotido', 'moroto', 'nabilatuk',
'nakapiripirit', 'napak', 'kabale', 'kanungu', 'kisoro', 'rubanda', 'rukiga', 'rukungiri',
'alebtong', 'amolatar', 'apac', 'dokolo', 'kole', 'kwania', 'lira city', 'lira', 'otuke', 'oyam',
'buikwe', 'buvuma', 'kassanda', 'kayunga', 'kiboga', 'kyankwanzi', 'luwero', 'mityana', 'mubende',
'mukono', 'nakaseke', 'nakasongola', 'bukomansimbi', 'butambala', 'gomba', 'kalangala', 'kalungu',
'kyotera', 'lwengo', 'lyantonde', 'masaka city', 'masaka', 'mpigi', 'rakai', 'sembabule', 'wakiso',
'amuria', 'bukedea', 'kaberamaido', 'kalaki', 'kapelebyong', 'katakwi', 'kumi', 'ngora', 'serere',
'soroti city', 'soroti', 'bundibugyo', 'bunyangabu', 'fort portal city', 'kabarole', 'kamwenge',
'kasese', 'kitagwenda', 'kyegegwa', 'kyenjojo', 'ntoroko', 'adjumani', 'arua city', 'arua', 'koboko',
'madi-okollo', 'maracha', 'moyo', 'nebbi', 'obongi', 'pakwach', 'terego', 'yumbe', 'zombo'
]
    
    with st.expander('See geojson'):
        st.write(gdf.head())

    if geojson_choice == 'subcounty':
        district_choice = st.selectbox("Choose a District:", district_list)
    


    st.write('Please upload the Data file')
    # Assuming upload_csv_data returns a DataFrame
    data = upload_csv_data()

    with st.expander("see data uploaded"):
        st.write(data.head())
    
    # Check if both geojson_choice has been made and data has been uploaded
    if geojson_choice and not data.empty and not gdf.empty:
        data, gdf = process_data(data, gdf)
                
        # Adding an empty option manually
        org_unit_options = [""] + list(data.columns)
        data_col_options = [""] + list(data.columns)
        
        org_unit = st.selectbox("Select Organizational Unit", options=org_unit_options, index=0)
        data_col = st.selectbox("Select Data Column", options=data_col_options, index=0)
        
        palette_choice = st.selectbox(
            'Choose a color Palette for the Map:',
            options = [ "RdYlGn", "RdYlGn_r","Blues","Greens"],
            index=3)
        # Proceed only if selections are made beyond the empty option
        if org_unit and data_col:
            # Check if the selected data column is numerical or integer
            if pd.api.types.is_numeric_dtype(data[data_col]):
                if st.button("Lets Map"):
                    create_and_display_map(data, gdf, org_unit, data_col, palette_choice)
            else:
                st.error("Error: Please choose the right column. The selected column is not of type numerical or integer.")

if __name__ == "__main__":
    main()