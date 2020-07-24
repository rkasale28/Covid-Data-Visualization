import streamlit as st
import plotly.graph_objects as go
from controller import load_data, get_states, get_districts, get_state_data, get_aggregated_data, addLine, addBar, addPie, addDistrictPie

st.title("Covid Data Visualization")
st.sidebar.title("Covid Data Visualization")

data,districtData = load_data()

modified_data = data.loc[data['State_Name'] == 'Total']
modified_data = modified_data.set_index('Date')
modified_data = modified_data.sort_index()

st.markdown("## National Level: ")
st.subheader("Daily Updates")

options = ['Confirmed','Deceased','Recovered']
fig = go.Figure()

# Part 1
st.sidebar.subheader("National Level: ")
st.sidebar.subheader("Daily Updates")
choice = st.sidebar.multiselect('',options)

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

if (st.sidebar.checkbox("Show Data",False,key=1)):
    modified_data = modified_data.drop(columns='State_Name')
    st.dataframe(modified_data, width=600, height=300)

# Part 2
types = ['Active', 'Confirmed','Deceased','Recovered']
fig = go.Figure()

st.subheader("Cumulative Updates")

st.sidebar.subheader("Cumulative Updates")
choice = st.sidebar.multiselect('',types)

modified_data = get_state_data(data,'Total')
modified_data = modified_data.drop(columns=['State_Name','Confirmed','Deceased','Recovered'])
modified_data = modified_data.rename(columns={'CumConfirmed':'Confirmed','CumDeceased':'Deceased','CumRecovered':'Recovered'})

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

if (st.sidebar.checkbox("Show Data",False,key=2)):
    st.dataframe(modified_data, width=600, height=300)

# Part 3
st.subheader("Breakdown")
st.sidebar.subheader("Breakdown")

modified_data = get_aggregated_data(data, 'Total')
fig = go.Figure()
fig.add_trace(go.Pie(labels=types, values=modified_data, hole=.5))
st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=3)):
    st.dataframe(modified_data.to_frame().T, width=600, height=300)

states = get_states(data)

# Part 4
st.sidebar.subheader("State-wise breakdown")
active = st.sidebar.checkbox('Show Active',True,key=4)
confirmed = st.sidebar.checkbox('Show Confirmed',False,key=5)
deceased = st.sidebar.checkbox('Show Deceased',False,key=6)
recovered = st.sidebar.checkbox('Show Recovered',False,key=7)
decision = st.sidebar.checkbox('Show Data',False,key=8)

if (active or confirmed or deceased or recovered or decision):
    st.subheader("State-wise breakdown")

for option in types:
    if ((option=='Confirmed') & confirmed) | ((option=='Deceased') & deceased) | ((option=='Recovered') & recovered) | ((option=='Active') & active):
        st.markdown("#### "+ option)
        fig = addPie(data,option,states)
        st.plotly_chart(fig)

if (decision):
    modified_data = get_aggregated_data(data,states)
    st.dataframe(modified_data, width=600, height=300)

# Part 5
st.sidebar.subheader("Compare States")
select = st.sidebar.selectbox('Visualization type', ['Line Graph', 'Bar Plot', 'Pie Chart'], key=9)
choice = st.sidebar.multiselect('Select States: ',states)

if (len(choice)>0):
    active = st.sidebar.checkbox('Show Active',True,key=10)
    confirmed = st.sidebar.checkbox('Show Confirmed',False,key=11)
    deceased = st.sidebar.checkbox('Show Deceased',False,key=12)
    recovered = st.sidebar.checkbox('Show Recovered',False,key=13)
    decision = st.sidebar.checkbox('Show Data',False,key=14)

    if (active or confirmed or deceased or recovered or decision):
        st.subheader("Compare States")

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

# Part 6
st.markdown("## State Level: ")
st.sidebar.subheader("State Level: ")
select = st.sidebar.selectbox('Select State', states, key=15)

st.markdown("### "+ select)
st.subheader("Daily Updates")
st.sidebar.subheader("Daily Updates")
choice = st.sidebar.multiselect('',options,key=16)

modified_data = data.loc[data['State_Name'] == select]
modified_data = modified_data.set_index('Date')
modified_data = modified_data.sort_index()

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

if (st.sidebar.checkbox("Show Data",False,key=17)):
    modified_data = modified_data.drop(columns='State_Name')
    st.dataframe(modified_data, width=600, height=300)

#Part 7
st.subheader("Cumulative Updates")
st.sidebar.subheader("Cumulative Updates")
choice = st.sidebar.multiselect('',types,key=18)

modified_data = get_state_data(data,select)
modified_data = modified_data.drop(columns=['State_Name','Confirmed','Deceased','Recovered'])
modified_data = modified_data.rename(columns={'CumConfirmed':'Confirmed','CumDeceased':'Deceased','CumRecovered':'Recovered'})

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

if (st.sidebar.checkbox("Show Data",False,key=19)):
    st.dataframe(modified_data, width=600, height=300)

# Part 8
st.subheader("Breakdown")
st.sidebar.subheader("Breakdown")
modified_data = get_aggregated_data(data,select)
if ((modified_data['Active']==0) & (modified_data['Confirmed']==0) & (modified_data['Deceased']==0) & (modified_data['Recovered']==0)):
    st.markdown("**Total Cases = 0**")
else:
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=types, values=modified_data, hole=.5))
    st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=20)):
    st.dataframe(modified_data.to_frame().T, width=600, height=300)

# Part 9
st.sidebar.subheader("District-wise breakdown")
active = st.sidebar.checkbox('Show Active',True,key=21)
confirmed = st.sidebar.checkbox('Show Confirmed',False,key=22)
deceased = st.sidebar.checkbox('Show Deceased',False,key=23)
recovered = st.sidebar.checkbox('Show Recovered',False,key=24)
decision = st.sidebar.checkbox('Show Data',False,key=25)

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

    active = st.sidebar.checkbox('Show Active',True,key=26)
    confirmed = st.sidebar.checkbox('Show Confirmed',False,key=27)
    deceased = st.sidebar.checkbox('Show Deceased',False,key=28)
    recovered = st.sidebar.checkbox('Show Recovered',False,key=29)
    decision = st.sidebar.checkbox('Show Data',False,key=30)

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
select = st.sidebar.selectbox('Select District', districts, key=31)

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
    fig.add_trace(go.Pie(labels=types,values=[transposed_data[select]['Active'],transposed_data[select]['Confirmed'],transposed_data[select]['Deceased'],transposed_data[select]['Recovered']], hole=.5))
    st.plotly_chart(fig)

if (st.sidebar.checkbox("Show Data",False,key=32)):
    st.dataframe(modified_data, width=600, height=300)
