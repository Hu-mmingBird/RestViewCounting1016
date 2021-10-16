#-*- encoding: utf-8 -*-
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import sys
import network
key_col = input()
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = THIS_FOLDER + '/automationproj-327806-6e9bf5c39245.json'
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    JSON_PATH, scope)
gc = gspread.authorize(credentials)
gc1 = gc.open('에프터마케팅18.10~의 사본').worksheet('2019년 월보장')
cntsch = gc1.col_values(1)
keyword = gc1.col_values(3)
company = gc1.col_values(5)
info = {'cntsch':[],'keyword': [], 'company': [], 'date': []}
for cs, k, c in zip(cntsch,keyword,company):
    if k == 'END' and c == 'END':
        break
    info['cntsch'].append(cs)
    info['keyword'].append(k)
    info['company'].append(c)
    num = 0
    if k != '' and c != '':
        num = network.counting(c, k)
        if num == -1:
            info['date'].append('x')
            info['date'].append('')
        else:
            info['date'].append('1')
            info['date'].append(str(num))
    elif cs=='':
        info['date'].append('')
start_col=key_col+'3'
end_col=key_col+str(len(info['date']))
date=info['date'][2:]
print(date)
date = list(map(list,date))
gc1.update(start_col+':'+end_col,date)
