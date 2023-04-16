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
from model.mysql.user import User
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

