from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import datetime
import json

service = Service('chromedriver.exe')
browser = webdriver.Chrome(service=service)


browser.get("https://facebook.com")

# Đọc cookie từ file
with open('cookie.json','r') as file:
    cookies = json.load(file)

# Thêm từng cookie vào trình duyệt
for cookie in cookies:
    browser.add_cookie(cookie)

browser.get('https://facebook.com')

sleep(1)
# page_instance = Page()
# listPages = page_instance.all()
# for page in listPages:
#     link = page['link']
#     browser.get(link)
#     crawl = Crawl(browser,page)
#     crawl.get()
#     sleep(2)

browser.close() # Đóng