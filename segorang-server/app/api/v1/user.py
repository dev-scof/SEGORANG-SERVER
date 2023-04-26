"""User 관련 APIs"""
from flask import g, current_app
from flask_validation_extended import Json, Route, File
from flask_validation_extended import Validator, MinLen, Ext, MaxFileCount, MaxLen
from bson.objectid import ObjectId
from app.api.response import response_200, created, no_content, conflict
from app.api.response import bad_request
from app.api.decorator import login_required, timer
from app.api.validation import ObjectIdValid
from controller.util import remove_none_value
from controller.file_util import upload_to_s3
from controller.auth.sejong import sejong_auth
from model.mysql.user import User
from model.mysql.user_image import User_Image
from uuid import uuid4
from . import api_v1 as api


@api.get('/user')
@timer
@login_required
def user_get_api():
    user_model = User(current_app.db)
    model_res = user_model.get_user_by_single_property('id', g.user_id)
    res={
        'id': model_res.get('id'),
        'name': model_res.get('user_name'),
        'nickname': model_res.get('nickname'),
        'major': model_res.get('major')
    }
    return response_200(res)

@api.get('/user/pw')
@timer
@Validator(bad_request)
def user_get_pw_api(
    sj_id=Json(str, rules=MinLen(1)),
    sj_pw=Json(str, rules=MinLen(1))
):
    '''
    사용자 비밀번호 찾기
    '''
    # 1. 세종인증 진행하기
    result = sejong_auth({
        'sj_id':sj_id,
        'sj_pw':sj_pw
    })
    if result.is_auth is not True:
        return bad_request("잘못된 정보입니다.")
    model = User(current_app.db)
    model_res = model.get_user_by_elem(['pw'], {'sj_id':sj_id})
    if model_res is None:
        return bad_request("등록되지 않은 사용자입니다.")
    return response_200(model_res)

@api.get('/user/id')
@timer
@Validator(bad_request)
def user_get_id_api(
    sj_id=Json(str, rules=MinLen(1)),
    sj_pw=Json(str, rules=MinLen(1))
):
    '''
    사용자 아이디 찾기
    '''
    # 1. 세종인증 진행하기
    result = sejong_auth({
        'sj_id':sj_id,
        'sj_pw':sj_pw
    })
    if result.is_auth is not True:
        return bad_request("잘못된 정보입니다.")
    model = User(current_app.db)
    model_res = model.get_user_by_elem(['id'], {'sj_id':sj_id})
    if model_res is None:
        return bad_request("등록되지 않은 사용자입니다.")
    return response_200(model_res)

@api.post('/user/img')
@timer
@login_required
@Validator(bad_request)
def user_upload_img_api(
    user_img: File = File(
        rules=[
            Ext(['.png', '.jpg', '.jpeg', '.gif', '.heic']),
            MaxFileCount(1)
        ]
    )
):
    img_path = upload_to_s3(
            s3=current_app.s3,
            files=user_img,
            type="user",
            object_id=f"{g.user_id}_{uuid4()}"
        )[0]
    
    """ 사용자 사진 업로드 API """
    return response_200(img_path)

@api.patch('/user')
@timer
@login_required
@Validator(bad_request)
def user_update_info_api(
    img_path=Json(str, rules=MinLen(1), optional=True),
    nickname=Json(str, rules=MaxLen(15), optional=True),
    pw=Json(str, rules=MaxLen(20), optional=True),
):
    '''
    사용자 정보 변경
    '''
    new_info = remove_none_value(locals())
    
    if new_info.get('img_path') is not None:
        # 이미지 저장
        model = User_Image(current_app.db)
        model_res = model.insert_user_image({
            'img_path':img_path,
            'user_id':g.user_id
        })
        if isinstance(model_res, Exception):
            return bad_request(model_res.__str__())
        del new_info['img_path']

    if new_info:
        model = User(current_app.db)
        model_res = model.update_user_by_id(new_info, g.user_id)
        if isinstance(model_res, Exception):
            # TODO: 중복될 경우, 중복확인
            return bad_request(model_res.__str__())

    return no_content