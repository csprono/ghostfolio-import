import pandas as pd
import json

#read csv
transactions = pd.read_csv('transReport_latest.csv')

#prepare format for json
transactions.drop(['Order ID', 'Market code', 'Exchange rate', 'Amount', 'Transaction method'], axis=1, inplace=True)

#rearrange columns to fit json format
column_names = list(transactions.columns)
print(column_names)
order = [7,0,6,3,1,5,4]
column_names = [column_names[i] for i in order]
transactions = transactions[column_names] 

#rename columns
transactions.columns = ['currency', 'date', 'fee', 'quantity', 'symbol', 'type', 'unitPrice', 'marketCode']

#merge market code and symbol columns
df_dict = transactions.to_dict(orient='records')
for row in df_dict:
    if row['currency'] == 'nzd':
        row['symbol'] = str(row['symbol']) + '.NZ'
    elif row['currency'] == 'aud':
        row['symbol'] = str(row['symbol']) + '.AX'
transactions = pd.DataFrame.from_dict(df_dict, orient="columns")



#rudimentary json (not final format but close)
json_str = transactions.to_json(orient='records')
json_test = json.loads(json_str)
