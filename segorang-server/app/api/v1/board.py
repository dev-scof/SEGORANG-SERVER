from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_validation_extended import Validator, Json, MinLen, MaxLen, File, Ext, MaxFileCount, Query, Route
from flask_jwt_extended import (
    get_jwt_identity, create_refresh_token, create_access_token, jwt_required
)
from app.api.response import response_200, bad_request, forbidden, no_content, conflict, unauthorized
from app.api.decorator import timer, login_required, admin_required
from model.mysql.user import User
from MySQLdb import IntegrityError
from config import config
from datetime import timedelta
from config import Config
from . import api_v1 as api
from model.mysql.board import Board
from controller.file_util import upload_to_s3
from uuid import uuid4

@api.post('/board')
@timer
@admin_required
@Validator(bad_request)
def create_board_api(
    title=Json(str, rules=[MinLen(1), MaxLen(20)])
):
    '''
    게시판 추가 API
    '''
    board_model = Board(current_app.db)
    model_res = board_model.insert_board(title)
    # 중복 error 발생시
    if isinstance(model_res, IntegrityError):
        return conflict("Duplicate key or Foreign Key Constraint fail")
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())

    # 게시판 추가 완료
    return response_200()

@api.delete('/board')
@timer
@admin_required
@Validator(bad_request)
def delete_board_api(
    title=Json(str, rules=[MinLen(1), MaxLen(20)])
):
    '''
    게시판 삭제 API
    '''
    board_model = Board(current_app.db)
    model_res = board_model.delete_board(title)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    
    return no_content

@api.patch('/board')
@timer
@admin_required
@Validator(bad_request)
def update_board_api(
    pre_title=Json(str, rules=[MinLen(1), MaxLen(20)]),
    nex_title=Json(str, rules=[MinLen(1), MaxLen(20)])
):
    '''
    게시판 변경 API
    '''
    board_model = Board(current_app.db)
    model_res = board_model.update_board(pre_title, nex_title)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    
    return no_content

@api.get('/board')
@timer
@admin_required
@Validator(bad_request)
def get_boards_api():
    '''
    모든 게시판 반환
    '''
    board_model = Board(current_app.db)
    model_res = board_model.get_board_all()

    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())

    return response_200(
        model_res
    )

@api.get('/board/<board_title>')
@timer
@login_required
@Validator(bad_request)
def get_postlist_api(
    board_title=Route(str),
    page=Query(int),
    limit=Query(int)
):
    '''
    게시판 목록 반환
    '''
    board_model = Board(current_app.db)
    if board_model.get_board_id_by_title(
        board_title) is None:
        return bad_request(f"{board_title} is not exist")
    model_res = board_model.get_post_list(board_title)

    return response_200(model_res)
    # model_res = board_model.get_post_list()
    # print(page, limit)