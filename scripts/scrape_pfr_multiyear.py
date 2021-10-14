import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

from pathlib import Path

def scrape_pfr(year, directory):

    try:
        # check directory if not exits create create the directory
        Path(directory).mkdir(parents=True, exist_ok=True)

        pd.set_option('display.max_columns', None)

        URL = f'https://www.pro-football-reference.com/years/{year}/fantasy.htm'

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

        df.to_csv(f'{directory}/{year}.csv', index=False)

        print(f'scrape in year: {year} ,successful')
    except Exception as e:
        # write error to logfile
        with open('error_log', 'a') as logfile:
            print(f'error msg scrape in year: {year}\n{e}\n', file=logfile)
        print(f'scrape in year: {year} ,found error see in log file')

if __name__ == '__main__':

    # scape year config
    start_year = 2000
    end_year = 2021
    # csv export directory
    directory = 'yearly'

    while start_year <= end_year:
        scrape_pfr(start_year, directory)
        start_year += 1

