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
    
    def get_comment_by_postid(self, post_id):
        query = f"WITH RECURSIVE CTE AS (\
                    SELECT id, IF(is_deleted=false, content, '삭제된 댓글입니다.') content, \
                        created_at, parent_comment_id, user_id, CAST(id AS CHAR(255)) AS path\
                    FROM comment\
                    WHERE parent_comment_id IS NULL AND post_id={post_id}\
                    \
                    UNION ALL\
                    \
                    SELECT c.id, IF(c.is_deleted=false, c.content, '삭제된 댓글입니다.') content, \
                        c.created_at, c.parent_comment_id, c.user_id, CONCAT(cte.path, '-', c.id)\
                    FROM comment c\
                		JOIN CTE cte ON c.parent_comment_id = cte.id\
                	WHERE c.post_id={post_id}\
                )\
                SELECT CTE.id, CTE.content, user.nickname, CTE.parent_comment_id, CTE.created_at\
                FROM CTE JOIN user ON CTE.user_id=user.id\
                ORDER BY CAST(REPLACE(path, '-', '+') AS UNSIGNED), created_at;"
        keys = ['id', 'content', 'nickname', 
                'parent_comment_id', 'created_at']
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        
        return list(map(lambda x:dict(zip(keys, x)), data))

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