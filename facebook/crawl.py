
from facebook.type import types
from selenium.webdriver.common.by import By
from time import sleep
from mongo.collections import posts 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Crawl:
    def __init__(self,browser, page):
        self.page = page
        self.browser = browser

    def get(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(10)
        
        try:
            posts = self.browser.find_elements(By.XPATH, '//*[@aria-posinset]')
            print(len(posts))
            for post in posts:
                # with open('output.txt','a',encoding='utf-8') as file:
                #     file.write(post.text)
                #     file.write('\n----------------------------------------------\n')
                
                xem_them_buttons = post.find_elements(By.XPATH, types['btn-more'])
                for button in xem_them_buttons:
                    try:
                        button.click()
                        print(button.text)
                        sleep(1)
                    except:
                        pass
                self.getData(post)
        except:
            print(f"Không tìm thấy bài post nào trên page: {self.page['link']}")
            pass


    def getData(self, post):
        data = {
            'title': '',
        }
        try:
            # Lấy content
            content = WebDriverWait(post, 10).until(
                EC.presence_of_element_located((By.XPATH, types['content-post']))
            )
            
            texts = content.find_elements(By.XPATH, './div/div/span/div/div')
            for text in texts:
                data['title'] += text.text + ' '

        except Exception as e:
            print(f'Post. Error: {e}')

        posts.insert_one(data)