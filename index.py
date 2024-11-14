from selenium import webdriver
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from facebook.crawl import Crawl
from sql.pages import Page

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service('chromedriver.exe') 
browser = webdriver.Chrome(service=service,options=chrome_options)

browser.get("https://facebook.com")

# Đọc cookie từ file
with open('cookie.json','r') as file:
    cookies = json.load(file)

# Thêm từng cookie vào trình duyệt
for cookie in cookies:
    browser.add_cookie(cookie)

browser.get('https://facebook.com')

sleep(1)
page_instance = Page()
listPages = page_instance.all()
for page in listPages:
    link = page['link']
    browser.get(link)
    crawl = Crawl(browser,page)
    crawl.get()
    sleep(2)

browser.close() # Đóng
