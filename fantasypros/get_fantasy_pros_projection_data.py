import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

pd.set_option('display.max_columns', None)

ENDPOINT = """https://www.fantasypros.com/nfl/projections/{pos}.php?week=draft"""

positions = ['te', 'wr', 'qb', 'rb', 'k', 'dst']
dfs = []
for pos in positions:
    res = requests.get(ENDPOINT.format(pos=pos))
    soup = BS(res.content, 'html.parser')
    table = soup.find('table', {'id': 'data'})
    df = pd.read_html(str(table))[0]

    if pos != 'k' and pos != 'dst':
        df.columns = df.columns.droplevel(level=0)

    df['Pos'] = pos.upper()

    if pos != 'dst':

        df['Team'] = df['Player'].apply(lambda x: x.split()[-1])

        df['Player'] = df['Player'].apply(
            lambda x: ' '.join(x.split()[:-1])
        )

    if pos == 'rb':
        df = df.rename({
        'ATT': 'RushingAtt',
        'REC': 'Receptions',
        'FPTS': 'FantasyPoints'
        }, axis=1)

        df['RushingYds'] = df['YDS'].iloc[:, 0]
        df['ReceivingYds'] = df['YDS'].iloc[:, 1]
        df['RushingTD'] = df['TDS'].iloc[:, 0]
        df['ReceivingTD'] = df['TDS'].iloc[:, 1]

        df = df.drop([
            'YDS', 'TDS'
        ], axis=1)

        ordered_cols = [
        'Player', 'Team', 'Pos', 'RushingAtt', 'RushingYds', 'RushingTD', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'FL', 'FantasyPoints'
        ]

        df = df[ordered_cols]

    elif pos == 'qb':
        df = df.rename({
        'CMP': 'PassingCmp',
        'INTS': 'Int',
        'FPTS': 'FantasyPoints'
        }, axis=1)

        df['PassingYds'] = df['YDS'].iloc[:, 0]
        df['RushingYds'] = df['YDS'].iloc[:, 1]
        df['PassingTD'] = df['TDS'].iloc[:, 0]
        df['RushingTD'] = df['TDS'].iloc[:, 1]
        df['PassingAtt'] = df['ATT'].iloc[:, 0]
        df['RushingAtt'] = df['ATT'].iloc[:, 1]

        df = df.drop([
            'YDS', 'TDS', 'ATT'
        ], axis=1)

        ordered_cols = [
            'Player', 'Team', 'Pos', 'PassingAtt', 'PassingCmp', 'PassingYds', 'PassingTD', 'Int', 'RushingAtt', 'RushingYds', 'RushingTD', 'FL', 'FantasyPoints'
        ]

        df = df[ordered_cols]

    elif pos == 'te':
        df = df.rename({
        'REC': 'Receptions',
        'YDS': 'ReceivingYds',
        'TDS': 'ReceivingTD',
        'FPTS': 'FantasyPoints'
        }, axis=1)

        ordered_cols = [
            'Player', 'Team', 'Pos', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'FL', 'FantasyPoints'
        ]

        df = df[ordered_cols]

    elif pos == 'wr':
        df = df.rename({
        'REC': 'Receptions',
        'FPTS': 'FantasyPoints',
        'ATT': 'RushingAtt'
        }, axis=1)

        df['RushingYds'] = df['YDS'].iloc[:, 1]
        df['ReceivingYds'] = df['YDS'].iloc[:, 0]
        df['RushingTD'] = df['TDS'].iloc[:, 1]
        df['ReceivingTD'] = df['TDS'].iloc[:, 0]

        df = df.drop([
            'YDS', 'TDS'
        ], axis=1)

        ordered_cols = [
        'Player', 'Team', 'Pos', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD', 'FL', 'FantasyPoints'
        ]

        df = df[ordered_cols]


    elif pos == 'k':
        df = df.rename({
            'FG': 'FieldGoalsMade',
            'FGA': 'FieldGoalsAttempted',
            'XPT': 'ExtraPointsMade',
            'FPTS': 'FantasyPoints'
        }, axis=1)

        ordered_cols = [
        'Player', 'Team', 'Pos', 'FieldGoalsMade',
        'FieldGoalsAttempted', 'ExtraPointsMade', 'FantasyPoints'
        ]

        df = df[ordered_cols]

    elif pos == 'dst':
        df = df.rename({
        'SACK': 'TotalSacks',
        'INT': 'TotalInt',
        'FR': 'FumblesRecovered',
        'FF': 'FumblesForced',
        'TD': 'DefensiveTDs',
        'SAFETY': 'SafetysForced',
        'PA': 'PointsAllowed',
        'YDS AGN': 'YardsAllowed',
        'FPTS': 'FantasyPoints'
        }, axis=1)

        df['Team'] = df['Player']

        ordered_cols = [
        'Player', 'Team', 'Pos', 'TotalSacks', 'TotalInt', 'FumblesRecovered', 'FumblesForced', 'DefensiveTDs', 'SafetysForced', 'PointsAllowed', 'FantasyPoints'
        ]

        df = df[ordered_cols]

    dfs.append(df)

df = pd.concat(dfs).fillna(0)

columns = [column for column in df.columns if column != 'FantasyPoints'] + ['FantasyPoints']
df = df[columns]
df = df.sort_values(by='FantasyPoints', ascending=False)
df.to_csv('fp_projections.csv')
