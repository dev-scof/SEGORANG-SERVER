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
from model.mysql.post_like import Post_Like
from controller.file_util import upload_to_s3
from controller.util import remove_none_value
from uuid import uuid4
@api.post('/post')
@timer
@login_required
@Validator(bad_request)
def post_insert_api(
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
    post_data = {
        'title':post_title,
        'content':content,
        'user_id':g.user_id,
        'board_id':board_id
    }
    # category가 None이 아니면 추가
    if category is not None:
        post_data['category']=category
    model_res = post_model.insert_post(post_data)
    

    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    
    # TODO: image가 있으면 post_image에 추가해야한다.
    if images is not None:
        post_img_model = Post_Image(current_app.db)
        post_img_model.insert_post_image({
            'img_path':images,
            'post_id':model_res
        })
    return response_200(model_res)

@api.get('/post/<post_id>')
@timer
@login_required
@Validator(bad_request)
def post_get_api(
    post_id: int = Route(int)
):
    '''
    특정 게시물 반환 API
    '''
    post_model = Post(current_app.db)
    model_res = post_model.get_post_by_postid(post_id, g.user_id)
    if model_res is None:
        return bad_request('There are no posts.')
    res_form = {
		"board_title": model_res.get('board_title'),	
		"category": model_res.get('post_category'),
		"content": model_res.get('post_content'),
		"created_at": model_res.get('post_created_at'),
		"images": model_res.get('post_img_path'),
		"is_like": model_res.get('is_like'),
		"like_num": model_res.get('like_cnt'),
		"post_title": model_res.get('post_title'),
		"updated_at": model_res.get('post_updated_at'),
		"view_num": model_res.get('post_view_cnt'),
		"writer": model_res.get('user_nickname')
	}                       
    return response_200(res_form)


@api.delete('/post/<post_id>')
@timer
@login_required
@Validator(bad_request)
def post_delete_api(
    post_id: int = Route(int)
):
    post_model = Post(current_app.db)
    model_res = post_model.get_post_by_postid(post_id, g.user_id)
    # post_id에 해당하는 게시물이 없으면
    if model_res is None:
        return bad_request('There are no posts.')

    # 현재 사용자가 작성자가 아닌 경우
    if model_res.get('post_user_id') != g.user_id:
        return unauthorized('You do not have permission.')
    
    model_res = post_model.delete_post_by_postid(post_id)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    print(model_res)
    return response_200()

@api.patch('/post/<post_id>')
@timer
@login_required
@Validator(bad_request)
def post_update_api(
    post_id: int = Route(int),
    title=Json(str, rules=[MinLen(1), MaxLen(100)]),
	content=Json(str, rules=[MinLen(1), MaxLen(2000)]),
	images=Json(str, rules=[MaxLen(200)],optional=True),
	category=Json(str, rules=[MinLen(1), MaxLen(10)], optional=True),
):
    post_model = Post(current_app.db)
    model_res = post_model.get_post_by_postid(post_id, g.user_id)
    # post_id에 해당하는 게시물이 없으면
    if model_res is None:
        return bad_request('There are no posts.')

    # 현재 사용자가 작성자가 아닌 경우
    if model_res.get('post_user_id') != g.user_id:
        return unauthorized('You do not have permission.')
    post_data = {
        'title': title,
        'content': content,
        'category': category
    }
    model_res = post_model.update_post_by_postid(post_id, post_data)
    
    # TODO: image가 있으면 post_image에 추가해야한다.
    if images is not None:
        post_img_model = Post_Image(current_app.db)
        img_model_res = post_img_model.update_post_image(images, post_id)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    if isinstance(img_model_res, Exception):
        return bad_request(model_res.__str__())
    print(model_res)
    return response_200()
    
@api.post('/post/img')
@timer
@login_required
@Validator(bad_request)
def post_img_upload_api(
    post_img: File = File(
        rules=[
            Ext(['.png', '.jpg', '.jpeg', '.gif', '.heic']),
            MaxFileCount(1)
        ]
    )
):
    """ 게시물 사진 업로드 API"""
    return response_200(
        upload_to_s3(
            s3=current_app.s3,
            files=post_img,
            type="post",
            object_id=f"{g.user_id}_{uuid4()}"
        )[0]
    )

@api.post('post/like/<post_id>')
@timer
@login_required
@Validator(bad_request)
def post_like_insert_api(
    post_id: int = Route(int)
):
    """ 게시물 좋아요 생성 API"""
    model = Post_Like(current_app.db)
    model_res = model.insert_like(g.user_id, post_id)
    
    if isinstance(model_res, Exception):
        
        return conflict(model_res.__str__())
    else:
        return response_200()
    
@api.delete('post/like/<post_id>')
@timer
@login_required
@Validator(bad_request)
def post_like_delete_api(
    post_id: int = Route(int)
):
    """ 게시물 좋아요 삭제 API """
    model = Post_Like(current_app.db)
    model_res = model.delete_like(g.user_id, post_id)
    print(model_res)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    else:
        return no_content

@api.get('post/like/<post_id>')
@timer
@login_required
@Validator(bad_request)
def post_like_cnt_get_api(
    post_id: int = Route(int)
):
    """ 게시물 좋아요 수 반환 API"""
    model = Post_Like(current_app.db)
    model_res = model.get_like_cnt(post_id)
    return response_200(model_res)