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
    return data

@st.cache(persist=True)
def get_states(data):
    states = data['State_Name'].unique()
    states = states[(states!='Total') & (states!='State Unassigned')]
    return states

@st.cache(persist=True)
def get_state_data(data,state):
    return data.loc[data['State_Name'] == state].sort_values(by=['Date'])

@st.cache(persist=True, allow_output_mutation=True)
def addChart(data, option, choice):
    fig = go.Figure()
    for ch in choice:
        modified_data = get_state_data(data, ch)
        fig.add_trace(go.Line(x=modified_data['Date'], y=modified_data[option],name = ch))

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
    return fig

@st.cache(persist=True, allow_output_mutation=True)
def addBar(data, option, choice):
    fig = go.Figure()
    for ch in choice:
        modified_data = get_state_data(data, ch)
        fig.add_trace(go.Bar(x=modified_data['Date'], y=modified_data[option],name = ch))

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
    return fig

@st.cache(persist=True, allow_output_mutation=True)
def addPie(data, option, choice):
    fig = go.Figure()
    modified_data = data.groupby(['State_Name']).sum()
    modified_data = modified_data.loc[choice,option]

    fig.add_trace(go.Pie(labels=choice, values=modified_data))

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
    return fig

data = load_data()
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
        l=4,
        r=4,
        b=4,
        t=4,
        pad=0
    ),
)

st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=1)):
    st.write(modified_data)

states = get_states(data)

st.sidebar.subheader("State-wise breakdown")
select = st.sidebar.selectbox('Visualization type', ['Line Graph', 'Bar Plot', 'Pie Chart'], key='3')
choice = st.sidebar.multiselect('Select States: ',states)

if (len(choice)>0):
    st.subheader("State-wise breakdown")

    for option in options:
        st.markdown("#### "+ option)
        if select == 'Line Graph':
            fig = addChart(data, option , choice)
        elif select == 'Bar Plot':
            fig = addBar(data, option , choice)
            st.text("Bar Plot")
        else:
            fig = addPie(data, option , choice)
        st.plotly_chart(fig)

    if (st.sidebar.checkbox("Show Data",False,key=2)):
        if (select!='Pie Chart'):
            modified_data = pd.DataFrame()
            for ch in choice:
                modified_data = get_state_data(data, ch)
        else:
            modified_data = data.groupby(['State_Name']).sum()
            modified_data = modified_data.loc[choice]
        st.write(modified_data)
