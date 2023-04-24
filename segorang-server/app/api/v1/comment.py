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
from model.mysql.comment_like import Comment_Like
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
    parent_comment_id=Json(int, rules=[Min(0)], optional=True),
    post_id=Json(int)
):
    '''
    댓글 추가
    '''
    comment_model = Comment(current_app.db)
    comment_data = {
        'content':content,
        'user_id':g.user_id,
        'post_id':post_id
    }
    if parent_comment_id:
        comment_data['parent_comment_id'] = parent_comment_id
    model_res = comment_model.insert_comment(comment_data)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    return created

@api.delete('/comment/<int:comment_id>')
@timer
@login_required
@Validator(bad_request)
def comment_delete_api(
    comment_id=Route(int, rules=Min(0))
):
    '''
    댓글 삭제 API
    '''
    comment_model = Comment(current_app.db)
    model_res = comment_model.get_comment_by_id(['user_id'], comment_id)
    # 다른 사람이 댓글을 삭제하는 경우
    if model_res['user_id'] != g.user_id:
        return unauthorized('잘못된 접근입니다.')
    model_res = comment_model.delete_comment_by_id(comment_id)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    return no_content

@api.patch('/comment/<int:comment_id>')
@timer
@login_required
@Validator(bad_request)
def comment_patch_api(
    comment_id=Route(int, rules=Min(0)),
    content=Json(str, rules=[MinLen(1), MaxLen(300)])
):
    '''
    댓글 수정 API
    '''
    comment_model = Comment(current_app.db)
    model_res = comment_model.get_comment_by_id(['user_id'], comment_id)
    # 다른 사람이 댓글을 삭제하는 경우
    if model_res['user_id'] != g.user_id:
        return unauthorized('잘못된 접근입니다.')
    model_res = comment_model.update_content_by_id(comment_id, content)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    return no_content

@api.get('/comment/post/<int:post_id>')
@timer
@login_required
@Validator(bad_request)
def comment_get_api(
    post_id=Route(int, rules=Min(0))
):
    '''
    댓글 반환 API
    '''
    comment_model = Comment(current_app.db)
    model_res = comment_model.get_comment_by_postid(post_id)
    return response_200(model_res)

@api.post('/comment/like/<int:comment_id>')
@timer
@login_required
@Validator(bad_request)
def comment_like_insert_api(
    comment_id=Route(int, rules=Min(0))
):
    '''
    댓글 좋아요 생성 API
    '''
    model=Comment_Like(current_app.db)
    model_res = model.insert_like(g.user_id, comment_id)

    if isinstance(model_res, Exception):
        return conflict(model_res.__str__())
    else:
        return response_200()


@api.delete('/comment/like/<int:comment_id>')
@timer
@login_required
@Validator(bad_request)
def comment_like_delete_api(
    comment_id=Route(int, rules=Min(0))
):
    """ 댓글 좋아요 삭제 API """
    model = Comment_Like(current_app.db)
    model_res = model.delete_like(g.user_id, comment_id)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    else:
        return no_content

@api.get('/comment/like/<int:comment_id>')
@timer
@login_required
@Validator(bad_request)
def comment_like_cnt_get_api(
    comment_id=Route(int, rules=Min(0))
):
    """ 게시물 좋아요 수 반환 API"""
    model = Comment_Like(current_app.db)
    model_res = model.get_like_cnt(comment_id)
    return response_200(model_res)