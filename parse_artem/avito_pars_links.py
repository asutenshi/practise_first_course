# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

# %%
driver = webdriver.Chrome()

links = []

for i in range(21):
    driver.get(f"https://www.avito.ru/irkutsk/kommercheskaya_nedvizhimost/sdam?p={i}")
    elements = driver.find_elements("css selector", "[data-marker='item-title']")
    for elem in elements:
        links.append(elem.get_attribute("href"))

    pause = random.uniform(5, 10)
    time.sleep(pause)

print(links)

# %%

print(len(links))

with open('./out/links.txt', "w", encoding="utf-8") as f:
    for link in links:
        f.write(link + '\n')

# %%
