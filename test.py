import pandas as pd
import json

#read csv
transactions = pd.read_csv('test.csv')

df_dict = transactions.to_dict(orient='records')
for row in df_dict:
    if row['Currency'] == 'nzd':
        row['Instrument code'] = str(row['Instrument code']) + '.NZ'
        
    elif row['Currency'] == 'aud':
        row['Instrument code'] = str(row['Instrument code']) + '.AX'

transactions = pd.DataFrame.from_dict(df_dict, orient="columns")



trans_str = transactions.to_json(orient="records")
json_str = json.dumps([{'activities':json.loads(trans_str)}])
json_obj = json.loads(json_str)

with open('test.json', 'w') as outfile:
   outfile.write(json.dumps(json_obj, indent=2))