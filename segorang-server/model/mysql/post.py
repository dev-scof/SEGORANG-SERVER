from .base import Model
from .utils import get_fields_data, set_quote

class Post(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'post_id', 'post_title','content',
            'view_cnt','category',
            'created_at', 'updated_at',
            'writer', 'board_id']

    def insert_post(self, post_data:dict):
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

    def get_post_by_postid(self, post_id:int):
        query = f'SELECT post.*, board.title \
                FROM post JOIN board ON post.board_id=board.id\
                where post.id={post_id};'
        self.cursor.execute(query)
        post_data = self.cursor.fetchone()
        cur_property = self.property + ['board_title']
        print(cur_property)
        print(post_data)
        self.cursor.close()
        if post_data is None:
            return None
        else:
            return dict(zip(cur_property, post_data))