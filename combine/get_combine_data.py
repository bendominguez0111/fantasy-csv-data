import requests
from bs4 import BeautifulSoup as BS
import os
import pandas as pd; pd.set_option('display.max_columns', None);

ENDPOINT = "https://www.pro-football-reference.com/play-index/nfl-combine-results.cgi?request=1&year_min={year}&year_max={year}&height_min=65&height_max=82&weight_min=140&weight_max=400&pos%5B%5D={position}&show=p&order_by=year_id"

base_dir = os.path.abspath(os.path.dirname(__file__))
combine_data_dir = os.path.join(base_dir, 'combinedata')

def scrape_pfr_data():
    for year in range(2000, 2020):
        for position in ['WR', 'RB', 'TE', 'QB']:
            res = requests.get(ENDPOINT.format(year=year, position=position))

            soup = BS(res.content, 'html.parser')
            table = soup.find('table')
            df = pd.read_html(str(table))[0]

            df = df.drop('College', axis=1)

            df.to_csv(os.path.join(combine_data_dir, str(year) + '/' + f'{position}.csv'), index=True)

def join_csv_files():
    final_df = pd.DataFrame()
    for year in range(2000, 2020):
        combine_folder = os.path.join(combine_data_dir, str(year))
        for position in ['WR', 'RB', 'TE', 'QB']:
            pos_df = pd.read_csv(os.path.join(combine_folder, f'{position}.csv'))
            final_df = pd.concat([final_df, pos_df])

    final_df.to_csv(os.path.join(base_dir, 'combine00to20.csv'))

if __name__ == '__main__':
    # scrape_pfr_data()
    join_csv_files()