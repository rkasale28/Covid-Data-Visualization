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
    modified_data = data.loc[data['State_Name'] == state]
    modified_data = modified_data.set_index('Date')
    modified_data = modified_data.sort_index()
    modified_data['CumConfirmed'] = modified_data['Confirmed'].cumsum()
    modified_data['CumRecovered'] = modified_data['Recovered'].cumsum()
    modified_data['CumDeceased'] = modified_data['Deceased'].cumsum()
    modified_data['Active'] = modified_data['CumConfirmed'] - modified_data['CumRecovered'] - modified_data['CumDeceased']
    return modified_data

@st.cache(persist=True)
def get_aggregated_data(data,state):
    modified_data = data.groupby(['State_Name']).sum()
    modified_data = modified_data.loc[state]
    modified_data['Active'] = modified_data['Confirmed'] - modified_data['Deceased'] - modified_data['Recovered']
    return modified_data

@st.cache(persist=True, allow_output_mutation=True)
def addLine(data,option,choice):
    fig = go.Figure()
    for ch in choice:
        modified_data = get_state_data(data,ch)
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[option],name = ch))
    fig.update_layout(
        autosize=False,
        width=800,
        height=450,
        margin=dict(
            l=4,
            r=4,
            b=4,
            t=4,
            pad=0
        ),
    )
    return fig

@st.cache(persist=True, allow_output_mutation=True)
def addBar(data,option,choice):
    fig = go.Figure()
    for ch in choice:
        modified_data = get_state_data(data,ch)
        fig.add_trace(go.Bar(x=modified_data.index, y=modified_data[option],name = ch))
    fig.update_layout(
        autosize=False,
        width=800,
        height=450,
        margin=dict(
            l=4,
            r=4,
            b=4,
            t=4,
            pad=0
        ),
    )
    return fig

@st.cache(persist=True, allow_output_mutation=True)
def addPie(data,option,choice):
    fig = go.Figure()
    modified_data = get_aggregated_data(data,choice)
    fig.add_trace(go.Pie(labels=choice, values=modified_data[option]))
    fig.update_layout(
        autosize=False,
        width=800,
        height=450,
        margin=dict(
            l=4,
            r=4,
            b=4,
            t=4,
            pad=0
        ),
    )
    return fig

data = load_data()

modified_data = data.loc[data['State_Name'] == 'Total']
modified_data = modified_data.set_index('Date')
modified_data = modified_data.sort_index()

st.markdown("## Country Level: ")
st.subheader("Daily Updates")


options = ['Confirmed','Deceased','Recovered']
fig = go.Figure()

# Part-I
st.sidebar.subheader("Country Level: ")
st.sidebar.subheader("Daily Updates")
choice = st.sidebar.multiselect('',options)

if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[ch],name = ch))
else:
    for option in options:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[option],name = option))

fig.update_layout(
    autosize=False,
    width=800,
    height=450,
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
    modified_data = modified_data.drop(columns='State_Name')
    st.dataframe(modified_data, width=600, height=300)

# Part 2
types = ['Confirmed','Deceased','Recovered','Active']
fig = go.Figure()

st.subheader("Cumulative Updates")

st.sidebar.subheader("Cumulative Updates")
choice = st.sidebar.multiselect('',types)

modified_data = get_state_data(data,'Total')
modified_data = modified_data.drop(columns=['State_Name','Confirmed','Deceased','Recovered'])
modified_data = modified_data.rename(columns={'CumConfirmed':'Confirmed','CumDeceased':'Deceased','CumRecovered':'Recovered'})

if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[ch],name = ch))
else:
    for option in types:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[option],name = option))

fig.update_layout(
    autosize=False,
    width=800,
    height=450,
    margin=dict(
        l=4,
        r=4,
        b=4,
        t=4,
        pad=0
    ),
)

st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=2)):
    st.dataframe(modified_data, width=600, height=300)

# Part 3
st.subheader("Breakdown")
st.sidebar.subheader("Breakdown")

modified_data = get_aggregated_data(data, 'Total')
fig = go.Figure()
fig.add_trace(go.Pie(labels=types, values=modified_data))
st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=3)):
    st.dataframe(modified_data.to_frame().T, width=600, height=300)

states = get_states(data)

# Part 4
st.markdown("## State Level: ")
st.sidebar.subheader("State Level: ")
select = st.sidebar.selectbox('Select State', states, key=4)

st.markdown("### "+ select)
st.subheader("Daily Updates")
st.sidebar.subheader("Daily Updates")
choice = st.sidebar.multiselect('',options,key=5)

modified_data = data.loc[data['State_Name'] == select]
modified_data = modified_data.set_index('Date')
modified_data = modified_data.sort_index()

fig = go.Figure()
if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[ch],name = ch))
else:
    for option in options:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[option],name = option))

fig.update_layout(
    autosize=False,
    width=800,
    height=450,
    margin=dict(
        l=4,
        r=4,
        b=4,
        t=4,
        pad=0
    ),
)

st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=6)):
    modified_data = modified_data.drop(columns='State_Name')
    st.dataframe(modified_data, width=600, height=300)

#Part 5
types = ['Confirmed','Deceased','Recovered','Active']

st.subheader("Cumulative Updates")
st.sidebar.subheader("Cumulative Updates")
choice = st.sidebar.multiselect('',types,key=7)

modified_data = get_state_data(data,select)
modified_data = modified_data.drop(columns=['State_Name','Confirmed','Deceased','Recovered'])
modified_data = modified_data.rename(columns={'CumConfirmed':'Confirmed','CumDeceased':'Deceased','CumRecovered':'Recovered'})

fig = go.Figure()
if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[ch],name = ch))
else:
    for option in types:
        fig.add_trace(go.Line(x=modified_data.index, y=modified_data[option],name = option))

fig.update_layout(
    autosize=False,
    width=800,
    height=450,
    margin=dict(
        l=4,
        r=4,
        b=4,
        t=4,
        pad=0
    ),
)

st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=8)):
    st.dataframe(modified_data, width=600, height=300)

# Part 6
st.subheader("Breakdown")
st.sidebar.subheader("Breakdown")
modified_data = get_aggregated_data(data,select)

fig = go.Figure()
fig.add_trace(go.Pie(labels=types, values=modified_data))
st.plotly_chart(fig)
if (st.sidebar.checkbox("Show Data",False,key=9)):
    st.dataframe(modified_data.to_frame().T, width=600, height=300)

# Part 7
st.sidebar.subheader("State-wise breakdown")
select = st.sidebar.selectbox('Visualization type', ['Line Graph', 'Bar Plot', 'Pie Chart'], key=10)
choice = st.sidebar.multiselect('Select States: ',states)

if (len(choice)>0):
    confirmed = st.sidebar.checkbox('Show Confirmed',True,key=11)
    deceased = st.sidebar.checkbox('Show Deceased',False,key=12)
    recovered = st.sidebar.checkbox('Show Recovered',False,key=13)
    active = st.sidebar.checkbox('Show Active',False,key=14)
    decision = st.sidebar.checkbox('Show Data',False,key=15)

    st.subheader("State-wise breakdown")
    for option in types:
        if ((option=='Confirmed') & confirmed) | ((option=='Deceased') & deceased) | ((option=='Recovered') & recovered) | ((option=='Active') & active):
            st.markdown("#### "+ option)
            if (select=='Line Graph'):
                fig=addLine(data,option,choice)
            elif (select=='Bar Plot'):
                fig=addBar(data,option,choice)
            else:
                fig =addPie(data,option,choice)
            st.plotly_chart(fig)

    if (decision):
        if (select!='Pie Chart'):
            for ch in choice:
                modified_data = get_state_data(data, ch)
                st.markdown("#### "+ ch)
                modified_data = modified_data.drop(columns=['State_Name','CumConfirmed','CumDeceased','CumRecovered'])
                modified_data = modified_data[(modified_data['Confirmed']>0) | (modified_data['Recovered']>0) | (modified_data['Deceased']>0)]
                st.dataframe(modified_data, width=600, height=300)
        else:
            modified_data = get_aggregated_data(data,choice)
            st.dataframe(modified_data, width=600, height=300)
