from selenium import webdriver
import json
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from facebook.crawl import Crawl
from mongo.collections import pages

service = Service('chromedriver.exe') # Khởi tạo dịch vụ
browser = webdriver.Chrome(service=service) # Mở chorm

browser.get("https://facebook.com") # Chuyển hướng

# Đọc cookie từ file
with open('cookie.json','r') as file:
    cookies = json.load(file)

# Thêm từng cookie vào trình duyệt
for cookie in cookies:
    browser.add_cookie(cookie)

browser.get('https://facebook.com')

sleep(1)

listPages = pages.find() #lấy danh sách page
for page in listPages:
    link = page['link']
    browser.get(link)
    crawl = Crawl(browser,page)
    crawl.get()
    sleep(2)

browser.close() # Đóng
