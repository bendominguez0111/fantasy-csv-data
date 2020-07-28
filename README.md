# Fantasy Football Data Sets

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
    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/2019/week1.csv', index_col=0)

## Yearly Fantasy stats
Yearly fantasy stats are available going back to 1970.

The url format:
https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/{year}.csv

To grab yearly data for 2019 in pandas, do the following:

    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2019.csv', index_col=0)


