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
json_str = transactions.to_json(orient="records")
json_test = json.loads(json_str)
print(json.dumps(json_test, indent=4))
