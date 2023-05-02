from .base import Model
from .utils import get_fields_data, set_quote

class User_Image(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'img_path',
            'created_at', 'updated_at', 'user_id'
        ]

    def insert_user_image(self, img_data:dict):
        keys, values = get_fields_data(img_data)
        query = self.insert_query.format(
            table_name=self.table_name,
            keys=', '.join(map(str, keys)),
            values=', '.join(map(set_quote, values)))
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()