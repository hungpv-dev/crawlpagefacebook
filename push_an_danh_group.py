# Import các thư viện cần thiết
from selenium import webdriver  # Thư viện điều khiển trình duyệt
from selenium.webdriver.chrome.service import Service  # Quản lý dịch vụ cho Chrome
from time import sleep  # Tạm dừng code trong một khoảng thời gian
from facebook.push_an_danh_group import Push  # Lớp Push cho phép tự động đăng bài vào group
import json  # Thư viện xử lý dữ liệu JSON
from sql.posts import Post  # Lớp Post để lấy bài viết từ cơ sở dữ liệu

# Tạo đối tượng dịch vụ cho Chrome và khởi động trình duyệt
service = Service('chromedriver.exe')
browser = webdriver.Chrome(service=service)

# Điều hướng đến trang Facebook
browser.get("https://facebook.com")

# Đọc cookie từ file JSON để đăng nhập
with open('cookie.json', 'r') as file:
    cookies = json.load(file)

# Thêm từng cookie vào trình duyệt để duy trì phiên đăng nhập
for cookie in cookies:
    browser.add_cookie(cookie)

# Điều hướng lại trang Facebook (sau khi thêm cookie) để đảm bảo đã đăng nhập thành công
browser.get('https://facebook.com')
sleep(1)  # Đợi một giây để trang tải hoàn toàn

# Điều hướng đến group Facebook cụ thể bằng URL của group
browser.get('https://www.facebook.com/groups/1251316042850404')
sleep(1)  # Đợi một giây để group tải

# Tạo một instance (đối tượng) của lớp Post và lấy một bài viết ngẫu nhiên từ cơ sở dữ liệu
post_instance = Post()
record = post_instance.random_record()

# Khởi tạo đối tượng Push để đăng bài vào group
push_instance = Push(browser)

# Gọi phương thức anonymous_post để chọn chế độ "đăng ẩn danh" trước khi đăng
push_instance.anonymous_post()

# Gọi phương thức up để đăng bài với nội dung lấy từ record
push_instance.up(record)

# Đóng trình duyệt sau khi hoàn thành
browser.close()
