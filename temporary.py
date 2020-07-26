import requests
import pandas as pd
from datetime import datetime
import numpy as np

DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_tested_daily.csv"
)

data = pd.read_csv(DATA_URL)
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by=['Date'])
data = data.iloc[-1:]
dt = data['Date'].values[0]

resp = requests.get("https://api.covid19india.org/state_test_data.json")
new_json = []
if resp.status_code==200:
    resp = resp.json()
    df = pd.DataFrame(resp['states_tested_data'])
    df = df[['updatedon','totaltested','state']]

    if not (df.empty):
        for (item,row) in df.iterrows():
            date = datetime.strptime(row['updatedon'],'%d/%m/%Y')
            date_string = datetime.strftime(date,'%d-%b-%Y')
            new_obj = {
                'Date' : date_string,
                'Tested' : row['totaltested'],
                'State_Name' : row['state']
            }
            new_json.append(new_obj)
else:
    print ('HTTP ERROR')

df = pd.DataFrame(new_json)
df = df.replace(r'^\s*$', np.nan, regex=True)
df.fillna(0, inplace=True)

df.to_csv(DATA_URL)
print ('Successful')
