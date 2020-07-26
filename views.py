import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from controller import load_data, get_states, get_districts, get_state_data, get_aggregated_data, addLine, addBar, addPie, addDistrictPie, get_dates

st.title("Covid Data Visualization")
st.sidebar.title("Covid Data Visualization")

data,districtData,testData = load_data()
options = ['Confirmed','Deceased','Recovered']
types = ['Active', 'Confirmed','Deceased','Recovered']
required = ['Active', 'Deceased', 'Recovered']

# Part 1
st.markdown("## National Level: ")
st.subheader("Daily Updates")

st.sidebar.subheader("National Level: ")
st.sidebar.subheader("Daily Updates")

dt1, dt2 = get_dates(data)
start_date = st.sidebar.date_input('Start Date', min_value=dt1, max_value=dt2, value=dt1, key=1)
end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=dt2, value=dt2, key=2)

choice = st.sidebar.multiselect('',options)

modified_data = data.loc[data['State_Name'] == 'Total']
modified_data = modified_data.set_index('Date')
modified_data = modified_data.sort_index()
modified_data = modified_data.loc[start_date:end_date]

fig = go.Figure()

if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[ch],mode='lines',  name = ch))
else:
    for option in options:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[option],mode='lines',  name = option))

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

if (st.sidebar.checkbox("Show Data",False,key=3)):
    modified_data = modified_data.drop(columns='State_Name')
    st.dataframe(modified_data, width=600, height=300)

# Part 2
fig = go.Figure()

st.subheader("Cumulative Updates")

st.sidebar.subheader("Cumulative Updates")
start_date = st.sidebar.date_input('Start Date', min_value=dt1, max_value=dt2, value=dt1, key=4)
end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=dt2, value=dt2, key=5)
choice = st.sidebar.multiselect('',types)

modified_data = get_state_data(data,'Total')
modified_data = modified_data.drop(columns=['State_Name','Confirmed','Deceased','Recovered'])
modified_data = modified_data.rename(columns={'CumConfirmed':'Confirmed','CumDeceased':'Deceased','CumRecovered':'Recovered'})
modified_data = modified_data.loc[start_date:end_date]

if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[ch],mode='lines',  name = ch))
else:
    for option in types:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[option],mode='lines',  name = option))

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
    st.dataframe(modified_data, width=600, height=300)

# Part 3
st.subheader("Breakdown")
st.sidebar.subheader("Breakdown")

modified_data = get_aggregated_data(data, 'Total')
fig = go.Figure()
fig.add_trace(go.Pie(labels=required, values=modified_data.drop(['Confirmed'],axis=0), hole=.5))
st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=7)):
    st.dataframe(modified_data.to_frame().T, width=600, height=300)

states = get_states(data)

# Part 4
st.sidebar.subheader("State-wise breakdown")

active = st.sidebar.checkbox('Show Active',True,key=8)
confirmed = st.sidebar.checkbox('Show Confirmed',False,key=9)
deceased = st.sidebar.checkbox('Show Deceased',False,key=10)
recovered = st.sidebar.checkbox('Show Recovered',False,key=11)
decision = st.sidebar.checkbox('Show Data',False,key=12)

if (active or confirmed or deceased or recovered or decision):
    st.subheader("State-wise breakdown")

for option in types:
    if ((option=='Confirmed') & confirmed) | ((option=='Deceased') & deceased) | ((option=='Recovered') & recovered) | ((option=='Active') & active):
        st.markdown("#### "+ option)
        fig = addPie(data,option,states,dt1,dt2)
        st.plotly_chart(fig)

if (decision):
    modified_data = get_aggregated_data(data,states)
    st.dataframe(modified_data, width=600, height=300)

# Part 5
st.sidebar.subheader("Compare States")
select = st.sidebar.selectbox('Visualization type', ['Line Graph', 'Bar Plot', 'Pie Chart'], key=13)
choice = st.sidebar.multiselect('Select States: ',states)

if (len(choice)>0):
    start_date = st.sidebar.date_input('Start Date', min_value=dt1, max_value=dt2, value=dt1, key=14)
    end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=dt2, value=dt2, key=15)

    active = st.sidebar.checkbox('Show Active',True,key=16)
    confirmed = st.sidebar.checkbox('Show Confirmed',False,key=17)
    deceased = st.sidebar.checkbox('Show Deceased',False,key=18)
    recovered = st.sidebar.checkbox('Show Recovered',False,key=19)
    decision = st.sidebar.checkbox('Show Data',False,key=20)

    if (active or confirmed or deceased or recovered or decision):
        st.subheader("Compare States")

    for option in types:
        if ((option=='Confirmed') & confirmed) | ((option=='Deceased') & deceased) | ((option=='Recovered') & recovered) | ((option=='Active') & active):
            st.markdown("#### "+ option)
            if (select=='Line Graph'):
                fig=addLine(data,option,choice, start_date, end_date)
            elif (select=='Bar Plot'):
                fig=addBar(data,option,choice, start_date, end_date)
            else:
                fig =addPie(data,option,choice, start_date,end_date)
            st.plotly_chart(fig)

    if (decision):
        if (select!='Pie Chart'):
            for ch in choice:
                modified_data = get_state_data(data, ch)
                modified_data = modified_data.loc[start_date:end_date]

                st.markdown("#### "+ ch)
                modified_data = modified_data.drop(columns=['State_Name','CumConfirmed','CumDeceased','CumRecovered'])
                modified_data = modified_data[(modified_data['Confirmed']>0) | (modified_data['Recovered']>0) | (modified_data['Deceased']>0)]
                st.dataframe(modified_data, width=600, height=300)
        else:
            modified_data = data.set_index('Date')
            modified_data = modified_data.sort_index()
            modified_data = modified_data.loc[start_date:end_date]
            modified_data = get_aggregated_data(modified_data,choice)

            st.dataframe(modified_data, width=600, height=300)

# Part 6
st.markdown("## State Level: ")
st.sidebar.subheader("State Level: ")
select = st.sidebar.selectbox('Select State', states, key=21)

st.markdown("### "+ select)
st.subheader("Daily Updates")
st.sidebar.subheader("Daily Updates")
start_date = st.sidebar.date_input('Start Date', min_value=dt1, max_value=dt2, value=dt1, key=22)
end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=dt2, value=dt2, key=23)
choice = st.sidebar.multiselect('',options,key=24)

modified_data = data.loc[data['State_Name'] == select]
modified_data = modified_data.set_index('Date')
modified_data = modified_data.sort_index()
modified_data = modified_data.loc[start_date:end_date]

fig = go.Figure()
if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[ch],mode='lines',  name = ch))
else:
    for option in options:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[option],mode='lines',  name = option))

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

if (st.sidebar.checkbox("Show Data",False,key=25)):
    modified_data = modified_data.drop(columns='State_Name')
    st.dataframe(modified_data, width=600, height=300)

# Part 8
st.subheader("Test Data")
st.sidebar.subheader("Test Data")

modified_data = testData[testData['State_Name']==select]
dt1,dt2 = get_dates(modified_data)

start_date = st.sidebar.date_input('Start Date', min_value=dt1, max_value=dt2, value=dt1, key=44)
end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=dt2, value=dt2, key=45)

modified_data = modified_data.set_index('Date')
modified_data = modified_data.loc[start_date:end_date]
modified_data = modified_data.drop(columns=['State_Name'])

fig = go.Figure()
fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data['Tested'], mode='lines'))

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

if (st.sidebar.checkbox("Show Data",False,key=43)):
    st.dataframe(modified_data, width=600, height=300)

#Part 7
st.subheader("Cumulative Updates")
st.sidebar.subheader("Cumulative Updates")
dt1, dt2 = get_dates(data)
start_date = st.sidebar.date_input('Start Date', min_value=dt1, max_value=dt2, value=dt1, key=26)
end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=dt2, value=dt2, key=27)
choice = st.sidebar.multiselect('',types,key=28)

modified_data = get_state_data(data,select)
modified_data = modified_data.drop(columns=['State_Name','Confirmed','Deceased','Recovered'])
modified_data = modified_data.rename(columns={'CumConfirmed':'Confirmed','CumDeceased':'Deceased','CumRecovered':'Recovered'})
modified_data = modified_data.loc[start_date:end_date]

fig = go.Figure()
if (len(choice)>0):
    for ch in choice:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[ch], mode='lines', name = ch))
else:
    for option in types:
        fig.add_trace(go.Scatter(x=modified_data.index, y=modified_data[option],mode='lines', name = option))

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

if (st.sidebar.checkbox("Show Data",False,key=29)):
    st.dataframe(modified_data, width=600, height=300)

# Part 8
st.subheader("Breakdown")
st.sidebar.subheader("Breakdown")
modified_data = get_aggregated_data(data,select)
if ((modified_data['Active']==0) & (modified_data['Confirmed']==0) & (modified_data['Deceased']==0) & (modified_data['Recovered']==0)):
    st.markdown("**Total Cases = 0**")
else:
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=required, values=modified_data.drop(['Confirmed'],axis=0), hole=.5))
    st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=30)):
    st.dataframe(modified_data.to_frame().T, width=600, height=300)

# Part 9
st.sidebar.subheader("District-wise breakdown")
active = st.sidebar.checkbox('Show Active',True,key=31)
confirmed = st.sidebar.checkbox('Show Confirmed',False,key=32)
deceased = st.sidebar.checkbox('Show Deceased',False,key=33)
recovered = st.sidebar.checkbox('Show Recovered',False,key=34)
decision = st.sidebar.checkbox('Show Data',False,key=35)

if (active or confirmed or deceased or recovered or decision):
    st.subheader("District-wise breakdown")

modified_data = districtData[districtData['State_Name']==select]
districts = get_districts(modified_data)
if (districts.size!=0):
    for option in types:
        if ((option=='Confirmed') & confirmed) | ((option=='Deceased') & deceased) | ((option=='Recovered') & recovered) | ((option=='Active') & active):
            st.markdown("#### "+ option)
            districts.sort()
            fig = addDistrictPie(modified_data,option,districts)
            st.plotly_chart(fig)
else:
    st.write("No districts to display")

if (decision):
    modified_data = modified_data[modified_data['District_Name']!='Unknown']
    modified_data = modified_data.drop(columns=['State_Name'])
    modified_data = modified_data.set_index('District_Name')
    st.dataframe(modified_data, width=600, height=300)

# Part 10
st.sidebar.subheader("Compare Districts")
choice = st.sidebar.multiselect('Select Districts: ',districts)

modified_data = districtData[districtData['State_Name']==select]

if (len(choice)>0):
    choice.sort()

    active = st.sidebar.checkbox('Show Active',True,key=36)
    confirmed = st.sidebar.checkbox('Show Confirmed',False,key=37)
    deceased = st.sidebar.checkbox('Show Deceased',False,key=38)
    recovered = st.sidebar.checkbox('Show Recovered',False,key=39)
    decision = st.sidebar.checkbox('Show Data',False,key=40)

    modified_data = modified_data[modified_data['District_Name'].isin(choice)]

    if (active or confirmed or deceased or recovered or decision):
        st.subheader("Compare Districts")

    for option in types:
        if ((option=='Confirmed') & confirmed) | ((option=='Deceased') & deceased) | ((option=='Recovered') & recovered) | ((option=='Active') & active):
            st.markdown("#### "+ option)
            fig =addDistrictPie(modified_data,option,choice)
            st.plotly_chart(fig)

    if (decision):
        modified_data = modified_data.drop(columns=['State_Name'])
        modified_data = modified_data.set_index('District_Name')
        st.dataframe(modified_data, width=600, height=300)

# Part 11
st.markdown("## District Level: ")
st.sidebar.subheader("District Level: ")
districts = get_districts(districtData)
districts.sort()
select = st.sidebar.selectbox('Select District', districts, key=41)

st.subheader("Breakdown")
st.sidebar.subheader("Breakdown")

modified_data = districtData[districtData['District_Name']==select]
st.markdown("**State Name: **"+ modified_data['State_Name'].values[0])
st.markdown("**District Name: **"+ modified_data['District_Name'].values[0])
modified_data = modified_data.drop(columns=['State_Name'])
modified_data = modified_data.set_index('District_Name')
transposed_data = modified_data.T
if ((transposed_data[select]['Active']==0) & (transposed_data[select]['Confirmed']==0) & (transposed_data[select]['Deceased']==0) & (transposed_data[select]['Recovered']==0)):
    st.markdown("**Total Cases = 0**")
else:
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=required,values=[transposed_data[select]['Active'],transposed_data[select]['Deceased'],transposed_data[select]['Recovered']], hole=.5))
    st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=42)):
    st.dataframe(modified_data, width=600, height=300)
