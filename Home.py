# streamlit_app.py

import streamlit as st
from st_aggrid import AgGrid
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
        page_icon="🚲", 
        page_title="Divvy Dashboard"
    )

st.markdown("# Divvy E-Bike availability Forcasting")
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


@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"], client_session_keep_alive=True)

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# Testing to remove the ttl to see if it saves on query costs
# @st.experimental_memo(ttl=600) 
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

#######
# station_query = '''
# SELECT LEGACY_ID, NAME FROM DIVVY_DATABASE.PUBLIC.STATION_INFO_FLATTEN
# '''
# station_df = pd.read_sql(station_query, conn)
# st.write(station_df)

# ##########

# current_query = '''
# select LEGACY_ID, NUM_EBIKES_AVAILABLE from STATION_STATUS_FLATTEN_FULL
#     where last_updated = (
#         select last_updated from station_status_flatten_full
#     order by last_updated desc
#     limit 1);
# '''
# current_df = pd.read_sql(current_query, conn)
# # st.write(station_df)


#################


#Timezone
df['LAST_UPDATED'] = pd.to_datetime(df.LAST_UPDATED, utc=True, format='%Y/%m/%d %i:$M %p')
df['NUM_EBIKES_AVAILABLE_BOOL (actual)_True_PREDICTION'] = df['NUM_EBIKES_AVAILABLE_BOOL (actual)_True_PREDICTION'].map('{:.2%}'.format)
#Columns Changes
df = df.drop(columns=['FORECAST_DISTANCE'])
df['LEGACY_ID'] = df['LEGACY_ID'].apply(lambda x: x.replace('"', ''))

# Pull the Station IDs
all_stations = pd.unique(df[["LEGACY_ID"]].values.ravel())


df = df.drop(columns=['FORECAST_POINT'])
# df = df.rename(columns= {'LAST_UPDATED': 'Forecast Time', 'LEGACY_ID': 'Station ID' }, inplace = True)
# stations_stations = st.multiselect("Choose staions to visualize", all_stations, all_stations[:3])
stations_stations = st.multiselect("Choose your staions", all_stations)
selected_rows = df.loc[df['LEGACY_ID'].isin(stations_stations)]
selected_rows.sort_values(by=['LAST_UPDATED', 'LEGACY_ID'])
AgGrid(selected_rows)

## display the current availaiblity 
# selected_current = current_df.loc[current_df['LEGACY_ID'].isin(stations_stations)]
# st.write(selected_current)


# ### Plot the line chart
# plot_data = df.iloc[:, [0,1,3]]
# # st.line_chart(plot_data)
# if plot_data is not None:
#     plot_data.plot()


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


######## line chart
if not selected_rows.empty:
    # st.write(selected_rows.iloc[:, [1,3]])
    line_plot = selected_rows.iloc[:, [2]]
    # st.pyplot(line_plot)
    # st.write(line_plot.style.hide_index())
    # st.dataframe(line_plot)





    # st.write(line_plot.to_string(index=False))


    # timeseries_data = { 
    #     # 'Date': ['2021-12-26', '2021-12-29',
    #     #          '2021-12-27', '2021-12-30',
    #     #          '2021-12-28', '2021-12-31' ], 
    #     'Date': (selected_rows.iloc[:, [1]](index=False)),
        
    #     'Washington': [42, 41, 41, 42, 42, 40],
        
    #     'Canada' : [30, 30, 31, 30, 30, 30],
        
    #     'California' : [51, 50, 50, 50, 50, 50]
    # }

    # # Create dataframe

    # dataframe = pd.DataFrame(timeseries_data,columns=['Date', 'Washington', 'Canada', 'California'])
    
    # # Changing the datatype

    # dataframe["Date"] = dataframe["Date"].astype("datetime64")
    
    # # Setting the Date as index

    # dataframe = dataframe.set_index("Date")
    # dataframe