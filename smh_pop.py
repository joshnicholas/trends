import pandas as pd 
from bs4 import BeautifulSoup as bs 
import pytz
import datetime

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

csv_path = 'data/smh_pop.csv'
old_df = pd.read_csv(csv_path)

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
brissie = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
bris_reverse_date = brissie.strftime('%Y-%m-%d')
bris_hour = brissie.strftime('%H')


driver = webdriver.Chrome(options=chrome_options)
start_url = "https://smh.com.au"
driver.get(start_url)

soup = bs(driver.page_source.encode("utf-8"), 'html.parser')

container = soup.find("section", {"data-an-name": "Most Popular"})
items = container.find_all("h3")
items = [{"SMH most viewed":f"{x.text.strip()}"} for x in items]

df = pd.DataFrame(items)

df = df.T.reset_index()
headers = [f"{x}" for x in range(0,8)]
headers.insert(0, "What")
df.columns = headers

df['Date'] = bris_reverse_date
df['Hour'] = bris_hour

old_df = old_df.append(df)

old_df['Hour'] = old_df['Hour'].astype(str)
old_df['Date'] = old_df['Date'].astype(str)

old_df['Hour'] = old_df['Hour'].apply(lambda x: '0' + x if len(x) < 2 else x)

old_df = old_df.drop_duplicates(subset=["Date", "Hour"])
old_df = old_df.sort_values(by=["Date", "Hour"], ascending=True)

with open(csv_path, "w") as f:
    old_df.to_csv(f, index=False)
