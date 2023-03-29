from .base import Model
from .utils import get_fields_data, set_quote

class Post(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'sj_id', 'nickname', 
            'pw', 'name', 'major', 
            'is_admin', 'sejong_auth', 
            'created_at', 'updated_at', 'version']

    