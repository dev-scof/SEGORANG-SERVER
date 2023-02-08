from dataclasses import dataclass
from flask import g, current_app
from sejong_univ_auth import auth, DosejongSession
from datetime import datetime
import json, itertools
"""
Params
--------
sj_id : 세종대학교 포털 아이디
sj_pw : 세종대학교 포털 비밀 번호
Return
--------
Bool (True or False)
"""
def sejong_auth(user_data:dict):
    result = auth(
                id=user_data.get('sj_id'),
                password=user_data.get('sj_pw'), 
                methods=DosejongSession)
    return result