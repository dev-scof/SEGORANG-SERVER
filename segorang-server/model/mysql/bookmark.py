from .base import Model
from .utils import get_fields_data, set_quote

class Bookmark(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'user_id', 'post_id'
            'created_at', 'updated_at'
        ]

    def insert_bookmark(self, data:dict):
        keys, values = get_fields_data(data)
        query = self.insert_query.format(
            table_name=self.table_name,
            keys=', '.join(map(str, keys)),
            values=', '.join(map(set_quote ,values))
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
    
    def delete_bookmark(self, data:dict):
        query = self.delete_query.format(
            table_name=self.table_name,
            condition='WHERE '+' AND '.join(map(lambda x:x[0]+'='+set_quote(x[1]), data.items()))
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()

    def get_bookmark(self, condition:dict):
        query = self.select_query.format(
            table_name=f"bookmark LEFT JOIN post ON bookmark.post_id=post.id",
            property=f"post.id, post.title, post.view_cnt, post.category",
            condition="WHERE "+" AND ".join(map(lambda x:x[0]+'='+set_quote(x[1]), condition.items()))
        )
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        if data is None:
            return None
        else:
            keys = ['id', 'title', 'view_num', 'category']
            return list(map(lambda x:dict(zip(keys, x)),data))