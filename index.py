from selenium import webdriver
import json
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from facebook.crawl import Crawl
from mongo.connections import pages

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
    crawl = Crawl(page)
    crawl.get()
    sleep(2)

browser.close() # Đóng

# x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k xjl7jj x1xmf6yo x1emribx x1e56ztr x1i64zmx x19h7ccj xu9j1y6 x7ep2pv