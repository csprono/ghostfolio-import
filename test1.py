from datetime import datetime

string = '2020-03-25 23:00:00 (UTC)'
string = string[:19]
time_str = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
print(time_str.isoformat())