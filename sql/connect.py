import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost', 
        database='asfyvn666bef_fb_dev',
        user='root',
        password=''
    )
    
    if connection.is_connected():
        print("Kết nối thành công đến MySQL!")
    else:
        print("Kết nối thất bại đến MySQL.")

except Exception as e:
    print(f"Kết nối thất bại: {e}")
