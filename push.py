from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from facebook.push import Push
import json
from sql.posts import Post

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
browser.get('https://www.facebook.com/groups/1251316042850404')
sleep(1)

post_instance = Post()
record = post_instance.random_record()

push_instance = Push(browser)
push_instance.up(record)

browser.close() # Đóng