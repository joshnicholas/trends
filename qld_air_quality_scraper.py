import xml.etree.ElementTree as ET
import requests
import pandas as pd 

url = 'https://apps.des.qld.gov.au/air-quality/xml/feed.php?category=1&region=ALL'
headers = {'user-agent': 'my-app/0.0.1'}
response = requests.get(url, headers=headers)

root = ET.fromstring(response.content)

csv_path = "qld_air_quality.csv"
latest_csv_path = "latest_qld_air_quality.csv"

old_df = pd.read_csv(csv_path)

measurement_hour = root.find('category').attrib['measurementhour']
measurement_date = root.find('category').attrib['measurementdate']

current_day = old_df[old_df['measurementdate'] == measurement_date]

if int(measurement_hour) in current_day['measurementhour'].values.tolist():
    pass
    print("Nup")
else:

    listo = []

    for station in root.iter('station'):
        dicto = {'station': f"{station.attrib['name']}", "longitude": f"{station.attrib['longitude']}", "latitude": f"{station.attrib['latitude']}", 'measurementhour': f"{measurement_hour}", 'measurementdate': f"{measurement_date}"}
        for thingy in station:
            reading = {f"{thingy.attrib['name']}":f"{thingy.attrib['index']}"}

            dicto.update(reading)
        listo.append(dicto)

    new_data = pd.DataFrame(listo)

    old_df = old_df.append(new_data)

    print(old_df)

    with open(csv_path, "w") as f:
        old_df.to_csv(f,index=False)
               
    with open(latest_csv_path, "w") as f:
        new_data.to_csv(f,index=False)
