from . import api_v1 as api
from flask import g, current_app, request
from flask_validation_extended import Json, Route, File, Query, Min
from flask_validation_extended import Validator, MinLen, Ext, MaxFileCount, MaxLen
from bson.objectid import ObjectId
from app.api.response import response_200, created, no_content, conflict
from app.api.response import bad_request
from app.api.decorator import login_required, timer, admin_required
from app.api.validation import ObjectIdValid
from controller.util import remove_none_value
from controller.file_util import upload_to_s3
from model.mysql.youtube import Youtube
from . import api_v1 as api

@api.get('/youtube')
@timer
@Validator(bad_request)
@login_required
def youtube_get_api(
    page=Query(int, rules=Min(1)),
    limit=Query(int, rules=Min(1))
):
    model = Youtube(current_app.db)
    model_res = model.get_youtube(page-1, limit)
    return response_200(model_res)

@api.post('/youtube')
@timer
@admin_required
@Validator(bad_request)
def youtube_insert_api(
    thumb_nail=Json(str, rules=MinLen(1)),
    title=Json(str, rules=MinLen(1)),
    link=Json(str, rules=MinLen(1))
):
    model = Youtube(current_app.db)
    data={
        'thumb_nail':thumb_nail,
        'title':title,
        'link':link
    }
    model_res = model.insert_youtube(data)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    
    return no_content

@api.patch('/youtube')
@timer
@admin_required
def youtube_update_api(
    thumb_nail=Json(str, rules=MinLen(1), optional=True),
    title=Json(str, rules=MinLen(1), optional=True),
    link=Json(str, rules=MinLen(1), optional=True),
    id=Json(int, rules=Min(0))
):
    '''
    유튜브 정보 수정 API
    '''
    model = Youtube(current_app.db)
    data = request.get_json()
    id=data.pop('id')
    model_res = model.update_youtube_by_id(id, data)

    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    return no_content

@api.delete('/youtube')
@timer
def youtube_delete_api(
    id=Query(int, rules=Min(0))
):
    '''
    유튜브 정보 삭제
    '''
    model = Youtube(current_app.db)
    model_res = model.delete_youtube_api(id)
    if isinstance(model_res, Exception):
        return bad_request(model_res.__str__())
    return no_content