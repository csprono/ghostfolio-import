import json

with open('error.json', 'r') as f:
    error = json.load(f)
    
print(error['error'])