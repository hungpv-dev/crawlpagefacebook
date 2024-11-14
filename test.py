import mysql.connector

connection = mysql.connector.connect(
    host='112.213.89.89', 
    database='asfyvn666bef_FB_Dev',
    user='asfyvn666bef_dev_hung',
    password='kpo{?{)#w9W7',
)

try:
    connection.is_connected()
    print('Kết nối thành công!')
except Exception as e:
    print(f"Kết nối thất bại: {e}")