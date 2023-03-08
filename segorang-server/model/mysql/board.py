from .base import Model
from .utils import get_fields_data, set_quote

class Board(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'user_id', 'nickname',
            'category', 'title', 'content',
            'crated_at', 'updated_at'
        ]

    def insert_post(self, post_data:dict):
        keys, values = get_fields_data(post_data)
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