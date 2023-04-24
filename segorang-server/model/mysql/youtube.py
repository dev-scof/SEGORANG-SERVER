from .base import Model
from .utils import get_fields_data, set_quote

class Youtube(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'thumb_nail', 'title',
            'link', 'created_at', 'updated_at'
        ]
    
    def insert_youtube(self, data:dict):
        keys, values = get_fields_data(data)
        query = self.insert_query.format(
            table_name=self.table_name,
            keys=', '.join(map(str, keys)),
            values=', '.join(map(set_quote, values))
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()

    def get_youtube(self, page:int, limit:int):
        keys = ['thumb_nail', 'title', 'link']            
        query = self.select_query.format(
            table_name=self.table_name,
            property=', '.join(keys),
            condition=f'ORDER BY created_at'
                        f' LIMIT {limit}'
                        f" OFFSET {page*limit}"
        )
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        if data is None:
            return None
        else:
            return list(map(lambda x:dict(zip(keys, x)),data))