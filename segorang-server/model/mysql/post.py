from .base import Model
from .utils import get_fields_data, set_quote

class Post(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'post_id', 'post_title','content',
            'view_num','category',
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
        keys = ['post_id', 'post_title', 'post_category', 'post_content',
                'post_view_num','post_created_at','post_updated_at',
                'post_user_id', 'post_board_id', 
                'board_title', 'user_nickname', 'user_name', 'user_major',
                'user_sj_id', 'post_img_path', 'like_cnt', 'is_like', 'is_deleted']
        # 게시물 정보를 얻어오는 쿼리
        query = f'SELECT post.id, post.title, post.category, post.content,\
                        post.view_num, post.created_at, post.updated_at,\
                        post.user_id, post.board_id, \
                        board.title, user.nickname, user.user_name, user.major,\
                        user.sj_id, post_image.img_path,\
                        (\
                            SELECT COUNT(*)\
                            FROM post_like\
                            WHERE post_id={post_id}\
                        ),\
                        post.is_deleted\
                  FROM post JOIN board \
                                ON post.board_id=board.id \
                            JOIN user \
                                ON post.user_id=user.id \
                            LEFT JOIN post_image \
                                ON post.id=post_image.post_id\
                  WHERE post.id={post_id};'
        self.cursor.execute(query)
        post_data = self.cursor.fetchone()

        if post_data is None or post_data[-1]:
            # 게시물이 없거나 / 삭제되었을 경우 -> None 반환
            return None
        # 좋아요를 눌렀는지 확인하는 쿼리
        post_data = list(post_data)
        query = f'SELECT * FROM post_like WHERE user_id={set_quote(user_id)}'
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res is None:
            post_data.append(False)
        else:
            post_data.append(True)
        
        return dict(zip(keys, post_data))

    def delete_post_by_postid(self, post_id:int):
        query = self.update_query.format(
            table_name=self.table_name,
            update_data='is_deleted = true',
            condition=f'WHERE id={post_id}'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()

    def update_post_by_postid(self, post_id:int, post_data:dict):
        query = self.update_query.format(
            table_name=self.table_name,
            update_data=', '.join(map(lambda x:x[0]+'='+set_quote(x[1]), list(post_data.items()))),
            condition=f'WHERE id={post_id}'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()