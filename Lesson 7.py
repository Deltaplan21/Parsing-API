from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://mail.ru')
sleep(1)
elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.RETURN)
sleep(1)
elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('Password172')
elem.send_keys(Keys.RETURN)
sleep(10)
db = pd.DataFrame(columns=['От кого', 'Кому', 'Тема', 'Текст'], index=[])
for i in range(0,7):
    elem = driver.find_elements_by_xpath('//a[@class="llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal"]')[i]
    elem.click()
    sleep(1)
    elem = driver.find_elements_by_class_name('letter__contact-item')
    mail = elem[0].get_attribute('title')
    to = elem[1].get_attribute('title')
    elem = driver.find_element_by_class_name('thread__subject')
    subject = elem.text
    elem = driver.find_element_by_class_name('letter__body')
    text = elem.text
    db.loc[i, db.columns] = mail,to,subject,text
    driver.back()
    sleep(1)
    print(f'{i+1}-е письмо')
print(db)

