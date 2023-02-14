from .base import Model
from .utils import get_fields_data, set_quote
class User(Model):

    VERSION = 1

    def insert_user(self, user_data:dict):
        keys, values = get_fields_data(user_data)
        query = self.insert_query.format(
            table_name=self.table_name,
            keys=', '.join(map(str, keys)),
            values=', '.join(map(set_quote, values)))
        self.cursor.execute(query)
        self.conn.commit()
        