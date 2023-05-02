from .base import Model
from .utils import get_fields_data, set_quote

class Post_Image(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'title','content',
            'view_cnt','category',
            'created_at', 'updated_at',
            'user_id', 'board_id']

    def insert_post_image(self, post_data:dict):
        keys, values = get_fields_data(post_data)
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
    
    def update_post_image(self, img_path, post_id):
        query = self.update_query.format(
            table_name=self.table_name,
            update_data=f'img_path={set_quote(img_path)}',
            condition=f'WHERE id={post_id}'
        )
        print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()