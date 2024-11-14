from sql.connect import connection

class Model:
    def __init__(self):
        self.cursor = connection.cursor()
        self.where_clauses = []
        self.order_by_clause = ''
        self.offset_clause = ''
        self.limit_clause = ''

    def where(self, where_clause=None):
        if where_clause:
            self.where_clauses.append(where_clause)
        return self

    def orderBy(self, order_by_clause=None):
        if order_by_clause:
            self.order_by_clause = order_by_clause
        return self

    def offset(self, offset_clause=None):
        if offset_clause is not None:
            self.offset_clause = f" OFFSET {offset_clause}"
        return self

    def limit(self, limit_clause=None):
        if limit_clause is not None:
            self.limit_clause = f" LIMIT {limit_clause}"
        return self

    def all(self):
        query = f"SELECT * FROM {self.table}"
        if self.where_clauses:
            query += " WHERE " + " AND ".join(self.where_clauses)
        if self.order_by_clause:
            query += f" ORDER BY {self.order_by_clause}"
        if self.offset_clause:
            query += self.offset_clause
        if self.limit_clause:
            query += self.limit_clause
        return self.fetch_all(query)
    
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

    def update(self, data, condition):
        table = self.table
        set_clause = ''
        params = []
        for i, fill in enumerate(self.filllabel):
            if fill in data and data[fill]:
                set_clause += f"`{fill}` = %s"
                params.append(data[fill])
                if (i + 1) != len(self.filllabel):
                    set_clause += ', '

        # Kiểm tra xem set_clause có rỗng không
        if not set_clause:
            print("Không có cột hoặc giá trị nào để cập nhật trong cơ sở dữ liệu.")
            return

        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.cursor.execute(sql, tuple(params))
        connection.commit()

    def truncate(self):
        sql = f'TRUNCATE TABLE {self.table}'
        self.cursor.execute(sql)
