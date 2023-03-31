from .base import Model
from .utils import get_fields_data, set_quote

class User_Image(Model):

    VERSION = 1

    @property
    def property(self):
        return [
            'id', 'title',
            'created_at', 'updated_at'
        ]

    