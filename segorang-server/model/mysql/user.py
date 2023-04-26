from .base import Model
from .utils import get_fields_data, set_quote

class User(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'sj_id', 'nickname',
            'user_name', 'pw', 'major', 
            'is_admin', 'sejong_auth', 
            'created_at', 'updated_at', 'version']

    def insert_user(self, user_data:dict):
        keys, values = get_fields_data(user_data)
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

    def update_user_by_id(self, data:dict, id):
        query = self.update_query.format(
            table_name=self.table_name,
            update_data=', '.join(map(lambda x:x[0]+'='+set_quote(x[1]), list(data.items()))),
            condition=f"WHERE id={set_quote(id)}"
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

    def get_user_by_single_property(self, property, input_property):
        """한 속성에 해당하는 속성값을 통해 사용자를 찾는다"""
        query = self.select_query.format(
            property="*",
            table_name=self.table_name,
            condition=f"WHERE {property}={set_quote(input_property)}"
        )
        self.cursor.execute(query)
        user_data = self.cursor.fetchone()
        self.cursor.close()
        if user_data is None:
            return None
        else:
            return dict(zip(self.property, user_data))
    
    def get_user_by_elem(self, property:list, elem:dict):
        query = self.select_query.format(
            property=', '.join(map(str, property)),
            table_name=self.table_name,
            condition="WHERE "+'AND'.join(map(lambda x:x[0]+'='+set_quote(x[1]), elem.items()))
        )
        self.cursor.execute(query)
        user_data = self.cursor.fetchone()
        self.cursor.close()
        if user_data is None:
            return None
        else:
            if property[0]=='*':
                return dict(zip(self.property, user_data))    
            return dict(zip(property, user_data))

    def delete_user_by_id(self, id:str):
        """id에 해당하는 사용자를 삭제한다."""
        query = self.delete_query.format(
            table_name=self.table_name,
            condition=f'WHERE id="{id}"'
        )
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e
        finally:
            self.cursor.close()

