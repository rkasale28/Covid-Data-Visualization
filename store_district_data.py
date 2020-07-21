import requests
import pandas as pd

resp = requests.get("https://api.covid19india.org/state_district_wise.json")
resp = resp.json()

DATA_URL = (
"C:/Users/Rohit/Documents/Self Learning/Streamlit/district_level.csv"
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
print ('Successful')
