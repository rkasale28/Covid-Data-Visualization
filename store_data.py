import requests
import pandas as pd
from datetime import datetime

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
resp = resp.json()

df = pd.DataFrame(resp['states_daily'])
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['date','status'])

DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_daily.csv"
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
for (item,row) in df.iterrows():
    date = datetime.strftime(row.index.get_level_values(0)[0],'%d-%b-%y')
    new_obj = {
        'Date' : date,
        'Confirmed' : row[date]['Confirmed'],
        'Deceased' :row[date]['Deceased'],
        'Recovered': row[date]['Recovered'],
        'State_Name': item
    }
    new_json.append(new_obj)

df = pd.DataFrame(new_json)
df.to_csv(DATA_URL, mode='a', header=False, index=False)
print ('Successful')
