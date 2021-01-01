import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

pd.set_option('display.max_columns', None)

URL = 'https://www.pro-football-reference.com/years/2020/fantasy.htm'

res = requests.get(URL)
soup = BS(res.content, 'html.parser')
table = soup.find('table', {'id': 'fantasy'})
df = pd.read_html(str(table))[0]
df.columns = df.columns.droplevel(level=0)

#removing filler rows
df = df.loc[df['Player'] != 'Player']

#fixing player names that have astericks
df['Player'] = df['Player'].apply(lambda x: x.split('*')[0].strip())

#Column names:
#Player,Tm,Pos,Age,G,GS,Tgt,Rec,PassingYds,PassingTD,PassingAtt,RushingYds,
#RushingTD,RushingAtt,ReceivingYds,ReceivingTD,FantasyPoints,Int,Fumbles,FumblesLost

df['PassingYds'] = df['Yds'].iloc[:, 0]
df['RushingYds'] = df['Yds'].iloc[:, 1]
df['ReceivingYds'] = df['Yds'].iloc[:, 2]

df['PassingTD'] = df['TD'].iloc[:, 0]
df['RushingTD'] = df['TD'].iloc[:, 1]
df['ReceivingTD'] = df['TD'].iloc[:, 2]

df['PassingAtt'] = df['Att'].iloc[:, 0]
df['RushingAtt'] = df['Att'].iloc[:, 1]

df = df.rename(columns={
    'FantPos': 'Pos', 'FantPt': 'FantasyPoints', 'Fmb': 'Fumbles', 'FL': 'FumblesLost'
})

df = df[[
    'Player','Tm','Pos','Age','G','GS','Tgt','Rec','PassingYds','PassingTD','PassingAtt',
    'RushingYds','RushingTD','RushingAtt','ReceivingYds','ReceivingTD','FantasyPoints',
    'Int','Fumbles','FumblesLost'
]]

df.to_csv('yearly/2020.csv', index=False)
