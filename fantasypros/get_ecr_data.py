import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

BASE_URLS = {
    "PPR": "https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php",
    "HALF_PPR": "https://www.fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php",
    "STANDARD": "https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php"
}

#Christian McCaffreyC. McCaffrey CAR
def get_player_name(name):
    name = ' '.join(name.split()[:2])
    first_name = name.split()[0]
    last_name = name.split()[-1]
    last_name = [char for char in last_name]
    last_name = ''.join(last_name[:-2])

    name = ' '.join([first_name, last_name])

    return name

for league_format, BASE_URL in BASE_URLS.items():
    res = requests.get(BASE_URL)

    if res.ok:
        html = res.content
        soup = BS(html, 'html.parser')
        table = soup.find('table', {'id': 'rank-data'})

        df = pd.read_html(str(table))[0]

        df = df[1:]

        df = df.drop('WSID', axis=1)

        df['Overall (Team)'] = df['Overall (Team)'].astype(str)

        df['Team'] = df['Overall (Team)'].apply(
            lambda x: x.split()[-1]
        )

        df['Player'] = df['Overall (Team)'].apply(get_player_name)

        df = df.drop(['Overall (Team)', 'vs. ADP'], axis=1)

        df['Rank'] = df['Rank'].astype(str)

        for _, row in df.iterrows():
            if 'Tier' in row['Rank']:
                df = df.loc[df['Rank'] != row['Rank']]

        columns = [column for column in list(df.columns) if column != 'Player' and column != 'Team']
        columns = ['Player', 'Team'] + columns
        df = df[columns]

        df.to_csv(f'fantasypros/ecr/{league_format}_ECR.csv')
