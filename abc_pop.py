import requests
import pandas as pd 
from bs4 import BeautifulSoup as bs 
import pytz
import datetime

csv_path = 'abc_pop.csv'
old_df = pd.read_csv(csv_path)

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
brissie = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
bris_reverse_date = brissie.strftime('%Y-%m-%d')
bris_hour = brissie.strftime('%H')

r = requests.get("https://www.abc.net.au/news/")
soup = bs(r.text, 'html.parser')
div = soup.find("div", {"data-component":"MostPopularStories"})

items = div.find_all("a", {"data-component":"Link"})
items = [{"ABC most viewed":f"{x.text.strip()}"} for x in items]

df = pd.DataFrame(items)

df = df.T.reset_index()
headers = [f"{x}" for x in range(0,5)]
headers.insert(0, "What")
df.columns = headers

df['Date'] = bris_reverse_date
df['Hour'] = bris_hour

old_df = old_df.append(df)

old_df['Hour'] = old_df['Hour'].astype(str)
old_df['Date'] = old_df['Date'].astype(str)

old_df = old_df.drop_duplicates(subset=["Date", "Hour"])
old_df = old_df.sort_values(by=["Date", "Hour"], ascending=True)

with open(csv_path, "w") as f:
    old_df.to_csv(f, index=False)
