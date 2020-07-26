import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_daily.csv"
)

DISTRICT_DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/district_level.csv"
)

TEST_DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_tested_daily.csv"
)

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date'])

    districtData = pd.read_csv(DISTRICT_DATA_URL)

    testData = pd.read_csv(TEST_DATA_URL)
    testData['Date'] = pd.to_datetime(testData['Date'])
    return data,districtData, testData

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
def addLine(data,option,choice, start_date, end_date):
    fig = go.Figure()
    for ch in choice:
        modified_data = get_state_data(data,ch)
        modified_data = modified_data.loc[start_date:end_date]
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[option], mode='lines' ,name = ch))
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
def addBar(data,option,choice,start_date,end_date):
    fig = go.Figure()
    for ch in choice:
        modified_data = get_state_data(data,ch)
        modified_data = modified_data.loc[start_date:end_date]
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
def addPie(data,option,choice, start_date, end_date):
    fig = go.Figure()
    modified_data = data.set_index('Date')
    modified_data = modified_data.sort_index()
    modified_data = modified_data.loc[start_date:end_date]
    modified_data = get_aggregated_data(modified_data,choice)

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

@st.cache(persist=True)
def get_dates(data):
    if ('Date' in data.columns):
        data = data.set_index('Date')
    data = data.sort_index()
    dt1 = data.iloc[1:].index.values[0]
    dt1 = datetime.strptime(np.datetime_as_string(dt1,unit='s'), '%Y-%m-%dT%H:%M:%S')
    dt2 = data.iloc[-1:].index.values[0]
    dt2 = datetime.strptime(np.datetime_as_string(dt2,unit='s'), '%Y-%m-%dT%H:%M:%S')
    return dt1,dt2

@st.cache(persist=True, allow_output_mutation=True)
def addTestLine(testData,choice,start_date,end_date):
    fig = go.Figure()

    for select in choice:
        modified_data = getStateTestData(testData,select)
        modified_data = modified_data.loc[start_date:end_date]

        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data['Tested'], mode='lines',name=select))

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
def addTestBar(testData,choice,start_date,end_date):
    fig = go.Figure()

    for select in choice:
        modified_data = getStateTestData(testData,select)
        modified_data = modified_data.loc[start_date:end_date]

        fig.add_trace(go.Bar(x=modified_data.index, y=modified_data['Tested'],name=select))

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


@st.cache(persist=True)
def get_aggregated_test_data(data,state):
    modified_data = data[data['State_Name']==state]
    modified_data = modified_data.sort_index()
    modified_data = modified_data.iloc[-1:]
    if not (modified_data.empty):
        modified_data = pd.DataFrame([[state,modified_data['Tested'].values[0]]],columns=['State_Name','Tested'])
    else:
        modified_data = pd.DataFrame([[state,0]],columns=['State_Name','Tested'])
    modified_data = modified_data.set_index('State_Name')
    return modified_data

@st.cache(persist=True, allow_output_mutation=True)
def addTestPie(data,choice,start_date,end_date):
    modified_data = data.set_index('Date')
    modified_data = modified_data.sort_index()
    modified_data = modified_data.loc[start_date:end_date]

    temporary_data = pd.DataFrame()
    for state in choice:
        temporary_data = temporary_data.append(get_aggregated_test_data(modified_data,state))

    fig = go.Figure()

    fig.add_trace(go.Pie(labels=choice, values=temporary_data['Tested']))
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

@st.cache(persist=True)
def sliceData(data,start_date,end_date):
    modified_data = data.set_index('Date')
    modified_data = modified_data.sort_index()
    modified_data = modified_data.loc[start_date:end_date]
    return modified_data

@st.cache(persist=True)
def getStateTestData(testData, select):
    modified_data = testData[testData['State_Name']==select]
    modified_data = modified_data.set_index('Date')
    modified_data['total_tested'] = modified_data['Tested'].diff()
    modified_data = modified_data.drop(columns=['State_Name','Tested'])
    modified_data = modified_data.rename(columns = {'total_tested':'Tested'})
    modified_data[modified_data['Tested']<0] = 0
    return modified_data
