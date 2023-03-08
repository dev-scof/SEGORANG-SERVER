from flask import Blueprint, request, jsonify, current_app, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_validation_extended import Validator, Json, MinLen
from app.api.response import bad_request, response_200, unauthorized
from app.api.decorator import timer
from controller.auth.sejong import sejong_auth
from model.mysql.user import User
from config import Config
from datetime import timedelta
from . import api_auth as api


@api.post("/sejong")
@Validator(bad_request)
@timer
def sejong_auth_api(
    sj_id=Json(str),
    sj_pw=Json(str)
):
    result = sejong_auth({
        'sj_id':sj_id,
        'sj_pw':sj_pw
    })

    if result.is_auth == True:
        current_app.logger.info("인증 완료")
        user_model = User(current_app.db)
        model_res = user_model.get_user_by_single_property('sj_id', sj_id)
        if model_res is None:
            return response_200({
                'AuthResponse': result,
                'in_db': False
            })
        else:
            return response_200({
                'AuthResponse': result,
                'in_db': True
            })
    else:
        return bad_request('잘못된 정보입니다.')
