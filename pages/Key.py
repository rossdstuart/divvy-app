import streamlit as st
import json
import urllib

st.set_page_config(
        page_icon="🚲", 
        page_title="Key"
    )

st.markdown("# Stations Key ❄️")
st.sidebar.image(
    "./images/AHEAD.png",
    width=200
)
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



station_list = ["185", "222", "47", "196", "116", "316", "285", "125"]
for station in stations_info:
    if station['legacy_id'] in station_list:
        st.write(station)

# key_data = stations_info["legacy_id"]="185"
# st.write(key_data)
# print(key_data)