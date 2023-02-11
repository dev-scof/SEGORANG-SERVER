from . import api_v1 as api

@api.get('/create')
def api_v1_create():
    return "create"

@api.get('/read')
def api_v1_read():
    pass

@api.get('/update')
def api_v1_update():
    pass

@api.get('/delete')
def api_v1_delete():
    pass
