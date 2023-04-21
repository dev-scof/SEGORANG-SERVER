from .base import Model
from .utils import get_fields_data, set_quote

class Comment(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'content', 'parent_comment_id',
            'created_at', 'updated_at'
        ]

    def insert_comment(self, comment_data):
        pass