import streamlit as st

st.set_page_config(
        page_icon="🚴‍♂️", 
        page_title="About The Project"
    )
st.markdown("# About the Project")
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

st.write("Github Project: https://github.com/rossdstuart/divvy-app")