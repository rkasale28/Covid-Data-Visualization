import requests
import pandas as pd
from datetime import datetime
import numpy as np

DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/state_level_tested_daily.csv"
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

    print ('Test Data: Successful')
else:
    print ('Test Data: HTTP ERROR')
