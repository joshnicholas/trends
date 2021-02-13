import pandas as pd
from pytrends.request import TrendReq
import datetime
import pytz

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
brissie = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
bris_reverse_date = brissie.strftime('%Y-%m-%d')
bris_hour = brissie.strftime('%H')

heado = [str(x).strip() for x in range(0,20)]
heado.insert(0, "What")
heado.append("Date")
heado.append("Hour")

csv_path = 'Aus_google_trends.csv'
old_df = pd.read_csv(csv_path)

current_day = old_df[old_df['Date'] == bris_reverse_date]

if int(bris_hour) in current_day['Hour'].values.tolist():
    pass
    print("Nup")
else:

    pytrend = TrendReq(hl='en-US', tz=360)

    df = pytrend.trending_searches(pn='australia')
    df = df.rename(columns={0: "Google trending searches"})

    melted = df.T.reset_index()
    melted['Date'] = bris_reverse_date
    melted['Hour'] = bris_hour
    melted.columns = heado


    old_df = old_df.append(melted)

    print(old_df)

    with open(csv_path, "w") as f:
        old_df.to_csv(f,index=False)
