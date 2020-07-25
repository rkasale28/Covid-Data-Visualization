import requests
import pandas as pd
import numpy as np

resp = requests.get('https://api.covid19india.org/state_test_data.json')
resp = resp.json()

data = pd.read_csv("C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_tested_daily.csv")
data['Date'] = pd.to_datetime(data['Date'])
data['Date'] = data['Date'].dt.strftime('%d-%b-%y')
data = data.iloc[-1:]
dt = data['Date'].values[0]

df = pd.DataFrame(resp['states_tested_data'])
df = df[['updatedon','state','totaltested']]
df = df[df['updatedon']>dt]
df = df.replace(r'^\s*$', np.nan, regex=True)
df = df.rename(columns={'updatedon':'Date'})
df.fillna(0,inplace=True)
df.to_csv("C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_tested_daily.csv",mode='a', header=False, index=False)
