import streamlit as st
import json
import urllib
import pandas as pd
import pydeck as pdk

st.set_page_config(
        page_icon="🚲", 
        page_title="Key"
    )

st.markdown("# Map")
st.sidebar.image(
    "./images/AHEAD.png",
    width=200
)
st.sidebar.write("### Powered By:")
st.sidebar.image(
    "./images/snowflake.png",
    width=200
)
st.sidebar.image(
    "./images/datarobot.png",
    width=200
)

station_info_url = "https://gbfs.divvybikes.com/gbfs/en/station_information.json"

req = urllib.request.Request(station_info_url)
response = urllib.request.urlopen(req)
data = response.read()
values = json.loads(data)
stations_info = values["data"]["stations"]

station_points = pd.DataFrame(columns = ['lat', 'lon','legacy_id', 'name'])
station_list = ["185", "222", "47", "196", "116", "316", "285", "125"]
for station in stations_info:
    if station['legacy_id'] in station_list:
        st.write(
            station['legacy_id'],": ", station['name']
            )
        # add point to df
        station_points.loc[len(station_points)] = [station['lat'], station['lon'], station['legacy_id'], station['name']]

# Map the points
# st.write(station_points)
# st.map(station_points)
# st.pydeck_chart(station_points)

view = pdk.ViewState(latitude=41.8781, longitude=-87.62987, zoom=11,)
# Create the scatter plot layer
StationLayer = pdk.Layer(
        "ScatterplotLayer",
        data=station_points,
        pickable=True,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["lon", "lat"],
        # get_radius=metric_to_show_in_covid_Layer,
        get_fill_color=[252, 136, 3],
        get_line_color=[255,0,0],
        # tooltip={"text": "{legacy_id}"},
    )

r = pdk.Deck(
    layers=[StationLayer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
    tooltip={"text": "Station: {legacy_id} \n {name}"},
)

map = st.pydeck_chart(r)