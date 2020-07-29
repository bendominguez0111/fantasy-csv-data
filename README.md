# Fantasy Football Data Sets

If you are looking to run the scripts we've provided for locally updating fantasypros data, clone this repo and install dependencies.

    pip install -r requirements.txt

## Strength of Schedule data
Strength of Schedule data is available in the sos directory. Data is available going back to 1999. To load this data in pandas using the following the following url format:
https://raw.githubusercontent.com/fantasydatapros/data/master/sos/{year}.csv

For example, in pandas do the following:

    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/sos/1999.csv', index_col=0)
    df.index = df.index.rename('Team')

## 2019 play by play data
2019 play by play data is exposed through this url:
https://raw.githubusercontent.com/fantasydatapros/data/master/2019pbp.csv

To load the data in pandas:

    import pandas as pd

    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/2019pbp.csv', index_col=0)

## Weekly Fantasy Stats
Weekly stats going back to 1999 are available are exposed through the following url format

https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{year}/week{week}.csv

To grab weekly data for year 2019, week 1 in pandas, you would do:

    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/2019/week1.csv')

## Yearly Fantasy stats
Yearly fantasy stats are available going back to 1970.

The url format:
https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/{year}.csv

To grab yearly data for 2019 in pandas, do the following:

    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2019.csv')

## FantasyPros ECR data
Fantasy pros data is provided including projections and ECR data. Two python scripts are provided to be able to update your CSV files as new data rolls in.

To update your ECR data simply run

    python get_ecr_data.py

If you want to use the CSV data that's hosted in this repo (although be aware it may be outdated and you may want to just run the script provided locally), you would do:

    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/ECR.csv', index_col=0)

## FantasyPros Projection data
Fantasy pros projection data is exposed in a similar fashion. To update things locally, run

    python get_fantasy_pros_projection_data.py

And to load it in pandas from this repo

    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/fp_projections.csv', index_col=0)




