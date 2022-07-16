# streamlit_app.py

import streamlit as st
from st_aggrid import AgGrid
import snowflake.connector
import pandas as pd

st.set_page_config(
        page_icon="🚲", 
        page_title="Divvy Dashboard"
    )

st.markdown("# Divvy E-Bike availability Forcasting")
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


@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


query = '''
SELECT * FROM DIVVY_DATABASE.PUBLIC.DIVVY_DR_RESULTS
ORDER BY FORECAST_POINT desc, LAST_UPDATED asc
LIMIT 4800
'''
 
df = pd.read_sql(query, conn)
#Timezone
df['LAST_UPDATED'] = pd.to_datetime(df.LAST_UPDATED, utc=True, format='%Y/%m/%d %i:$M %p')
df['NUM_EBIKES_AVAILABLE_BOOL (actual)_True_PREDICTION'] = df['NUM_EBIKES_AVAILABLE_BOOL (actual)_True_PREDICTION'].map('{:.2%}'.format)
#Columns Changes
df = df.drop(columns=['FORECAST_DISTANCE'])
# df['LEGACY_ID'] = df["LEGACY_ID"].str('"', '')

# st.write('Divvy E-Bike availability Forcasting')
# Pull the Station IDs
all_stations = df["LEGACY_ID"].unique()

df = df.drop(columns=['FORECAST_POINT'])
# df = df.rename(columns= {'LAST_UPDATED': 'Forecast Time', 'LEGACY_ID': 'Station ID' }, inplace = True)
# stations_stations = st.multiselect("Choose staions to visualize", all_stations, all_stations[:3])
stations_stations = st.multiselect("Choose your staions", all_stations)
selected_rows = df.loc[df['LEGACY_ID'].isin(stations_stations)]
AgGrid(selected_rows)
