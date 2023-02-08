from flask import Blueprint, request, jsonify, current_app, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_validation_extended import Validator, Json, MinLen
from app.api.response import bad_request, response_200, unauthorized
from app.api.decorator import timer
from controller.auth.sejong import sejong_auth
from model.mongodb import User
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
    cur_data = request.get_json()
    current_app.logger.info("회원가입 API 요청들어옴\n"\
                            "받은 값 = {}".format(cur_data))
    result = sejong_auth(cur_data)
    if result.is_auth == True:
        current_app.logger.info("인증 완료")
        return response_200({
            'AuthResponse': result,
        })
    else:
        return bad_request('잘못된 정보입니다.')
    