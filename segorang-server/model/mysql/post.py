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

    def get_post_by_postid(self, post_id:int, user_id):
        keys = ['post_title', 'board_title', 'writer', 
                'content', 'category', 'images', 'view_num', 
                'created_at', 'updated_at', 'like_num', 'is_like']
        # 게시물 정보를 얻어오는 쿼리
        query = f'SELECT post.title, board.title, user.nickname, \
                        post.content, post.category, post_image.img_path,\
                        post.view_cnt, post.created_at, post.updated_at, \
                        (\
                            SELECT COUNT(*)\
                            FROM post_image\
                            WHERE post_id={post_id}\
                        )\
                  FROM post JOIN board \
                                ON post.board_id=board.id \
                            JOIN user \
                                ON post.user_id=user.id \
                            LEFT JOIN post_image \
                                ON post.id=post_image.post_id\
                  WHERE post.id={post_id};'
        self.cursor.execute(query)
        post_data = list(self.cursor.fetchone())
        # 좋아요를 눌렀는지 확인하는 쿼리
        query = f'SELECT * FROM post_like WHERE user_id={set_quote(user_id)}'
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        
        if res is None:
            post_data.append(False)
        else:
            post_data.append(True)
        
        self.cursor.close()
        if post_data is None:
            return None
        else:
            return dict(zip(keys, post_data))