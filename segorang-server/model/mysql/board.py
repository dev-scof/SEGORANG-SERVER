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