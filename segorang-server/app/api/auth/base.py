# """
# API Server Base Auth APIs
# """
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_validation_extended import Validator, Json, MinLen, MaxLen, Number
from flask_jwt_extended import (
    get_jwt_identity, create_refresh_token, create_access_token, jwt_required
)
from app.api.response import response_200, bad_request, forbidden, no_content, conflict, unauthorized
from app.api.decorator import timer, login_required
from model.mysql.user import User
from MySQLdb import IntegrityError
from config import config
from . import api_auth as api
from datetime import timedelta
from config import Config


@api.post('/signin')
@Validator(bad_request)
@timer
def signin_api(
    id=Json(str, rules=[MinLen(5), MaxLen(20)]),
    pw=Json(str, rules=[MinLen(8), MaxLen(16)]),
):
    """로그인 API"""
    user_model = User(current_app.db)
    model_res = user_model.get_user_by_single_property('id', id)

    if model_res is None:
        return unauthorized("Invalid Login Infomation")
    elif model_res.get('pw') != pw:
        return unauthorized("Invalid Login Infomation")

    return response_200({
        'access_token': create_access_token(
            identity = id,
            expires_delta = timedelta(Config.JWT_ACCESS_TOKEN_EXPIRES)),
        'refresh_token': create_refresh_token(
            identity = id,
            expires_delta = timedelta(Config.JWT_ACCESS_TOKEN_EXPIRES))
    })


@api.post('/signup')
@Validator(bad_request)
@timer
def auth_signup_api(
    sj_id=Json(str, rules=MinLen(2)),
    id=Json(str, rules=[MinLen(5), MaxLen(20)]),
    pw=Json(str, rules=[MinLen(8), MaxLen(16)]),
    name=Json(str, rules=[MinLen(1), MaxLen(20)]),
    major=Json(str, rules=[MinLen(1), MaxLen(20)]),
    nickname=Json(str, rules=[MinLen(3), MaxLen(20)]),
    sejong_auth=Json(bool)
):
    """회원가입 API"""
    user_model = User(current_app.db)
    model_res = user_model.insert_user({
        'sj_id':sj_id,
        'id':id,
        'pw':pw,
        'user_name':name,
        'major':major,
        'nickname':nickname,
        'sejong_auth':sejong_auth
    })

    # 중복 error 발생시
    if isinstance(model_res, IntegrityError):
        return conflict("Duplicate key or Foreign Key Constraint fail")
    # 이외 다른 예외 발생시
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())

    # 회원가입 완료
    return response_200()


@api.delete("")
@login_required
@timer
def auth_withdrawal_api():
    """회원 탈퇴 API"""
    user_id = get_jwt_identity()
    user_model = User(current_app.db)
    model_res = user_model.delete_user_by_id(user_id)
    if model_res:
        return no_content
    else:
        return bad_request(model_res)



@api.post('/id')
@Validator(bad_request)
@timer
def auth_check_duplicate_id_api(
    id=Json(str, rules=[MinLen(5), MaxLen(20)])
):
    """ID 중복 확인"""
    user_model = User(current_app.db)
    model_res = user_model.get_user_by_single_property('id', id)
    res = {}
    if model_res is None:
        res['in_db']=False
    else:
        res['in_db']=True
    return response_200(res)


@api.post('/nickname')
@Validator(bad_request)
@timer
def auth_check_duplicate_nickname_api(
    nickname=Json(str, rules=[MinLen(3), MaxLen(20)])
):
    """NICKNAME 중복 확인"""
    user_model = User(current_app.db)
    model_res = user_model.get_user_by_single_property('nickname', nickname)
    res = {}
    if model_res is None:
        res['in_db']=False
    else:
        res['in_db']=True
    return response_200(res)


@api.get('/refresh')
@jwt_required(refresh=True)
def auth_get_refresh_token():
    """JWT 토큰 리프레시"""
    id = get_jwt_identity()
    return response_200({
        'access_token': create_access_token(
            identity=id,
            expires_delta= timedelta(Config.JWT_ACCESS_TOKEN_EXPIRES)
        ),
        'refresh_token': create_refresh_token(
            identity=id,
            expires_delta= timedelta(Config.JWT_ACCESS_TOKEN_EXPIRES)
        ),
    })


# @api.get("/auth-test")
# @jwt_required()
# @timer
# def auth_test_api():
#     """인증 테스트"""
#     return response_200("hello, %s" % get_jwt_identity())


