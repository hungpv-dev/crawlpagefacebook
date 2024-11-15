# Import các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from facebook.type import push_an_danh_group  # Tệp chứa XPATH các phần tử trên Facebook
import json  # Dùng để xử lý chuỗi JSON
import pyautogui  # Thư viện hỗ trợ thao tác bàn phím và chuột

# Định nghĩa lớp Push để thực hiện thao tác đăng bài trên Facebook
class Push:
    def __init__(self, browser):
        self.browser = browser  # Trình duyệt sẽ được truyền vào khi khởi tạo lớp

    # Phương thức để chọn chế độ đăng bài ẩn danh
    def anonymous_post(self):
        try:
            # Tìm và nhấp vào nút đăng bài ẩn danh
            anonymous_button = self.browser.find_element(By.XPATH, push_an_danh_group['anonymous_post'])
            anonymous_button.click()  # Nhấp vào nút
            sleep(1)  # Tạm dừng 1 giây để đợi hành động hoàn tất

            # Tìm và nhấp vào nút xác nhận đăng ẩn danh
            create_anonymous = self.browser.find_element(By.XPATH, push_an_danh_group['create_anonymous_post'])
            create_anonymous.click()  # Nhấp vào nút
            sleep(1)  # Tạm dừng 1 giây để hành động hoàn tất

        # Xử lý ngoại lệ nếu có lỗi xảy ra trong quá trình chọn chế độ ẩn danh
        except Exception as e:
            print(f'Lỗi khi chọn đăng ẩn danh: {e}')

    # Phương thức để đăng bài viết
    def up(self, post):
        try:
            # Tìm và nhấp vào nút để tạo bài viết mới
            createPost = self.browser.find_element(By.XPATH, push_an_danh_group['createPost'])
            createPost.click()  # Nhấp vào nút tạo bài viết
            sleep(1)  # Tạm dừng 1 giây để đợi khung tạo bài viết mở ra

            # Lấy phần tử đang hoạt động (ô nhập nội dung bài viết)
            input_element = self.browser.switch_to.active_element
            # Nhập nội dung từ `post['content']` vào ô nhập liệu
            input_element.send_keys(post['content'])

            # Giải mã chuỗi JSON `post['media']` để lấy danh sách ảnh
            media = json.loads(post['media'])
            images = media['images']  # Danh sách đường dẫn của ảnh

            # Lặp qua danh sách ảnh và thực hiện tải ảnh lên
            for src in images:
                self.browser.execute_script("window.open('');")  # Mở một tab mới
                self.browser.switch_to.window(self.browser.window_handles[1])  # Chuyển sang tab mới
                self.browser.get(src)  # Truy cập vào đường dẫn ảnh
                sleep(1)  # Tạm dừng 1 giây để ảnh tải xong

                # Sao chép ảnh vào clipboard
                pyautogui.hotkey('ctrl', 'c')
                sleep(0.5)  # Tạm dừng 0.5 giây để sao chép hoàn tất

                # Đóng tab hiện tại sau khi sao chép ảnh
                pyautogui.hotkey('ctrl', 'w')
                self.browser.switch_to.window(self.browser.window_handles[0])  # Quay lại tab chính
                sleep(1)  # Tạm dừng 1 giây để đảm bảo ảnh được sao chép vào clipboard

                # Dán ảnh vào ô nhập liệu của bài viết
                input_element.send_keys(Keys.CONTROL, 'v')
                sleep(1)  # Tạm dừng 1 giây để ảnh được dán vào

            # Gọi phương thức `anonymous_post` để chọn chế độ đăng ẩn danh
            self.anonymous_post()
            sleep(5)  # Tạm dừng 5 giây để chờ chế độ ẩn danh được kích hoạt

            # Tìm nút "Đăng bài" và cuộn màn hình đến nút này
            submit_button = self.browser.find_element(By.XPATH, push_an_danh_group['submit_button'])
            self.browser.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            sleep(1)  # Tạm dừng 1 giây để nút hiện trong tầm nhìn

            # Nhấp vào nút "Đăng bài" để hoàn tất đăng bài
            self.browser.execute_script("arguments[0].click();", submit_button)
            sleep(1)  # Tạm dừng 1 giây để chờ bài viết được đăng

        # Xử lý ngoại lệ nếu có lỗi xảy ra trong quá trình đăng bài
        except Exception as e:
            print(f'Lỗi khi đăng bài viết: {e}')
