from .base import Model
from .utils import get_fields_data, set_quote

class Comment_Like(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'title',
            'created_at', 'updated_at'
        ]

    def insert_like(self, user_id, comment_id):
        query = self.insert_query.format(
            table_name = self.table_name,
            keys=f'user_id, comment_id',
            values=f'{set_quote(user_id)}, {comment_id}' 
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()
    
    def delete_like(self, user_id, comment_id):
        query = self.delete_query.format(
            table_name = self.table_name,
            condition = f'WHERE user_id={set_quote(user_id)}'
                        f' and comment_id={comment_id}'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            return e
        finally:
            self.cursor.close()
    
    def get_like_cnt(self, comment_id):
        query = self.select_query.format(
            property = "COUNT(*)",
            table_name = self.table_name,
            condition = f"WHERE comment_id = {comment_id}"
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]