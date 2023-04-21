from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_validation_extended import Validator, Json, MinLen, MaxLen, File, Ext, MaxFileCount, Route, Min
from flask_jwt_extended import (
    get_jwt_identity, create_refresh_token, create_access_token, jwt_required
)
from app.api.response import response_200, bad_request, forbidden, no_content, conflict, unauthorized, created
from app.api.decorator import timer, login_required, admin_required
from model.mysql.user import User
from MySQLdb import IntegrityError
from config import config
from datetime import timedelta
from config import Config
from . import api_v1 as api
from model.mysql.comment import Comment
from model.mysql.post import Post
from model.mysql.post_image import Post_Image
from model.mysql.post_like import Post_Like
from controller.file_util import upload_to_s3
from controller.util import remove_none_value
from uuid import uuid4



@api.post('/comment/post')
@timer
@login_required
@Validator(bad_request)
def comment_insert_api(
    content=Json(str, rules=[MinLen(1), MaxLen(300)]),
    parent_comment_id=Json(int, Min(0), default=0),
    post_id=Json(int)
):
    '''
    댓글 추가
    '''
    comment_model = Comment(current_app.db)
    comment_data = {
        'content':content,
        'parent_comment_id':parent_comment_id,
        'user_id':g.user_id,
        'post_id':post_id
    }
    print(comment_data)
    return created