import pandas as pd
import json
import requests
from datetime import datetime
from math import ceil


def send(payload):
    url = "http://localhost:3333/api/v1/import"

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjhhMjE4YjJjLTdmMzgtNDU1NC1hODQ5LTVmMDlkNTg2YTM0MyIsImlhdCI6MTY3NTY0NTIyNywiZXhwIjoxNjkxMTk3MjI3fQ.Objay0z0AlfsuehulOHRPPlZY1A15Phw4kM_kYKSvwU',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


#read csv
transactions = pd.read_csv('transReport_latest.csv')

#prepare format for json
transactions.drop(['Order ID', 'Market code', 'Exchange rate', 'Amount', 'Transaction method', 'Comments'], axis=1, inplace=True)
transactions['dataSource'] = 'YAHOO'
transactions['accountId'] = None

#rearrange columns to fit json format
column_names = list(transactions.columns)
order = [8,6,7,0,5,2,1,4,3]
column_names = [column_names[i] for i in order]
transactions = transactions[column_names] 

transactions.columns = ['accountId','currency', 'dataSource','date', 'fee', 'quantity', 'symbol', 'type', 'unitPrice']


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
row_count = transactions.shape[0]
packet_size = ceil(row_count / 10)

#send packets 
start_i = 0
for end_i in range(packet_size, row_count+1, packet_size):
    to_send = transactions.iloc[:end_i]
    transactions = transactions.iloc[end_i+1:]
    
    trans_str = to_send.to_json(orient="records")
    json_str = json.dumps({'activities':json.loads(trans_str)})
    json_obj = json.loads(json_str)
    to_send = json.dumps(json_obj)    

    send(to_send)
    print(f'sent {start_i}:{end_i}')   
    start_i = end_i+1


# #write json object to file
# json_obj = json.loads(json_str)
# with open('test.json', 'w') as outfile:
#     to_print = json.dumps(json_obj, indent=2)
#     outfile.write(to_print)
    
