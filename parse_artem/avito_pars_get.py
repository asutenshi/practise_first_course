# %%
import requests
import pandas as pd
from collections import defaultdict
import time
import random

# %%
def get_info(data):
    info_data = []
    for item in data['items']:
        info = defaultdict(lambda: 0)
        info['title'] = item['title']
        info['price'] = item['priceDetailed']['value']
        info['normalizedPrice'] = item['normalizedPrice']
        info['formattedAddress'] = item['geo']['formattedAddress']
        info['lat'] = item['coords']['lat']
        info['lng'] = item['coords']['lng']
        info_data.append(info)
    return info_data

# %%
collected_info = []
for i in range(1, 21):
    url = f"https://www.avito.ru/js/1/map/items?categoryId=42&locationId=628970&correctorMode=0&page={i}&map=1&params[536]=5546&params[178133]=1&verticalCategoryId=1&rootCategoryId=4&localPriority=0&disabledFilters[ids][0]=byTitle&disabledFilters[slugs][0]=bt&viewPort[width]=500&viewPort[height]=845&limit=980&countAndItemsOnly=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error {response.status_code}")
    else:
        data = response.json()
        collected_info += get_info(data)
    pause = random.uniform(2, 5)
    time.sleep(pause)

# %%
df = pd.DataFrame(collected_info)
df.to_csv('./out/output.csv', index=False, encoding='utf-8')