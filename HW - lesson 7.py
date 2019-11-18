from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import json, pandas as pd
driver = webdriver.Chrome()
driver.get('https://mvideo.ru')
assert 'М.Видео' in driver.title
z = 0
while z < 6:
    elem = driver.find_elements_by_class_name('sel-hits-button-next')
    elem[2].send_keys(Keys.RETURN)
    z += 1
goods = driver.find_elements_by_class_name("sel-product-tile-title")
for sku in goods[4:20]:
    name = sku.get_attribute('data-product-info')
    dict = json.loads(name)
    db = pd.DataFrame(columns=dict.keys(), index=[])
j=0
for sku in goods[4:20]:
    name = sku.get_attribute('data-product-info')
    dict = json.loads(name)
    db.loc[j, dict.keys()] = [n for n in dict.values()]
    j += 1
print(db)
db.to_csv('1.csv')

