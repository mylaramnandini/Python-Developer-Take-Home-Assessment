import re
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def clean_text(text):
    # Replace \n, \r, \t with space
    text = re.sub(r'[\n\r\t]', ' ', text)
    # Remove other escape sequences and non-ASCII/control chars
    text = re.sub(r'[^\x20-\x7E]', '', text)

    return text.strip()


option = Options()
option.add_argument("--headless")
driver = webdriver.Chrome(options=option)
# driver1 = webdriver.Chrome()
laptops = []
driver.get('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')
time.sleep(5)
button = driver.find_element(By.CLASS_NAME,'acceptCookies')
button.click()
time.sleep(3)
# # while True:
# total_jobs = driver.find_elements(By.CSS_SELECTOR,'.col-md-4 col-xl-4 col-lg-4')
total_laptops = driver.find_elements(By.CSS_SELECTOR, '.col-md-4.col-xl-4.col-lg-4')
print(len(total_laptops))
for laptop in total_laptops:
    # title = job.find_element(By.CLASS_NAME ,'title').text
    # ratings = job.get_attribute('data-rating')
    try:
        ratings=laptop.find_element(By.CSS_SELECTOR,'p[data-rating]')
        rating = ratings.get_attribute('data-rating')
    except Exception as e:
        print(e)
        rating = None
    try:
        review_count=laptop.find_element(By.CSS_SELECTOR,'span[itemprop="reviewCount"]').text
    except:
        review_count='N/A'
    url = laptop.find_element(By.CLASS_NAME,'title').get_attribute('href')
    # price = job.find_element(By.CSS_SELECTOR,'price.float-end.card-title.pull-right').text
    try:
        price = laptop.find_element(By.CSS_SELECTOR, '.price.float-end.card-title.pull-right').text
    except Exception as e:
        print(e)
        price='N/A'
    driver.get(url)
    time.sleep(3)
    title = description = ''
    try:
        description = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.description.card-text'))
        ).text
        title = driver.find_element(By.CSS_SELECTOR,'.title.card-title').text
    except TimeoutException:
        print("Timed out waiting for the element to load.")

    driver.back()

    laptops.append({
        'title': title,
        'url': url,
        'description':clean_text(description),
        'review_count':review_count,
        'price':price,
        'ratings':rating
    })
    print(len(laptops))
print(len(laptops))

with open("laptop_data.json", "w", encoding="utf-8") as f:
    json.dump(laptops, f, ensure_ascii=False, indent=4)

print("Data saved to laptop_jdata.json")




