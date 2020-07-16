import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
modified_data = data.loc[data['State_Name'] == 'Total'].sort_values(by = ['Date'])
st.subheader("Daily Updates")
fig = go.Figure()
options = ['Confirmed','Deceased','Recovered']
st.sidebar.subheader("Daily Updates")
choice = st.sidebar.multiselect('',options)
if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Line(x=modified_data['Date'], y=modified_data[ch],name = ch))
else:
    for option in options:
        fig.add_trace(go.Line(x=modified_data['Date'], y=modified_data[option],name = option))

fig.update_layout(
    autosize=False,
    width=800,
    height=500,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
)

st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False)):
    st.write(modified_data)
