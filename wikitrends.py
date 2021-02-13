import pandas as pd
import requests
import datetime
import json
import requests

csv_path = 'wiki_trends.csv'

utc_now = datetime.datetime.utcnow()
utc_then = utc_now - datetime.timedelta(days=1)

utc_month = datetime.date.strftime(utc_then, '%m')
utc_year = datetime.date.strftime(utc_then, '%Y')
utc_day = datetime.date.strftime(utc_then, '%d')

utc_reverse_date = utc_then.strftime('%Y-%m-%d')
utc_hour = utc_then.strftime('%H')

heado = [str(x).strip() for x in range(0,50)]
heado.insert(0, "What")
heado.append("UTC Date")

wiki_linko = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{utc_year}/{utc_month}/{utc_day}"

headers = {'user-agent': 'Josh'}

wiki_r = requests.get(wiki_linko, headers=headers)

wiki_trends = json.loads(wiki_r.text)
wiki_trends = wiki_trends['items'][0]['articles']
wiki_trends = wiki_trends[2:52]
wiki_trends = [x['article'] for x in wiki_trends]

df = pd.DataFrame(wiki_trends)
df = df.rename(columns={0: "Wiki trends"})
df['Wiki trends'] = df['Wiki trends'].str.replace("_", " ")

melted = df.T.reset_index()
melted['UTC Date'] = utc_reverse_date
melted.columns = heado


old_df = pd.read_csv(csv_path)

old_df = old_df.append(melted)
old_df = old_df.drop_duplicates(subset="UTC Date")

with open(csv_path, "w") as f:
    old_df.to_csv(f, index=False, header=True)
