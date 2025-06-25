import time
import random
import json
import os.path
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parse.src.constants import PROXIES, USER_AGENTS

def setup_driver(proxy=None):
    options = uc.ChromeOptions()

    options.add_argument(f'--user-agent={random.choice(USER_AGENTS)}')

    if proxy:
        options.add_argument(f'--proxy-server=http://{proxy}')
    
    driver = uc.Chrome(options=options)
    return driver

def get_info(driver):
    title = driver.find_element(By.CSS_SELECTOR, '[data-marker="item-view/title-info"]').text
    price = driver.find_element(By.CSS_SELECTOR, '[data-marker="item-view/item-price"].hQ3Iv').get_attribute('content')
    address = driver.find_elements(By.CLASS_NAME, 'xLPJ6')
    address = address[0].text if len(address) == 1 else ''
    district = driver.find_elements(By.CLASS_NAME, 'tAdYM')
    district = district[0].text if len(district) == 1 else ''
    map = driver.find_element(By.CLASS_NAME, 'j2TYE')
    lat = map.get_attribute('data-map-lat')
    lon = map.get_attribute('data-map-lon')

    properties = []
    uls = driver.find_elements(By.CLASS_NAME, 'HRzg1')
    for ul in uls:
        items = ul.find_elements(By.TAG_NAME, 'li')
        for item in items:
            properties.append((item.text.strip().split(':')))
    info = {
        'title': title,
        'price': price,
        'address': address,
        'district': district,
        'lat': lat,
        'lon': lon,
    }

    for prop in properties:
        key, value = prop
        info[key] = value

    return info

def parse_urls(urls, proxy=None):
    driver = setup_driver(proxy)

    if proxy != None:
        driver.get('https://avito.ru')
        time.sleep(random.uniform(2, 4))

        if proxy == PROXIES[0]:
            cookies_path = './src/cookies_...json'
        else:
            cookies_path = './src/cookies_...json'

        with open(cookies_path, 'r', encoding='utf-8') as f:
            cookies = json.load(f)

        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                del cookie['sameSite']
            driver.add_cookie(cookie)

    list_info = []
    for url in urls:
        try:
            driver.get(url)
            time.sleep(random.uniform(3, 6))

            print(url)
            print(proxy)

            check_captcha = True if len(driver.find_elements(By.ID, 'geetest_captcha')) > 0 else False

            if check_captcha:
                print('check captcha true')
                button = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[name="submit"]'))
                )
                button.click()
                time.sleep(random.uniform(15, 20))

            info = get_info(driver)
            print(info)
            list_info.append((url, info))

        except Exception as e:
            print(f'Ошибка при обработке {url}: {e}')

    driver.quit()
    return list_info


urls = []
with open('./src/links.txt', 'r', encoding='utf-8') as f:
    for line in f:
        urls.append(line.strip())

data = {}

l = r = 0
N = len(urls)

last_proxies = []

while l < N:
    r = min(l + random.randint(3, 6), N)

    available_proxies = [p for p in PROXIES if last_proxies.count(p) < 2 or p != last_proxies[-1] or len(last_proxies) < 2]
    if not available_proxies:
        available_proxies = PROXIES.copy()
    proxy = random.choice([p for p in last_proxies if p != last_proxies[-1]] if len(last_proxies) >= 2 else available_proxies)

    info = parse_urls(urls[l:r], proxy)
    if len(info) > 0:
        for key, value in info:
            data[key] = value
    if os.path.exists('result.json'):
        with open("result.json", 'r', encoding='utf-8') as f:
            old_data = json.load(f)
    else:
        old_data = {}

    old_data.update(data)

    with open("result.json", 'w', encoding='utf-8') as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)
    l = r

    last_proxies.append(proxy)
    if len(last_proxies) > 2:
        last_proxies.pop(0)