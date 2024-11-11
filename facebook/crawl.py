
from facebook.type import types
from selenium.webdriver.common.by import By
from time import sleep
from mongo.collections import posts as postCollections
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Crawl:
    def __init__(self,browser):
        self.browser = browser

    def get(self, page):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)

        link = f"{page['link']}/posts/"
        self.link = link
        self.page_id = page['_id']

        post_ids = []
        posts = self.browser.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
        print(f"*) //a[contains(@href, '{link}')]",len(posts))

        for post in posts:
            href = post.get_attribute('href')
            post_id = href.replace(link, '').split('?')[0]
            if post_id not in post_ids:
                post_ids.append(post_id)

        print(f"=> Ra được: {len(post_ids)}")
        self.checkPost(post_ids)
    
    def checkPost(self, post_ids):
        new_posts = [post_id for post_id in post_ids if postCollections.find_one({'_id': post_id}) is None]
        if new_posts:
            for post_id in new_posts:
                self.crawlPost(post_id)

    def crawlPost(self, post_id):
        data = {
            '_id': post_id,
            'page_id': self.page_id,
            'title': ''
        }
        self.browser.get(f"{self.link}{post_id}")
        sleep(5)

        modal = self.browser.find_element(By.XPATH,types['modal'])
        try:
            content = modal.find_element(By.XPATH,types['content'])
            data['title'] = content.text
        except:
            pass
            
        postCollections.insert_one(data)


    