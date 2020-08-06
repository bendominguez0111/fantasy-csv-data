from bs4 import BeautifulSoup as BS
import requests
import pandas as pd; pd.set_option('display.max_columns', None);

ENDPOINT = "https://www.fantasypros.com/nfl/reports/snap-counts/?year={year}"

final_df = pd.DataFrame()

for year in range(2016, 2020):
    res = requests.get(ENDPOINT.format(year=year))

    soup = BS(res.content, 'html.parser')

    table = soup.find('table', {'id': 'data'})

    df = pd.read_html(str(table))[0]

    df.columns = df.columns[:3].tolist() + [f'Week {i}' for i in df.columns[3:-2]] + df.columns[-2:].tolist()

    df['Year'] = year

    cols = df.columns[:3].tolist() + df.columns[-1:].tolist() + df.columns[3:-1].tolist()
    df = df[cols]

    final_df = pd.concat([final_df, df])

final_df.to_csv('fantasypros/snapcounts.csv')