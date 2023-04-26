from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_validation_extended import Validator, Json, MinLen, MaxLen, File, Ext, MaxFileCount, Query, Route, Min
from flask_jwt_extended import (
    get_jwt_identity, create_refresh_token, create_access_token, jwt_required
)
from app.api.response import response_200, bad_request, forbidden, no_content, conflict, unauthorized
from app.api.decorator import timer, login_required, admin_required
from model.mysql.user import User
from model.mysql.bookmark import Bookmark
from MySQLdb import IntegrityError
from config import config
from datetime import timedelta
from config import Config
from . import api_v1 as api
from model.mysql.board import Board
from controller.file_util import upload_to_s3
from uuid import uuid4

@api.post('/bookmark/<int:post_id>')
@timer
@login_required
@Validator(bad_request)
def bookmark_insert_api(
    post_id=Route(int, rules=Min(0))
):
    '''
    북마크 추가
    '''
    model = Bookmark(current_app.db)
    model_res = model.insert_bookmark({
        'user_id':g.user_id,
        'post_id':post_id
    })
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    return no_content

@api.delete('/bookmark/<int:post_id>')
@timer
@login_required
@Validator(bad_request)
def bookmark_delete_api(
    post_id=Route(int, rules=Min(0))
):
    '''
    북마크 추가
    '''
    model = Bookmark(current_app.db)
    model_res = model.delete_bookmark({
        'user_id':g.user_id,
        'post_id':post_id
    })
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    return no_content

@api.get('/bookmark')
@timer
@login_required
@Validator(bad_request)
def bookmark_get_api():
    '''
    사용자에 대한 북마크 가져오기
    '''
    model = Bookmark(current_app.db)
    model_res = model.get_bookmark({
        'post.user_id':g.user_id
    })
    return response_200(model_res)