import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_daily.csv"
)

DISTRICT_DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/district_level.csv"
)

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date'])

    districtData = pd.read_csv(DISTRICT_DATA_URL)
    return data,districtData

@st.cache(persist=True)
def get_states(data):
    states = data['State_Name'].unique()
    states = states[(states!='Total') & (states!='State Unassigned')]
    return states

@st.cache(persist=True,allow_output_mutation=True)
def get_districts(data):
    districts = data['District_Name'].unique()
    districts = districts[(districts!='Other State') & (districts!='Unassigned') & (districts!='Unknown') & (districts!='Airport Quarantine')]
    return districts

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
    modified_data = modified_data[['Active','Confirmed','Deceased','Recovered']]
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
    fig.update_traces(textposition='inside')
    fig.update_layout(
        legend_title_text='States',
        uniformtext_minsize=12,
        uniformtext_mode='hide',
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
def addDistrictPie(modified_data,option,districts):
    fig = go.Figure()
    temp_data = modified_data[['District_Name',option]]
    temp_data = temp_data[temp_data['District_Name']!='Other State']
    temp_data = temp_data[temp_data['District_Name'].isin(districts)]
    fig.add_trace(go.Pie(labels=temp_data['District_Name'], values=temp_data[option]))
    fig.update_traces(textposition='inside')
    fig.update_layout(
        legend_title_text='Districts',
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        autosize=True,
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
