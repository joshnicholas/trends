import pandas as pd 
from bs4 import BeautifulSoup as bs 
import pytz
import datetime
import requests
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

csv_path = 'data/tech_meme_pop.csv'
old_df = pd.read_csv(csv_path)

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
brissie = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
bris_reverse_date = brissie.strftime('%Y-%m-%d')
bris_hour = brissie.strftime('%H')

try: 
    driver = webdriver.Chrome(options=chrome_options)
    start_url = "https://www.techmeme.com/"
    driver.get(start_url)

    soup = bs(driver.page_source.encode("utf-8"), 'html.parser')

    container = soup.find("div", {"id": "topcol1"})
    divs = container.find_all("div", class_="clus")
    items = [{"Tech Meme Top Stories":f"{div.find('strong').text.strip()}"} for div in divs][:10]

    df = pd.DataFrame(items)


    df = df.T.reset_index()
    headers = [f"{x}" for x in range(0,10)]
    headers.insert(0, "What")
    df.columns = headers

    df['Date'] = bris_reverse_date
    df['Hour'] = bris_hour
    old_df = old_df.append(df)
except Exception as e:
    print(e)
    pass

try:
    g_r = requests.get("https://www.theguardian.com/au/technology")
    g_soup = bs(g_r.text, 'html.parser')
    g_items = g_soup.find_all("li", class_="most-popular__item")

    g_items = [{"Guardian Oz tech most viewed":f"{x.h3.text.strip()}"} for x in g_items]

    g_df = pd.DataFrame(g_items)

    g_df = g_df.T.reset_index()
    g_headers = [f"{x}" for x in range(0,10)]
    g_headers.insert(0, "What")
    g_df.columns = g_headers

    g_df['Date'] = bris_reverse_date
    g_df['Hour'] = bris_hour


    old_df = old_df.append(g_df)
except Exception as e:
    print(e)
    pass

old_df['Hour'] = old_df['Hour'].astype(str)
old_df['Date'] = old_df['Date'].astype(str)

old_df['Hour'] = old_df['Hour'].apply(lambda x: '0' + x if len(x) < 2 else x)

old_df = old_df.drop_duplicates(subset=["What", "Date", "Hour"])
old_df = old_df.sort_values(by=["Date", "Hour"], ascending=True)


with open(csv_path, "w") as f:
    old_df.to_csv(f, index=False)