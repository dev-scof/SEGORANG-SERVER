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
from . import api_v1 as api


@api.get("/users/me")
@timer
@login_required
def api_v1_get_users_me():
    """내 정보 반환 API"""
    return response_200(
    )

