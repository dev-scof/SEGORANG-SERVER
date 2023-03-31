from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_validation_extended import Validator, Json, MinLen, MaxLen, File, Ext, MaxFileCount, Route
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
from model.mysql.board import Board
from model.mysql.post import Post
from model.mysql.post_image import Post_Image
from model.mysql.utils import none_to_null
from controller.file_util import upload_to_s3
from controller.util import remove_none_value
from uuid import uuid4
@api.post('/post')
@timer
@login_required
@Validator(bad_request)
def create_post_api(
    post_title=Json(str, rules=[MinLen(1), MaxLen(100)]),
	board_title=Json(str, rules=[MinLen(1), MaxLen(10)]),
	category=Json(str, rules=[MinLen(1), MaxLen(10)], optional=True),
	content=Json(str, rules=[MinLen(1), MaxLen(2000)]),
	images=Json(str, rules=[MaxLen(200)],optional=True)
):
    '''
    게시물 추가
    '''
    board_model = Board(current_app.db)
    board_id = board_model.get_board_id_by_title(board_title)
    if board_id is None:
        return bad_request(f"{board_title} is not exist board")
    post_model = Post(current_app.db)
    # post에 추가
    model_res = post_model.insert_post({
        'title':post_title,
        'content':content,
        'category': none_to_null(category),
        'user_id':g.user_id,
        'board_id':board_id[0]
    })
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    
    # TODO: image가 있으면 post_image에 추가해야한다.
    if images is not None:
        post_img_model = Post_Image(current_app.db)
        post_img_model.insert_post_image({
            'img_path':images,
            'post_id':model_res
        })
    return created

@api.get('/post/<post_id>')
@timer
@login_required
@Validator(bad_request)
def get_post_api(
    post_id: int = Route(int)
):
    post_model = Post(current_app.db)
    model_res = post_model.get_post_by_postid(post_id)
    return response_200(model_res)