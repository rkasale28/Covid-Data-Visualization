import requests
import pandas as pd
from datetime import datetime
import os
import numpy as np

states = {'an':'Andaman and Nicobar Islands',
'ap':'Andhra Pradesh',
'ar':'Arunachal Pradesh',
'as':'Assam',
'br':'Bihar',
'ch':'Chandigarh',
'ct':'Chhattisgarh',
'dd':'Daman and Diu',
'dl':'Delhi',
'dn':'Dadra and Nagar Haveli and Daman and Diu',
'ga':'Goa',
'gj':'Gujarat',
'hp':'Himachal Pradesh',
'hr':'Haryana',
'jh':'Jharkhand',
'jk':'Jammu and Kashmir',
'ka':'Karnataka',
'kl':'Kerala',
'la':'Ladakh',
'ld':'Lakshadweep',
'mh':'Maharashtra',
'ml':'Meghalaya',
'mn':'Manipur',
'mp':'Madhya Pradesh',
'mz':'Mizoram',
'nl':'Nagaland',
'or':'Odisha',
'pb':'Punjab',
'py':'Puducherry',
'rj':'Rajasthan',
'sk':'Sikkim',
'tg':'Telangana',
'tn':'Tamil Nadu',
'tr':'Tripura',
'tt':'Total',
'un':'State Unassigned',
'up':'Uttar Pradesh',
'ut':'Uttarakhand',
'wb':'West Bengal'
}

# State Level Daily
resp = requests.get("https://api.covid19india.org/states_daily.json")
if (resp.status_code == 200):
    resp = resp.json()

    df = pd.DataFrame(resp['states_daily'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date','status'])

    DATA_URL = (
    "D:/Covid-Data-Visualization/state_level_daily.csv"
    )

    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by=['Date'])
    data = data.iloc[-1:]
    dt = data['Date'].values[0]

    df = df[df['date']>dt]
    df = df.rename(columns=states)
    df = df.set_index(['date','status'])
    df = df.T
    new_json = []
    if not (df.empty):
        for (item,row) in df.iterrows():
            date_list = row.index.get_level_values(0).unique().sort_values()
            for d in date_list:
                date = datetime.strftime(d,'%d-%b-%y')
                if (item == 'dateymd'):
                    continue

                new_obj = {
                    'Date' : date,
                    'Confirmed' : row[date]['Confirmed'],
                    'Deceased' :row[date]['Deceased'],
                    'Recovered': row[date]['Recovered'],
                    'State_Name': item
                }
                new_json.append(new_obj)

        df = pd.DataFrame(new_json)
        df = df.sort_values(by=['Date','State_Name'])

        df.to_csv(DATA_URL, mode='a', header=False, index=False)
        print ('State Level Data: Successful')
    else:
        print ('State Level Data: Nothing to add')
else:
    print ('State Level Data: HTTP ERROR')

# District Level data
resp = requests.get("https://api.covid19india.org/state_district_wise.json")
if (resp.status_code == 200):
    resp = resp.json()

    DATA_URL = (
    "D:/Covid-Data-Visualization/district_level.csv"
    )

    new_json=[]

    for i in resp.keys():
        districtData = resp[i]['districtData']
        for j in districtData:
            new_obj = {
             'State_Name': i,
             'District_Name':j,
             'Active': districtData[j]['active'],
             'Confirmed': districtData[j]['confirmed'],
             'Deceased': districtData[j]['deceased'],
             'Recovered': districtData[j]['recovered']
            }
            new_json.append(new_obj)

    df = pd.DataFrame(new_json)
    df.to_csv(DATA_URL, index=False)
    print ('District Level Data: Successful')
else:
    print ('District Level Data: HTTP ERROR')

# Test Data
DATA_URL = (
"D:/Covid-Data-Visualization/state_level_tested_daily.csv"
)

resp = requests.get("https://api.covid19india.org/state_test_data.json")
new_json = []
if resp.status_code==200:
    resp = resp.json()
    df = pd.DataFrame(resp['states_tested_data'])
    df = df[['updatedon','totaltested','state']]

    for (item,row) in df.iterrows():
        date = datetime.strptime(row['updatedon'],'%d/%m/%Y')
        date_string = datetime.strftime(date,'%d-%b-%Y')
        new_obj = {
            'Date' : date_string,
            'Tested' : row['totaltested'],
            'State_Name' : row['state']
        }
        new_json.append(new_obj)

    df = pd.DataFrame(new_json)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df.fillna(0, inplace=True)

    df.to_csv(DATA_URL,index=False)
    print ('Test Data: Successful')
else:
    print ('Test Data: HTTP ERROR')
