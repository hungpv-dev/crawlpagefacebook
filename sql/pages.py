from sql.connect import connection
import pandas as pd
from sql.model import Model

class Page(Model):
    def __init__(self):
        super().__init__()
        self.table = 'pages'

    def insert_from_xlsx(self, file_path):
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            if row.iloc[1]:
                self.cursor.execute(
                    f"INSERT INTO {self.table} (link, type) VALUES (%s, %s)",
                    (row.iloc[1], row.iloc[2])
                )
        connection.commit()