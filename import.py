import pandas as pd
import json
import requests
from datetime import datetime

authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjhhMjE4YjJjLTdmMzgtNDU1NC1hODQ5LTVmMDlkNTg2YTM0MyIsImlhdCI6MTY3NTY0MTQ0NSwiZXhwIjoxNjkxMTkzNDQ1fQ.uTw2jCIhLXOwhhQUDFdQruYUGeyddcgP31cN8LSjEL8'

#read csv
transactions = pd.read_csv('transReport_latest.csv')

#prepare format for json
transactions.drop(['Order ID', 'Market code', 'Exchange rate', 'Amount', 'Transaction method'], axis=1, inplace=True)
transactions['dataSource'] = 'YAHOO'
transactions['accountId'] = '52953899-2a27-4b4a-a6e2-51cca9d82387'

#rearrange columns to fit json format
column_names = list(transactions.columns)
order = [8,6,7,0,5,2,1,4,3]
column_names = [column_names[i] for i in order]
transactions = transactions[column_names] 

#rename columns
transactions.columns = ['dataSource','currency', 'comments', 'date', 'fee', 'quantity', 'symbol', 'type', 'unitPrice']
transactions['accountId'] = None

#specify market in symbol code
df_dict = transactions.to_dict(orient='records')
for row in df_dict:
    if row['currency'] == 'nzd':
        row['symbol'] = str(row['symbol']) + '.NZ'
        row['currency'] = 'NZD'
    elif row['currency'] == 'aud':
        row['symbol'] = str(row['symbol']) + '.AX'
        row['currency'] = 'AUD'
    elif row['currency'] == 'usd':
        row['currency'] = 'USD'
    
    string = row['date'][:19]
    time_str = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
    row['date'] = time_str.isoformat()

#convert dataframe to json object
transactions = pd.DataFrame.from_dict(df_dict, orient="columns")
trans_str = transactions.to_json(orient="records")
json_str = json.dumps([{'activities':json.loads(trans_str)}])
json_obj = json.loads(json_str)

#write json object to file and send to address
with open('test.json', 'w') as outfile:
    to_print = json.dumps(json_obj, indent=2)
    outfile.write(to_print)
    requests.post('http://192.168.1.79:3333/api/v1/import', json=to_print, headers=authToken)

