
from facebook.type import types
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from mongo.collections import posts as postCollections
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Crawl:
    def __init__(self, browser, page):
        self.browser = browser
        self.page = page

    def get(self):
        # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # sleep(5)
        self.browser.execute_script("document.body.style.zoom='0.1';")
        sleep(5)

        pageLink = f"{self.page['link']}/posts/"
        self.postLink = pageLink

        actions = ActionChains(self.browser)
        links = self.browser.find_elements(By.CSS_SELECTOR, "a[href='#']")
        count = 0
        for link in links:
            try:
                actions.move_to_element(link).perform()
                count += 1
            except:
                pass
        print(f"{count}/{len(links)}")

        post_ids = []
        posts = self.browser.find_elements(By.XPATH, f"//a[contains(@href, '{pageLink}')]")
        for post in posts:
            href = post.get_attribute('href')
            post_id = href.replace(pageLink, '').split('?')[0]
            if post_id not in post_ids:
                post_ids.append(post_id)

        print(f"=> Ra được: {len(post_ids)}")
        self.checkPost(post_ids)
        sleep(2)
    
    def checkPost(self, post_ids):
        new_posts = [post_id for post_id in post_ids if postCollections.find_one({'post_id': post_id}) is None]
        if new_posts:
            for post_id in new_posts:
                sleep(5)
                self.crawlPost(post_id)

    def crawlPost(self, post_id):
        data = {
            'post_id': post_id,
            'page_id': self.page['_id'],
            'title': ''
        }
        self.browser.get(f"{self.postLink}{post_id}")
        sleep(5)

        try:
            # Chờ cho modal xuất hiện
            modal = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, types['modal']))
            )
            content = WebDriverWait(modal, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-ad-comet-preview="message"]'))
            )
            with open('output.txt','a',encoding='utf-8') as file:
                file.write('\n------\n')
                file.write(content.text)
            
            data['title'] = content.text
        except:
            print(f'Bài post: {post_id} page: {self.page["link"]} không có nội dung!')
            pass
            
        # postCollections.insert_one(data)


    