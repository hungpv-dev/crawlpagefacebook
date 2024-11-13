from sql.connect import connection

class Model:
    def __init__(self):
        self.cursor = connection.cursor()

    def all(self):
        return self.fetch_all(f"SELECT * FROM {self.table}")
    
    def get_none_post_ids(self, ids):
        nonexistent_ids = []
        for id in ids:
            self.cursor.execute(f"SELECT * FROM {self.table} WHERE post_id = %s", (id,))
            if not self.cursor.fetchone():
                nonexistent_ids.append(id)
        return nonexistent_ids
    
    def fetch_all(self, query):
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def insert(self, data):
        table = self.table
        params = []
        key = ''
        val = ''
        for i, fill in enumerate(self.filllabel):
            if fill in data and data[fill]:
                key += f"`{fill}`" 
                val += '%s'
                params.append(data[fill])
                if (i + 1) != len(self.filllabel): 
                    key += ',' 
                    val += ','

        # Kiểm tra xem key và val có rỗng không
        if not key or not val:
            print("Không có cột hoặc giá trị nào để chèn vào cơ sở dữ liệu.")
            return

        sql = f"INSERT INTO {table} ({key}) VALUES ({val})"
        self.cursor.execute(sql, tuple(params))
        connection.commit()
        
        # Trả về id của bản ghi vừa thêm
        self.cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = self.cursor.fetchone()[0]
        return last_id
        

    def truncate(self):
        sql = f'TRUNCATE TABLE {self.table}'
        self.cursor.execute(sql)
