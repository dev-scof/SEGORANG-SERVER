def set_quote(data):
        if isinstance(data, str):
            # 문자열이면
            return f'\"{data}\"'
        else:
            return f'{data}'

def get_fields_data(data:dict):
    '''dict를 keys, values로 반환'''
    keys=[]
    values=[]
    for k, v in data.items():
        keys.append(k)
        values.append(v)
    return keys, values