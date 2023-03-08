from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_validation_extended import Validator, Json, MinLen, MaxLen, File, Ext, MaxFileCount
from flask_jwt_extended import (
    get_jwt_identity, create_refresh_token, create_access_token, jwt_required
)
from app.api.response import response_200, bad_request, forbidden, no_content, conflict, unauthorized
from app.api.decorator import timer, login_required
from model.mysql.user import User
from MySQLdb import IntegrityError
from config import config
from datetime import timedelta
from config import Config
from model.mysql.board import Board
from controller.file_util import upload_to_s3
from uuid import uuid4
from . import api_v1 as api

@api.post('/board/post')
@timer
@login_required
@Validator(bad_request)
def create_post_api(
    title=Json(str, rules=[MinLen(1), MaxLen(20)]),
    nickname=Json(str, rules=[MinLen(1), MaxLen(20)]),
    category=Json(str, rules=[MinLen(1), MaxLen(20)]),
    content=Json(str, rules=[MinLen(1), MaxLen(1000)]),
    images=Json(str, optional=True)
):
    '''
    게시글 추가 API
    '''
    board_model = Board(current_app.db)
    model_res = board_model.insert_post({
        'user_id': g.user_id,
        'nickname': nickname,
        'category': category,
        'title': title,
        'content': content
    })
    # error 발생시
    if isinstance(model_res, IntegrityError):
        return conflict("Duplicate key or Foreign Key Constraint fail")
        
    # 게시글 추가 완료
    return response_200()

@api.post('/board/image')
@timer
@login_required
@Validator(bad_request)
def upload_img_api(
    img: File = File(
        rules=[
            Ext(['.png', '.jpg', '.jpeg', '.gif', '.heic']),
            MaxFileCount(1)
        ]
    )
):
    return response_200(
        upload_to_s3(
            s3=current_app.s3,
            files=img,
            type="post",
            object_id=f"{g.user_id}_{uuid4()}"
        )
    )
