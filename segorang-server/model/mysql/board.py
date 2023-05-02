from .base import Model
from .utils import get_fields_data, set_quote

class Board(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'title',
            'created_at', 'updated_at'
        ]

    def insert_board(self, title):
        query = self.insert_query.format(
            table_name=self.table_name,
            keys='title',
            values=set_quote(title)
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()
    
    def delete_board(self, title):
        """
        title을 통해 삭제한다.
        """
        query = self.delete_query.format(
            table_name=self.table_name,
            condition=f'WHERE title={set_quote(title)}'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()
    
    def update_board(self, pre_title, nex_title):
        """
        title을 변경한다.
        """
        query = self.update_query.format(
            table_name = self.table_name,
            update_data = f'title={set_quote(nex_title)}',
            condition = f"WHERE title={set_quote(pre_title)}"
        )
        try:
            if self.cursor.execute(query) == 0:
                raise Exception("Data has not been changed")
            self.conn.commit()

            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()

    def get_board_all(self):
        """
        모든 게시판 반환
        """
        query = self.select_query.format(
            table_name = self.table_name,
            property = '*',
            condition=''
        )
        self.cursor.execute(query)
        board_data = self.cursor.fetchall()
        self.cursor.close()
        if board_data is None:
            return None
        else:            
            return list(map(lambda x:dict(zip(self.property, x)),board_data))
    
    def get_board_id_by_title(self, title):
        '''
        제목에 해당하는 게시판 id 반환
        '''
        query = self.select_query.format(
            table_name = self.table_name,
            property = 'id',
            condition=f'WHERE title={set_quote(title)}'
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]
    def get_post_count(self, board_title):
        '''board_title에 해당하는 모든 post 반환'''
        query = self.select_query.format(
            property="COUNT(*)",
            table_name="post JOIN board ON post.board_id=board.id",
            condition=f"WHERE board.title = {set_quote(board_title)}"
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0]
    def get_post_list(self, board_title, page:int, limit:int):
        '''
        제목에 해당하는 게시물 반환하기
        '''
        query = (
            # select
            f"SELECT post.id, post.title, post.category,"
            f" post.view_cnt, post.created_at, post.updated_at,"
            f" post_image.img_path,"
            f" user.nickname,"
            f" COUNT(post_like.post_id),"
            f" COUNT(comment.post_id)"
            # from
            f" FROM post JOIN board ON post.board_id = board.id"
            f" LEFT JOIN user ON user.id = post.user_id"
            f" LEFT JOIN post_image ON post.id = post_image.post_id"
            f" LEFT JOIN post_like ON post.id = post_like.post_id"
            f" LEFT JOIN comment ON post.id = comment.post_id"
            # where
            f" WHERE board.title = {set_quote(board_title)}"
            # group by
            f" GROUP BY post.id, post.title, post.category, post.view_cnt, post.created_at, post.updated_at, post_image.img_path, user.nickname"
            # order by
            f" ORDER BY post.created_at"
            # limit
            f" LIMIT {limit}"
            # offset
            f" OFFSET {page*limit}"
        )
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result is None:
            return None
        else:
            keys = ['post_id', 'post_title', 'category',
                    'view_cnt', 'created_at', 'updated_at',
                    'image', 'writer', 'like_num', 'comment_num']
            return list(map(lambda x:dict(zip(keys, x)),result))
        
'''
SELECT post.id, board.title, user.nickname, post.category, post_image.img_path, post.created_at, post.updated_at, post.view_cnt, COUNT(comment.id) 
FROM post 
    JOIN board ON board.id = post.board_id 
    JOIN user ON user.id = post.user_id 
    JOIN post_image ON post.id = post_image.post_id 
    LEFT JOIN comment ON post.id = comment.post_id 
GROUP BY post.id;

'''
