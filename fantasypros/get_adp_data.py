from bs4 import BeautifulSoup as BS
import requests
import pandas as pd

BASE_URLS = {
    'PPR': 'https://www.fantasypros.com/nfl/adp/ppr-overall.php',
    'HALF_PPR': 'https://www.fantasypros.com/nfl/adp/half-point-ppr-overall.php',
    'STANDARD': 'https://www.fantasypros.com/nfl/adp/overall.php'
}

for league_format, BASE_URL in BASE_URLS.items():
    res = requests.get(BASE_URL)
    if res.ok:
        soup = BS(res.content, 'html.parser')
        table = soup.find('table', {'id': 'data'})
        df = pd.read_html(str(table))[0]

        df = df[['Player Team (Bye)', 'POS', 'AVG']]

        df['PLAYER'] = df['Player Team (Bye)'].apply(lambda x: ' '.join(x.split()[:-2])) # removing the team and position
        df['POS'] = df['POS'].apply(lambda x: x[:2]) # removing the position rank
        
        df = df[['PLAYER', 'POS', 'AVG']].sort_values(by='AVG')
        df.to_csv(f'fantasypros/adp/{league_format}_ADP.csv')
    
    else:
        print('oops, something didn\'t work right', res.status_code)
        break