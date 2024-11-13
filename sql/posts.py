from sql.connect import connection
import pandas as pd
from sql.model import Model

class Post(Model):
    def __init__(self):
        super().__init__()
        self.table = 'posts'
        self.filllabel = [
            'post_id',
            'page_id',
            'content',
            'media',
            'like',
            'comment',
            'share',
            'up',
            'user_id',
            'page_up_id',
            'created_at'
        ]

    def insert_from_xlsx(self, file_path):
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            if row.iloc[1]:
                self.cursor.execute(
                    f"INSERT INTO {self.table} (link, type) VALUES (%s, %s)",
                    (row.iloc[1], row.iloc[2])
                )
        connection.commit()