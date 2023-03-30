from . import api_v1 as api
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


@api.get('/youtube')
@timer
@login_required
def api_v1_get_youtube():
    return response_200([
        {
            'thumbNail':'https://i.ytimg.com/vi/__092GlqCUw/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD4C6IcOdd3cleTDtGQMQCNW8AVnA',
            'title': '[어쩌다 신입생🤔] 20학번의 강제 23학번 체험기❗️',
            'link': 'https://www.youtube.com/watch?v=__092GlqCUw&ab_channel=%EC%84%B8%EC%A2%85%EB%8C%80%ED%95%99%EA%B5%90',
        },
        {
            'thumbNail':'https://i.ytimg.com/vi/9Acim_CfG1U/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDnlQAHyLaCbqKofrlUaj4rFN6IRA',
            'title': '[학과 소개 인터뷰📢] EP. 미디어커뮤니케이션학과🎥',
            'link': 'https://www.youtube.com/watch?v=9Acim_CfG1U&ab_channel=%EC%84%B8%EC%A2%85%EB%8C%80%ED%95%99%EA%B5%90',
        },
        {
            'thumbNail':'https://i.ytimg.com/vi/lOrNhpOFcQY/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLA9Hpc6FvZM1UkLfaHIw8nYPXji8w',
            'title': '[🛞대학생을 위한 운전면허 꿀팁🛞] 운전면허 독학으로 취득하고 싶다면⁉️',
            'link': 'https://www.youtube.com/watch?v=lOrNhpOFcQY&ab_channel=%EC%84%B8%EC%A2%85%EB%8C%80%ED%95%99%EA%B5%90',
        }])