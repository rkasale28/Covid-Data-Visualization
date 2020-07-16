import streamlit as st
import pandas as pd

st.title("Covid Data Visualization")
st.sidebar.title("Covid Data Visualization")

DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_daily.csv"
)

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date'])
    states = data['State_Name'].unique()
    states = states[(states!='Total') & (states!='State Unassigned')]
    return data, states

data, states = load_data()
st.write(data)
st.write(states)
