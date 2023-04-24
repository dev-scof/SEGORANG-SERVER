from .base import Model
from .utils import get_fields_data, set_quote

class Comment(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'content', 'parent_comment_id',
            'user_id', 'post_id', 'created_at',
            'updated_at'
        ]

    def insert_comment(self, comment_data):
        keys, values = get_fields_data(comment_data)
        query = self.insert_query.format(
            table_name=self.table_name,
            keys=', '.join(map(str, keys)),
            values=', '.join(map(set_quote, values))
        )
        try:
            self.cursor.execute(query)
            inserted_id = self.conn.insert_id()
            self.conn.commit()
            return inserted_id
        except Exception as e:
            return e
        finally:
            self.cursor.close()
    
    def get_comment_by_id(self, property:list, id):
        query = self.select_query.format(
            table_name=self.table_name,
            property=', '.join(map(str, property)),
            condition=f"WHERE id={id}"
        )
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if data is None:
            return None
        else:
            keys=property
            if keys[0]=='*':
                keys=[
                    'id', 'content','created_at', 
                    'updated_at', 'parent_comment_id', 
                    'user_id', 'post_id', 'is_deleted']
            return dict(zip(keys, data))
    
    def delete_comment_by_id(self, id):
        query = self.update_query.format(
            table_name=self.table_name,
            update_data='is_deleted = true',
            condition=f'WHERE id={id}'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()

    def update_content_by_id(self, id, update_content):
        query = self.update_query.format(
            table_name=self.table_name,
            update_data=f'content = {set_quote(update_content)}',
            condition=f'WHERE id={id}'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()